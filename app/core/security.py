"""Security utilities for password hashing and JWT access tokens.

This module provides helper functions for hashing passwords using bcrypt
and creating/validating JWT access tokens. It uses timezone-aware
datetimes for token timestamps and raises FastAPI `HTTPException` on
invalid tokens to integrate cleanly with request handlers.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import HTTPException, status
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from app.config import settings

logger = logging.getLogger(__name__)

# Use bcrypt for password hashing. `deprecated="auto"` allows upgrade paths.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: Plain-text password provided by the user.

    Returns:
        The bcrypt hashed password as a string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a hashed password safely.

    Args:
        plain_password: The password provided by the user.
        hashed_password: The hashed password stored in the database.

    Returns:
        True if the password matches, False otherwise.
    """
    if not hashed_password:
        # Missing hashed password should fail verification
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Create a signed JWT access token including `iat` and `exp` claims.

    Generates a JWT token with timezone-aware UTC timestamps and strict
    claim validation. The provided data dictionary will be copied into the
    token payload to avoid mutating the caller's object.

    Required claims in `data`:
        - sub (str): Subject (user ID) — uniquely identifies the token holder
        - email (str): User email address for quick access without decoding

    Auto-generated claims:
        - iat (int): Issued-at timestamp (UNIX epoch, UTC)
        - exp (int): Expiration timestamp (UNIX epoch, UTC)

    Args:
        data: Dictionary containing JWT claims. Must include "sub" and "email".

    Returns:
        A JWT access token as a compact serialized string (JWS format).

    Raises:
        ValueError: If required claims ("sub", "email") are missing from data.
        HTTPException: If token encoding fails (500 error).

    Example:
        >>> token = create_access_token({
        ...     "sub": "user_id_123",
        ...     "email": "user@example.com"
        ... })
    """
    # Validate required claims
    if not data.get("sub"):
        logger.error("Token creation failed: missing 'sub' claim")
        raise ValueError("Claim 'sub' (user ID) is required for token creation.")
    if not data.get("email"):
        logger.error("Token creation failed: missing 'email' claim")
        raise ValueError("Claim 'email' is required for token creation.")

    # Generate timestamps (UTC)
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    # Build payload with registered and custom claims
    payload: Dict[str, Any] = data.copy()
    payload.update({
        "iat": int(now.timestamp()),      # Issued at (UNIX timestamp)
        "exp": int(expire.timestamp()),   # Expiration (UNIX timestamp)
    })

    # Encode and sign JWT
    try:
        token: str = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        logger.debug("JWT token created for user: %s", data.get("sub"))
        return token
    except Exception as exc:
        logger.exception("JWT token encoding failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate authentication token.",
        ) from exc


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token.

    Validates the JWT signature using the secret key and algorithm from
    settings, automatically validates token expiration via the `exp` claim,
    and returns the decoded payload. On any validation failure, raises
    HTTPException with status 401 and WWW-Authenticate header per RFC 6750.

    This function is the inverse of create_access_token(). It:
    1. Validates the JWT signature hasn't been tampered with
    2. Validates the token hasn't expired (via exp claim)
    3. Returns the payload if all validations pass
    4. Raises HTTPException(401) for any validation failure

    The WWW-Authenticate header is included in error responses to comply
    with OAuth2 Bearer Token specification (RFC 6750).

    Args:
        token: The JWT token string from the Authorization header (Bearer scheme).
               Should be a compact JWS format: "xxx.yyy.zzz"

    Returns:
        The decoded token payload as a dictionary. Typically contains:
        - sub (str): User ID
        - email (str): User email
        - iat (int): Issued-at timestamp (UNIX epoch)
        - exp (int): Expiration timestamp (UNIX epoch)
        - Additional custom claims if present

    Raises:
        HTTPException(401): If token is invalid or expired.
               - Invalid signature (secret key mismatch, tampering)
               - Expired (current time > exp claim)
               - Malformed (not valid JWS format)
               - Missing required claims (handled by caller)

    Example:
        >>> try:
        ...     payload = decode_access_token(token)
        ...     user_id = payload["sub"]
        ...     user_email = payload["email"]
        ... except HTTPException as exc:
        ...     # Token is invalid or expired
        ...     return 401 response
    """
    if not token:
        logger.warning("Token validation failed: token is empty")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # jwt.decode automatically validates:
        # - Signature using the secret key
        # - Algorithm matches the configured algorithm
        # - Expiration (exp claim must be > current time)
        payload: Dict[str, Any] = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        logger.debug("Token decoded successfully for user: %s", payload.get("sub"))
        return payload

    except ExpiredSignatureError as exc:
        logger.info("Token validation failed: token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    except JWTError as exc:
        # Catches all other JWT errors: invalid signature, malformed, etc.
        logger.warning("Token validation failed: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
