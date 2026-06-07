from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.repositories.document_repository import (
    create_document,
    get_document_by_id,
)

from app.repositories.verification_repository import (
    find_identity,
)

from app.services.aadhaar_service import (
    extract_aadhaar,
    validate_aadhaar,
)

from app.services.pan_service import (
    extract_pan,
    validate_pan,
)

from app.services.risk_service import (
    calculate_risk_score,
)

UPLOAD_DIR = Path("uploads")


def upload_document(
    file: UploadFile,
    current_user: dict,
) -> dict:

    try:

        UPLOAD_DIR.mkdir(exist_ok=True)

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        document_data = {
            "user_id": str(current_user["_id"]),
            "file_name": file.filename,
            "file_path": str(file_path),
            "uploaded_at": datetime.now(timezone.utc),
            "status": "pending",
        }

        created_document = create_document(
            document_data
        )

        return created_document

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}",
        )


def verify_document(
    document_id: str,
) -> dict:

    document = get_document_by_id(
        document_id
    )

    if not document:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    file_path = Path(
        document["file_path"]
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uploaded file not found",
        )

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        text = file.read()

    aadhaar = extract_aadhaar(
        text
    )

    pan = extract_pan(
        text
    )

    aadhaar_valid = validate_aadhaar(
        aadhaar
    )

    pan_valid = validate_pan(
        pan
    )

    identity = find_identity(
        aadhaar,
        pan,
    )

    identity_verified = (
        identity is not None
    )

    risk_data = calculate_risk_score(
        aadhaar_valid,
        pan_valid,
        identity_verified,
    )

    return {
        "document_id": document_id,
        "aadhaar": aadhaar,
        "aadhaar_valid": aadhaar_valid,
        "pan": pan,
        "pan_valid": pan_valid,
        "identity_verified": identity_verified,
        "risk_score": risk_data["risk_score"],
        "risk_level": risk_data["risk_level"],
    }