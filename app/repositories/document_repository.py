"""Repository layer for document-related MongoDB operations."""

from typing import Optional

from bson import ObjectId

from app.database import documents_collection


def create_document(document_data: dict) -> dict:
    """
    Insert a document record into MongoDB.
    """

    result = documents_collection.insert_one(document_data)

    return documents_collection.find_one(
        {"_id": result.inserted_id}
    )


def get_document_by_id(document_id: str) -> Optional[dict]:
    """
    Retrieve a document by MongoDB ObjectId.
    """

    try:
        object_id = ObjectId(document_id)

    except Exception:
        return None

    return documents_collection.find_one(
        {"_id": object_id}
    )


def get_documents_by_user(user_id: str) -> list:
    """
    Retrieve all uploaded documents for a user.
    """

    return list(
        documents_collection.find(
            {"user_id": user_id}
        )
    )