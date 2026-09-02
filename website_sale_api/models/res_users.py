"""Override read access field to read without login"""

# pylint:disable=import-error,too-few-public-methods,broad-exception-caught,protected-access
import random
from datetime import datetime, timedelta

from odoo import fields, models


class ResUsers(models.Model):
    """Override read access field to read without login"""

    _inherit = "res.users"

    reset_code = fields.Char(string="Reset Code", size=6, copy=False)
    reset_code_expiry = fields.Datetime(string="Reset Code Expiry", copy=False)
    reset_code_used = fields.Boolean(
        string="Reset Code Used", default=False, copy=False
    )
    mobile_device_token = fields.Char(
        string="Mobile Device Token",
        help="Store mobile device token for each user to push notifications",
    )
    last_login = fields.Datetime(
        string="Last Login", help="Store last login time by mobile user"
    )

    def _can_return_content(self, field_name=None, access_token=None):
        """Field to allow to read without login"""
        if field_name in [
            "image_1920",
            "image_1024",
            "image_512",
            "image_256",
            "image_128",
        ]:
            return True
        return super()._can_return_content(field_name, access_token)

    def generate_reset_code(self):
        """Generate a 6-digit random code"""
        return "".join([str(random.randint(0, 9)) for _ in range(6)])

    def create_reset_code(self):
        """Set reset code with 5-minute expiry"""
        code = self.generate_reset_code()
        self.write(
            {
                "reset_code": code,
                "reset_code_expiry": datetime.now() + timedelta(minutes=5),
                "reset_code_used": 0,
            }
        )
        self._send_otp_email()
        return code

    def _send_otp_email(self):
        """Send OTP code via email using Odoo's mail system"""
        email_values = {
            "email_cc": False,
            "auto_delete": True,
            "message_type": "user_notification",
            "recipient_ids": [],
            "partner_ids": [],
            "scheduled_date": False,
        }
        email_values["email_to"] = self.login
        user_lang = self.lang or self.env.lang or "en_US"
        body = (
            self.env["mail.render.mixin"]
            .with_context(lang=user_lang)
            ._render_template(
                self.env.ref("website_sale_api.mail_template_user_password_reset_otp"),
                model="res.users",
                res_ids=[self.id],
                engine="qweb_view",
                options={"post_process": True},
            )[self.id]
        )
        mail = (
            self.env["mail.mail"]
            .sudo()
            .create(
                {
                    "subject": self.with_context(lang=user_lang).env._(
                        "Password reset"
                    ),
                    "email_from": self.company_id.email_formatted
                    or self.email_formatted,
                    "body_html": body,
                    **email_values,
                }
            )
        )
        mail.send()

    def is_reset_code_valid(self, code):
        """
        Check if reset code is valid with single attempt only
        - If code is wrong: mark as used and invalidate
        - If code is correct: mark as used and allow
        """
        self.ensure_one()
        if self.reset_code_used:
            return False, "Reset code already used"
        # Check if code matches
        if self.reset_code != code:
            return (
                False,
                "Invalid reset code. This code can only be used once. Please request a new code.",
            )

        # Check if expired
        if datetime.now() > self.reset_code_expiry:
            return False, "Reset code has expired. Please request a new code."

        self.write(
            {
                "reset_code_used": True,
            }
        )

        return True, "Valid code"
