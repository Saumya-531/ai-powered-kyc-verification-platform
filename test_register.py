from app.services.auth_service import register_user

result = register_user(
    {
        "name": "Saumya",
        "email": "saumya_debug@gmail.com",
        "password": "password123"
    }
)

print(result)