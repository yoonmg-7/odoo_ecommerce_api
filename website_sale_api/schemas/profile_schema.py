"""Response schema for user profile endpoint combining UserData and Profile"""

# pylint:disable=too-many-instance-attributes
from dataclasses import dataclass
from typing import Optional

from .auth_schema import UserData


@dataclass
class Profile:
    """Response schema for user profile endpoint"""

    email: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    partner_id: Optional[int] = None
    country_id: Optional[int] = None
    state_id: Optional[int] = None
    township_id: Optional[int] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    image_url: Optional[str] = None


@dataclass
class ProfileResponse(Profile, UserData):
    """Response schema for user profile endpoint combining UserData and Profile"""
