import os
import uuid
import time
import fastapi
import fastapi.responses
import faststream.rabbit.fastapi

import config
import schemas
import database.io.request_log


router = faststream.rabbit.fastapi.RabbitRouter(
    url=config.settings.rabbitmq_url
)

UPLOAD_FOLDER = "uploads"


def get_real_ip(request: fastapi.Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host


@router.subscriber("add_file")
async def add_file_handler(
    data: schemas.UploadFileData,
):
    file_bytes = data.filebytes.encode("latin1")
    folder_path = "uploads/"
    os.makedirs(folder_path, exist_ok=True)
    generated_name = f"{uuid.uuid4().hex}{data.extension}"
    full_path = os.path.join(folder_path, generated_name)

    with open(full_path, "wb") as f:
        f.write(file_bytes)
    link = ""
    if config.settings.PORT == 80:
        link = (
            f"http://{config.settings.IP_ADDRESS}"
            f"/uploads/{generated_name}"
        )
    else:
        link = (
            f"http://{config.settings.IP_ADDRESS}:{config.settings.PORT}"
            f"/uploads/{generated_name}"
        )

    await router.broker.publish(
        {
            "link": link,
            "user_id": data.user_id,
        },
        queue="add_file_answer",
    )


@router.get("/uploads/{filename}")
async def download_file(
    filename: str,
    request: fastapi.Request,
):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    start_time = time.time()
    ip_address = get_real_ip(request)
    if not os.path.exists(file_path):
        log = schemas.RequestLogCreate(
            path=str(request.url.path),
            ip_address=ip_address,
            user_agent=request.headers.get("user-agent"),
            accept_language=request.headers.get("accept-language"),
            status_code=404,
            response_time_ms=int((time.time() - start_time) * 1000)
        )
        await database.io.request_log.create_request_log(log)
        raise fastapi.HTTPException(status_code=404, detail="Файл не найден")
    log = schemas.RequestLogCreate(
        path=str(request.url.path),
        ip_address=ip_address,
        user_agent=request.headers.get("user-agent"),
        accept_language=request.headers.get("accept-language"),
        status_code=200,
        response_time_ms=int((time.time() - start_time) * 1000)
    )
    await database.io.request_log.create_request_log(log)
    return fastapi.responses.FileResponse(
        path=file_path,
        filename=safe_filename,
        media_type="application/octet-stream"
    )
