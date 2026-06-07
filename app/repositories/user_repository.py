"""Repository layer for MongoDB user operations.

This module contains only database access functions. Business logic
must remain in the service layer.
"""

from typing import Any, Dict, Optional

from bson import ObjectId

from app.database import users_collection


def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a new user document into the `users` collection.

    Args:
        user_data: A dictionary representing the user document to insert.

    Returns:
        The inserted MongoDB document (as returned by `find_one`).
    """
    result = users_collection.insert_one(user_data)
    return users_collection.find_one({"_id": result.inserted_id})


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Find a user document by email.

    Args:
        email: Email address to query by.

    Returns:
        The matching user document or `None` if not found.
    """
    return users_collection.find_one({"email": email})


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Find a user document by its string ObjectId.

    Args:
        user_id: String representation of the MongoDB ObjectId.

    Returns:
        The matching user document or `None` if not found or if the id
        is not a valid ObjectId.
    """
    try:
        oid = ObjectId(user_id)
    except Exception:
        # Invalid ObjectId format — treat as not found at repository level
        return None

    return users_collection.find_one({"_id": oid})
