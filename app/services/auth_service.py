"""Authentication service layer for registration and login business logic.

This module contains the service-level functions which orchestrate
repository calls and security utilities. It does not perform HTTP
request handling (that belongs in the router layer).
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.auth_schema import TokenResponseSchema

logger = logging.getLogger(__name__)


def register_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Register a new user.

    Args:
        user_data: Dictionary containing `name`, `email`, and `password`.

    Returns:
        The created user document as returned by the repository.

    Raises:
        HTTPException: If email already exists or creation fails.
    """
    name = user_data.get("name")
    email = user_data.get("email")
    password = user_data.get("password")

    if not (name and email and password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name, email and password are required",
        )

    # Ensure email uniqueness
    if get_user_by_email(email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    # Prepare user document (hash password and set created_at)
    now = datetime.now(timezone.utc)
    to_insert = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": hash_password(password),
        "created_at": now,
    }

    created = create_user(to_insert)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user.",
        )

    return created


def login_user(login_data: Dict[str, Any]) -> TokenResponseSchema:
    """Authenticate user credentials and return a JWT token response.

    This function validates email and password, retrieves the user from the
    database, verifies the password, and generates a signed JWT token with
    the user ID and email as claims.

    Args:
        login_data: Dictionary containing `email` (str) and `password` (str).
                   Typically passed from LoginRequestSchema validation.

    Returns:
        A `TokenResponseSchema` containing the access token and token type.

    Raises:
        HTTPException: If required fields are missing (400), or if
                      email is not found or password is incorrect (401).

    Note:
        - Returns 401 for both user-not-found and password-mismatch to prevent
          email enumeration attacks.
        - Token claims include "sub" (user_id) and "email".
        - All business logic is isolated here; routers must not contain logic.
    """
    # Validate required fields
    email = login_data.get("email")
    password = login_data.get("password")

    if not (email and password):
        logger.warning("Login attempt with missing credentials")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email and password are required",
        )

    # Retrieve user from database
    user = get_user_by_email(email)

    # Verify user exists and password is correct (intentionally vague for security)
    if user is None or not verify_password(password, user.get("password", "")):
        logger.warning("Failed login attempt for email: %s", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # Generate JWT token with user ID and email as claims
    user_id: str = str(user.get("_id"))
    user_email: str = user.get("email", "")
    token_payload: Dict[str, Any] = {
        "sub": user_id,
        "email": user_email,
    }
    access_token: str = create_access_token(token_payload)

    logger.info("Successful login for user: %s", user_id)
    return TokenResponseSchema(access_token=access_token, token_type="Bearer")
