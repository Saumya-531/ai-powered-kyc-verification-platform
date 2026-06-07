from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.document_schema import (
    UploadResponseSchema,
)

from app.services.document_service import (
    upload_document,
)

from app.services.log_service import (
    log_api_activity,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=UploadResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document_endpoint(
    file: UploadFile = File(...),
    current_user: dict = Depends(
        get_current_user
    ),
):

    document = upload_document(
        file,
        current_user,
    )

    log_api_activity(
        current_user,
        "/api/v1/documents/upload",
        "POST",
        201,
    )

    return UploadResponseSchema(
        message="Document uploaded successfully",
        document_id=str(
            document["_id"]
        ),
    )