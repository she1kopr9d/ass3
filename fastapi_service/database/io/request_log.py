import database.models
import database.core
import schemas


async def create_request_log(
    data: schemas.RequestLogCreate,
):
    async with database.core.async_session_factory() as session:
        request_log_obj: database.models.RequestLog = (
            database.models.RequestLog(**data.dict())
        )
        session.add(request_log_obj)
        await session.commit()
        await session.refresh(request_log_obj)
