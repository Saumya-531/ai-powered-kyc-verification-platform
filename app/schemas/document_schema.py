"""Document upload and response schemas (Pydantic v2).

Defines request and response models for document uploads and retrieval.
Document status represents the KYC verification state: pending, verified,
rejected, or expired. All fields support JSON serialization for API responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class DocumentResponseSchema(BaseModel):
    """Schema for document data returned in responses.

    Represents a document in the KYC platform. The `id` is a string
    representation of the MongoDB ObjectId, while `uploaded_at` is a
    datetime indicating when the document was uploaded. Status reflects
    the KYC verification state of the document.

    Used in endpoints that return document information (GET /documents/{id},
    GET /me/documents, etc.).
    """

    id: str = Field(
        ...,
        description="Document identifier (stringified MongoDB ObjectId).",
        example="60f7f9a7e13f4b2d9c0e4f1a",
    )
    file_name: str = Field(
        ...,
        description="Original filename as uploaded by the user.",
        example="passport_scan.pdf",
    )
    file_path: str = Field(
        ...,
        description="Server-side file path where document is stored.",
        example="/uploads/documents/60f7f9a7e13f4b2d9c0e4f1a/passport_scan.pdf",
    )
    uploaded_at: datetime = Field(
        ...,
        description="UTC timestamp when document was uploaded.",
        example="2025-06-06T14:30:45.123456Z",
    )
    status: Literal["pending", "verified", "rejected", "expired"] = Field(
        ...,
        description="KYC verification status of the document.",
        example="pending",
    )

    model_config = ConfigDict(from_attributes=True)


class UploadResponseSchema(BaseModel):
    """Schema for document upload response.

    Returned immediately after a document is successfully uploaded.
    Contains a confirmation message and the ID of the created document
    for subsequent tracking and retrieval.

    Used in POST /documents/upload endpoint (201 Created response).
    """

    message: str = Field(
        ...,
        description="Confirmation message about the upload.",
        example="Document uploaded successfully.",
    )
    document_id: str = Field(
        ...,
        description="ID of the newly created document (stringified MongoDB ObjectId).",
        example="60f7f9a7e13f4b2d9c0e4f1a",
    )

    model_config = ConfigDict(from_attributes=True)
