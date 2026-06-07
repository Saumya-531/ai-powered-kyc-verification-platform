from app.database import logs_collection


def create_log(log_data: dict):

    result = logs_collection.insert_one(
        log_data
    )

    return logs_collection.find_one(
        {
            "_id": result.inserted_id
        }
    )


def get_logs_by_user(
    user_id: str
):

    return list(
        logs_collection.find(
            {
                "user_id": user_id
            }
        )
    )