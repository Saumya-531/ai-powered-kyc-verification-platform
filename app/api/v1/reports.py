from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_user,
)

from app.repositories.report_repository import (
    get_reports_by_user,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/")
async def get_my_reports(
    current_user: dict = Depends(
        get_current_user
    ),
):

    reports = get_reports_by_user(
        str(
            current_user["_id"]
        )
    )

    for report in reports:

        report["_id"] = str(
            report["_id"]
        )

    return reports