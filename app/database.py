"""MongoDB connection module for the AI-Powered KYC Verification API."""

import logging
from typing import List

from pymongo import MongoClient
from pymongo.database import Collection, Database
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

from app.config import settings

logger = logging.getLogger(__name__)


def _create_mongo_client(uri: str) -> MongoClient:
    """Create a MongoDB client and verify the server connection."""
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # verify connection by pinging the server
        client.admin.command("ping")
        # Informative message for successful connections (useful in dev logs)
        print("Connected to MongoDB successfully")
        logger.info("MongoDB connection verified")
        return client
    except ServerSelectionTimeoutError as exc:
        logger.error("MongoDB server selection timed out: %s", exc)
        raise ConnectionError(
            "Could not connect to MongoDB server. Check that MongoDB is running and the MONGODB_URI is correct."
        ) from exc
    except PyMongoError as exc:
        logger.error("MongoDB connection error: %s", exc)
        raise RuntimeError("Failed to initialize MongoDB client.") from exc


def _get_database(client: MongoClient, database_name: str) -> Database:
    """Return the configured MongoDB database."""
    if not database_name:
        raise ValueError("DATABASE_NAME must be set in settings.")

    return client[database_name]


def _ensure_collections(database: Database, collection_names: List[str]) -> None:
    """Ensure required MongoDB collections exist."""
    try:
        existing = database.list_collection_names()
        for collection_name in collection_names:
            if collection_name not in existing:
                database.create_collection(collection_name)
    except PyMongoError as exc:
        logger.error("Failed to ensure MongoDB collections: %s", exc)
        raise RuntimeError("Could not prepare MongoDB collections.") from exc


def _get_collection(database: Database, name: str) -> Collection:
    """Return a MongoDB collection reference."""
    return database[name]


client: MongoClient = _create_mongo_client(
    settings.MONGODB_URI
)

db: Database = _get_database(
    client,
    settings.DATABASE_NAME
)

_collection_names = [
    "users",
    "documents",
    "verification_reports",
    "api_logs",
    "failed_attempts",
    "dummy_identities",
]

_ensure_collections(
    db,
    _collection_names
)

users_collection: Collection = _get_collection(
    db,
    "users"
)

documents_collection: Collection = _get_collection(
    db,
    "documents"
)

reports_collection: Collection = _get_collection(
    db,
    "verification_reports"
)

logs_collection: Collection = _get_collection(
    db,
    "api_logs"
)

failed_attempts_collection: Collection = _get_collection(
    db,
    "failed_attempts"
)

dummy_identities_collection: Collection = _get_collection(
    db,
    "dummy_identities"
)

__all__ = [
    "client",
    "db",
    "users_collection",
    "documents_collection",
    "reports_collection",
    "logs_collection",
    "failed_attempts_collection",
    "dummy_identities_collection",
]