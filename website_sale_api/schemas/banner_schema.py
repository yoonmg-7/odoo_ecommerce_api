"""banner_schema.py"""

from dataclasses import dataclass


@dataclass
class BannerSchema:
    """Schema for badges"""

    id: int
    description: str
    image_1920: str
