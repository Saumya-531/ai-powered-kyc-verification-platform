from datetime import datetime

from pydantic import BaseModel


class VerificationReportSchema(
    BaseModel
):

    document_id: str

    aadhaar: str | None

    aadhaar_valid: bool

    pan: str | None

    pan_valid: bool

    identity_verified: bool

    risk_score: int

    risk_level: str


class StoredReportSchema(
    BaseModel
):

    id: str

    user_id: str

    document_id: str

    identity_verified: bool

    risk_score: int

    risk_level: str

    created_at: datetime