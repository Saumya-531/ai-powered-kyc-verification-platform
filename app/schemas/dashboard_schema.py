from pydantic import BaseModel


class DashboardStatsSchema(
    BaseModel
):

    total_users: int

    total_documents: int

    total_reports: int

    total_logs: int

    total_failed_attempts: int

    high_risk_cases: int