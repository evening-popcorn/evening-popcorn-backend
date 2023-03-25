from pydantic import BaseModel


class SimpleResponse(BaseModel):
    success: bool
