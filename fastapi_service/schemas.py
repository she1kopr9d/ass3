import pydantic


class UploadFileData(pydantic.BaseModel):
    user_id: int
    extension: str
    filebytes: str
