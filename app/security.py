"""Authentication dependencies for private API routes."""

import secrets

from fastapi import Header, HTTPException, status

from config import ADMIN_API_KEY, WIX_API_KEY


def _verify_key(
    *,
    configured_key: str | None,
    supplied_key: str | None,
    missing_configuration_message: str,
    invalid_credentials_message: str,
    authenticate_header: str,
) -> None:
    if not configured_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=missing_configuration_message,
        )

    if not supplied_key or not secrets.compare_digest(supplied_key, configured_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=invalid_credentials_message,
            headers={"WWW-Authenticate": authenticate_header},
        )


async def require_wix_api_key(
    x_wix_key: str | None = Header(default=None, alias="X-Wix-Key"),
) -> None:
    """Authenticate calls made by the Wix backend web methods."""
    _verify_key(
        configured_key=WIX_API_KEY,
        supplied_key=x_wix_key,
        missing_configuration_message="Wix access is not configured.",
        invalid_credentials_message="Invalid Wix credentials.",
        authenticate_header="X-Wix-Key",
    )


async def require_admin_api_key(
    x_admin_key: str | None = Header(default=None, alias="X-Admin-Key"),
) -> None:
    """Allow access only when the configured admin key matches the request header.

    A missing server configuration is treated as unavailable rather than silently
    making the lead database public.
    """
    _verify_key(
        configured_key=ADMIN_API_KEY,
        supplied_key=x_admin_key,
        missing_configuration_message="Admin access is not configured.",
        invalid_credentials_message="Invalid admin credentials.",
        authenticate_header="X-Admin-Key",
    )
