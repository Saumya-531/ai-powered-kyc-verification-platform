from app.database import failed_attempts_collection


def create_failed_attempt(
    attempt_data: dict,
):

    result = failed_attempts_collection.insert_one(
        attempt_data
    )

    return failed_attempts_collection.find_one(
        {
            "_id":
                result.inserted_id
        }
    )


def count_failed_attempts(
    user_id: str,
):

    return failed_attempts_collection.count_documents(
        {
            "user_id":
                user_id
        }
    )