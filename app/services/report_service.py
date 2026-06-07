from datetime import datetime, timezone

from app.repositories.report_repository import (
    create_report,
)


def save_verification_report(
    current_user: dict,
    verification_data: dict,
) -> dict:

    report_data = {
        "user_id": str(
            current_user["_id"]
        ),
        "document_id":
            verification_data[
                "document_id"
            ],
        "aadhaar":
            verification_data[
                "aadhaar"
            ],
        "pan":
            verification_data[
                "pan"
            ],
        "identity_verified":
            verification_data[
                "identity_verified"
            ],
        "risk_score":
            verification_data[
                "risk_score"
            ],
        "risk_level":
            verification_data[
                "risk_level"
            ],
        "created_at":
            datetime.now(
                timezone.utc
            ),
    }

    return create_report(
        report_data
    )