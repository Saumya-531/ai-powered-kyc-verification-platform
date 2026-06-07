"""Repository for identity verification operations."""

from app.database import dummy_identities_collection


def find_identity(
    aadhaar: str | None,
    pan: str | None,
):
    """
    Search government identity database.
    """

    query = {}

    if aadhaar:
        query["aadhaar"] = aadhaar

    if pan:
        query["pan"] = pan

    if not query:
        return None

    return dummy_identities_collection.find_one(
        query
    )