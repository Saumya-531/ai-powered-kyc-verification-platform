from bson import ObjectId

from app.database import reports_collection


def create_report(
    report_data: dict,
):

    result = reports_collection.insert_one(
        report_data
    )

    return reports_collection.find_one(
        {
            "_id":
                result.inserted_id
        }
    )


def get_reports_by_user(
    user_id: str,
):

    return list(
        reports_collection.find(
            {
                "user_id":
                    user_id
            }
        )
    )


def get_report_by_id(
    report_id: str,
):

    try:

        object_id = ObjectId(
            report_id
        )

    except Exception:

        return None

    return reports_collection.find_one(
        {
            "_id":
                object_id
        }
    )