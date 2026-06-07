from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DocumentNotFoundException,
)


async def document_not_found_handler(
    request: Request,
    exc: DocumentNotFoundException,
):

    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )