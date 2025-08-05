import pydantic
import typing


class UploadFileData(pydantic.BaseModel):
    user_id: int
    extension: str
    filebytes: str


class RequestLogCreate(pydantic.BaseModel):
    path: str = pydantic.Field(..., max_length=255)
    ip_address: str = pydantic.Field(..., max_length=45)
    user_agent: typing.Optional[str] = None
    accept_language: typing.Optional[str] = (
        pydantic.Field(default=None, max_length=255)
    )
    status_code: typing.Optional[int] = None
    response_time_ms: typing.Optional[int] = None
