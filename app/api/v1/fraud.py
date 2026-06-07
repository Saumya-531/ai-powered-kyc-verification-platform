from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_user,
)

from app.services.failed_attempt_service import (
    get_failed_attempt_count,
)

router = APIRouter(
    prefix="/fraud",
    tags=["Fraud Monitoring"],
)


@router.get("/attempts")
async def get_failed_attempts(
    current_user: dict = Depends(
        get_current_user
    ),
):

    return {
        "failed_attempts":
            get_failed_attempt_count(
                current_user
            )
    }