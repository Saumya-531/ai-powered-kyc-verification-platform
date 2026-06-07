from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.report_schema import (
    VerificationReportSchema,
)

from app.services.document_service import (
    verify_document,
)

from app.services.report_service import (
    save_verification_report,
)

from app.services.log_service import (
    log_api_activity,
)

from app.services.failed_attempt_service import (
    record_failed_attempt,
    get_failed_attempt_count,
)

router = APIRouter(
    prefix="/verification",
    tags=["Verification"],
)


@router.get(
    "/{document_id}",
    response_model=VerificationReportSchema,
)
async def verify_document_endpoint(
    document_id: str,
    current_user: dict = Depends(
        get_current_user
    ),
):

    result = verify_document(
        document_id
    )

    if not result["identity_verified"]:

        record_failed_attempt(
            current_user,
            "Identity verification failed",
        )

    failed_attempts = (
        get_failed_attempt_count(
            current_user
        )
    )

    result["failed_attempts"] = (
        failed_attempts
    )

    save_verification_report(
        current_user,
        result,
    )

    log_api_activity(
        current_user,
        "/api/v1/verification",
        "GET",
        200,
    )

    return VerificationReportSchema(
        **result
    )