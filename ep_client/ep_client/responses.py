from pydantic.main import BaseModel


class SimpleResponse(BaseModel):
    success: bool
