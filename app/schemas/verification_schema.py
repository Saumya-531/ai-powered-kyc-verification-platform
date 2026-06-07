from pydantic import BaseModel


class VerificationResponseSchema(BaseModel):

    document_id: str

    aadhaar: str | None

    aadhaar_valid: bool

    pan: str | None

    pan_valid: bool