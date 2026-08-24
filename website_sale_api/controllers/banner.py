"""Controller for handling product banner in the e-commerce API."""

# pylint: disable=import-error,too-few-public-methods
from odoo import http
from odoo.exceptions import ValidationError
from ..services.banner_service import BannerService
from .base import BaseAPI


class BannerController(BaseAPI):
    """API controller for product banner."""

    @http.route(
        "/api/banners",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_banners(self):
        """Fetch all product ribbons."""

        try:
            return self._success(BannerService().fetch_all_banners())

        except ValidationError as e:
            return self._error(
                message=str(e),
                code=400,
            )
