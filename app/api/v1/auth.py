"""Authentication router for user registration and login endpoints.

This router is intentionally thin — it delegates validation and business
logic to the service layer (`app.services.auth_service`). Endpoints
return response models declared via Pydantic schemas.
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.schemas.auth_schema import LoginRequestSchema, TokenResponseSchema
from app.schemas.user_schema import UserRegisterSchema, UserResponseSchema
from app.services.auth_service import login_user, register_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
)
def register_endpoint(payload: UserRegisterSchema) -> UserResponseSchema:

    print("STEP A - ENDPOINT HIT")

    created = register_user(
        {
            "name": payload.name,
            "email": payload.email,
            "password": payload.password,
        }
    )

    print("STEP B - SERVICE COMPLETED")
    print(created)

    response = UserResponseSchema(
        id=str(created.get("_id")),
        name=created.get("name"),
        email=created.get("email"),
    )

    print("STEP C - RESPONSE CREATED")

    return response

@router.post(
    "/login",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user with email and password. Returns a JWT access token on success.",
    responses={
        status.HTTP_200_OK: {
            "description": "Login successful. JWT access token returned.",
            "model": TokenResponseSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Missing email or password in request body.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid email or password.",
        },
    },
)
def login_endpoint(payload: LoginRequestSchema) -> TokenResponseSchema:
    """Authenticate user and return JWT access token.

    This endpoint accepts user credentials and returns a signed JWT token
    for subsequent API requests. All validation and token generation is
    delegated to the service layer.

    Args:
        payload: LoginRequestSchema containing email and password.

    Returns:
        TokenResponseSchema with access_token (JWT) and token_type ("Bearer").

    Raises:
        HTTPException(400): If email or password is missing or invalid format.
        HTTPException(401): If email not found or password is incorrect.
    """
    token_response: TokenResponseSchema = login_user(
        {"email": payload.email, "password": payload.password}
    )
    return token_response


@router.get(
    "/me",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve the authenticated user's profile information.",
    responses={
        status.HTTP_200_OK: {
            "description": "User profile retrieved successfully.",
            "model": UserResponseSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid, or expired Bearer token.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found in the database.",
        },
    },
)
def get_me_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> UserResponseSchema:
    """Retrieve the authenticated user's profile.

    This is a protected endpoint that requires a valid JWT token in the
    Authorization header (Bearer scheme). The token is validated, decoded,
    and the associated user is fetched from the database and returned.

    Args:
        current_user: The authenticated user document from the database.
                     Injected via Depends(get_current_user).

    Returns:
        UserResponseSchema containing the user's id, name, and email.

    Raises:
        HTTPException(401): If token is missing, invalid, or expired.
        HTTPException(404): If user is not found in the database.
    """
    return UserResponseSchema(
        id=str(current_user.get("_id")),
        name=current_user.get("name"),
        email=current_user.get("email"),
    )

