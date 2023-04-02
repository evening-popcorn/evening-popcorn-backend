from pydantic.main import BaseModel


class SimpleResponse(BaseModel):
    """
    Simple response
    """
    success: bool
