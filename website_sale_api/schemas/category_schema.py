"""Schema definitions for Category model."""

# pylint:disable=too-few-public-methods
from typing import List, Optional

from pydantic import BaseModel

from .pagination import PaginatedResponse


class ProductData(BaseModel):
    """Schema for product data"""

    id: int
    name: str


class ChildCategoryData(BaseModel):
    """Schema for child category data"""

    id: int
    parent_id: Optional[int] = None
    product_count: Optional[int] = None
    products: list[ProductData] = []


class CategoryData(BaseModel):
    """Schema for individual category data"""

    id: int
    name: str
    parent_id: Optional[int] = None
    image_256: Optional[str] = None
    child_ids: List[ChildCategoryData]
    product_count: Optional[int] = None


class CategoryResponse(PaginatedResponse[CategoryData]):
    """Response schema for Category model"""
