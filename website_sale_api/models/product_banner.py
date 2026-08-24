"""Product Banner Model"""

# pylint:disable=import-error,too-few-public-methods
from odoo import fields, models


class ProductBanner(models.Model):
    """Product Banner Model"""

    _name = "product.banner"
    _description = "Product Banner"
    _inherit = ["image.mixin"]

    description = fields.Text(string="Description")
