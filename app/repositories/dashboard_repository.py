from app.database import (
    users_collection,
    documents_collection,
    reports_collection,
    logs_collection,
    failed_attempts_collection,
)


def get_dashboard_stats():

    return {
        "total_users":
            users_collection.count_documents({}),

        "total_documents":
            documents_collection.count_documents({}),

        "total_reports":
            reports_collection.count_documents({}),

        "total_logs":
            logs_collection.count_documents({}),

        "total_failed_attempts":
            failed_attempts_collection.count_documents({}),

        "high_risk_cases":
            reports_collection.count_documents(
                {
                    "risk_level": "High"
                }
            ),
    }