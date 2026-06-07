"""FastAPI dependency functions for request context, authentication, and authorization.

This module provides reusable dependencies for extracting and validating
JWT tokens, authenticating users, and injecting authenticated user context
into route handlers. Dependencies use FastAPI's Depends() mechanism.
"""

import logging
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.repositories.user_repository import get_user_by_id

logger = logging.getLogger(__name__)

# OAuth2 scheme: reads Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    description="JWT Bearer token for authentication.",
    scopes={},
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Verify JWT token and return authenticated user document.

    This dependency:
    1. Extracts the Bearer token from the Authorization header
    2. Decodes and validates the JWT signature and expiration
    3. Extracts the user ID (sub) and email from the token payload
    4. Fetches the complete user document from the database
    5. Raises HTTPException if token is invalid, expired, or user not found

    The dependency is designed to be used with FastAPI's Depends() in route
    handlers to enforce authentication and inject the current user object.

    Args:
        token: Bearer token extracted from Authorization header by oauth2_scheme.

    Returns:
        The complete user document as a dictionary (from MongoDB).
        Includes fields: _id, name, email, password, created_at, etc.

    Raises:
        HTTPException(401): If token is invalid, expired, or user not found.

    Example:
        @router.get("/me")
        async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
            return current_user
    """
    # Decode and validate the JWT token
    # This will raise HTTPException(401) if invalid or expired
    payload: Dict[str, Any] = decode_access_token(token)

    # Extract user ID (subject claim) from payload
    user_id: Optional[str] = payload.get("sub")
    user_email: Optional[str] = payload.get("email")

    if not user_id:
        logger.warning("Token payload missing 'sub' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_email:
        logger.warning("Token payload missing 'email' claim for user: %s", user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database using the user ID from the token
    user: Optional[Dict[str, Any]] = get_user_by_id(user_id)

    if user is None:
        logger.warning("Authenticated token for non-existent user: %s", user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("User authenticated: %s (%s)", user_id, user_email)
    return user
