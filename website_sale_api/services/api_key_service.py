"""Api key Service - Handle all token operations and authentication middleware."""

# pylint:disable=import-error,too-few-public-methods
import json
import logging
from functools import wraps

from odoo.http import request

_logger = logging.getLogger(__name__)

SMEI_API_KEY = "9f3a8c2e7b6a1d4f9e3c8a2b7c6d5e4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4"


class ApiKeyService:
    """Api key Service - Handle all token operations"""

    @staticmethod
    def _verify_api_key(key):
        """Verify API key"""
        return SMEI_API_KEY == key

    @staticmethod
    def _unauthorized_response(message="Authentication required"):
        """Return unauthorized response"""
        return request.make_response(
            json.dumps({"error": "unauthorized", "message": message, "code": 401}),
            status=401,
            headers={"Content-Type": "application/json"},
        )

    @staticmethod
    def api_key_required():
        """
        API Key Authentication Decorator
        Checks for 'eco-smei-api-key' header in the request
        """

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                api_key = request.httprequest.headers.get("eco-smei-api-key")

                # Check if API key is provided
                if not api_key:
                    return ApiKeyService._unauthorized_response(
                        "API key required. Please provide 'eco-smei-api-key' in headers"
                    )

                # Verify API key
                if not ApiKeyService._verify_api_key(api_key):
                    return ApiKeyService._unauthorized_response("Invalid API key")

                # API key is valid, proceed to endpoint
                return func(self, *args, **kwargs)

            return wrapper

        return decorator
