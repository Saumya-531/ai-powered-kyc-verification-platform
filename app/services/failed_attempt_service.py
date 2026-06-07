from datetime import datetime, timezone

from app.repositories.failed_attempt_repository import (
    create_failed_attempt,
    count_failed_attempts,
)


def record_failed_attempt(
    current_user: dict,
    reason: str,
):

    attempt_data = {
        "user_id":
            str(
                current_user["_id"]
            ),
        "reason":
            reason,
        "created_at":
            datetime.now(
                timezone.utc
            ),
    }

    return create_failed_attempt(
        attempt_data
    )


def get_failed_attempt_count(
    current_user: dict,
):

    return count_failed_attempts(
        str(
            current_user["_id"]
        )
    )