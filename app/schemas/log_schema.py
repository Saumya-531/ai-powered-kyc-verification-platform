from datetime import datetime

from pydantic import BaseModel


class LogResponseSchema(
    BaseModel
):

    endpoint: str

    method: str

    status_code: int

    timestamp: datetime