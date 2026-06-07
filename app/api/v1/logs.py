from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_current_user,
)

from app.repositories.log_repository import (
    get_logs_by_user,
)

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.get("/")
async def get_my_logs(
    current_user: dict = Depends(
        get_current_user
    ),
):

    logs = get_logs_by_user(
        str(
            current_user["_id"]
        )
    )

    for log in logs:

        log["_id"] = str(
            log["_id"]
        )

    return logs