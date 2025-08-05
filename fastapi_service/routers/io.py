import os
import uuid
import fastapi
import fastapi.responses
import faststream.rabbit.fastapi

import config
import schemas


router = faststream.rabbit.fastapi.RabbitRouter(
    url=config.settings.rabbitmq_url
)

UPLOAD_FOLDER = "uploads"


@router.subscriber("add_file")
async def add_file_handler(
    data: schemas.UploadFileData,
):
    file_bytes = data.filebytes.encode("latin1")
    folder_path = "uploads/"
    os.makedirs(folder_path, exist_ok=True)
    generated_name = f"{uuid.uuid4().hex}.{data.extension}"
    full_path = os.path.join(folder_path, generated_name)

    with open(full_path, "wb") as f:
        f.write(file_bytes)
    await router.broker.publish(
        {
            "link": (
                f"http://{config.settings.IP_ADDRESS}:{config.settings.PORT}"
                f"/uploads/{generated_name}"
            ),
            "user_id": data.user_id,
        },
        queue="add_file_answer",
    )


@router.get("/uploads/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise fastapi.HTTPException(status_code=404, detail="Файл не найден")

    return fastapi.responses.FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
