"""RibbonService"""

from .base_service import BaseService
from ..schemas.banner_schema import BannerSchema


class BannerService(BaseService):
    """BannerService"""

    def __init__(self, env=None):
        super().__init__(env)
        self.model_name = "product.banner"
        self.fields = [
            "id",
            "description",
            "image_1920",
            "image_1024",
            "image_256",
            "image_128",
        ]

    def fetch_all_banners(self):
        """Fetch all ribbons"""
        banners = self.search()

        return [
            BannerSchema(
                id=banner.id,
                description=banner.description,
                image_1920=self._get_image_url(
                    "product.banner",
                    banner.id,
                    size="image_1920",
                ),
            )
            for banner in banners
        ]
