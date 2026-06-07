from datetime import datetime, timezone

from app.repositories.log_repository import (
    create_log,
)


def log_api_activity(
    current_user: dict,
    endpoint: str,
    method: str,
    status_code: int,
):

    log_data = {
        "user_id": str(
            current_user["_id"]
        ),
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "timestamp": datetime.now(
            timezone.utc
        ),
    }

    return create_log(
        log_data
    )