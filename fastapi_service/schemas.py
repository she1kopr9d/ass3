import pydantic


class UploadFileData(pydantic.BaseModel):
    user_id: int
    filebytes: str
