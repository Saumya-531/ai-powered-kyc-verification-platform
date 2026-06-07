from fastapi import (
    APIRouter,
    Depends,
)

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.dashboard_schema import (
    DashboardStatsSchema,
)

from app.services.dashboard_service import (
    fetch_dashboard_stats,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/stats",
    response_model=DashboardStatsSchema,
)
async def dashboard_stats(
    current_user: dict = Depends(
        get_current_user
    ),
):

    return fetch_dashboard_stats()