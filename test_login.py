from app.repositories.user_repository import get_user_by_email
from app.core.security import verify_password

user = get_user_by_email("saumya@gmail.com")

print("USER:", user)

if user:
    result = verify_password(
        "password123",
        user["password"]
    )

    print("PASSWORD MATCH:", result)