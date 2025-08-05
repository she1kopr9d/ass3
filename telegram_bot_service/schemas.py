import pydantic


class LinkData(pydantic.BaseModel):
    user_id: int
    link: str
