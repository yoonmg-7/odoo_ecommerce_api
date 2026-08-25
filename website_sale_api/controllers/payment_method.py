"""Controller for Payment Methods API endpoints"""

# pylint:disable=import-error,broad-exception-caught,too-few-public-methods
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from ..services.api_key_service import ApiKeyService
from ..services.payment_method_service import PaymentMethodService
from ..services.token_service import JWTService
from .base import BaseAPI


class PaymentMethodController(BaseAPI):
    """Payment Method API Controller"""

    @http.route(
        "/api/payment_methods", methods=["GET"], type="http", auth="public", csrf=False
    )
    @ApiKeyService.api_key_required()
    @JWTService.jwt_required()
    def get_payment_methods(self):
        """Get all available payment methods selected by delivery method"""
        try:
            user = request.authenticated_user
            result = PaymentMethodService().get_website_payment_methods(user)
            return self._success(result)
        except ValidationError as e:
            return self._error(message=str(e), code=400)
        except Exception as e:
            return self._error(message=str(e), code=400)
