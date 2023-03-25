from pydantic import BaseModel


class SimpleResponse(BaseModel):
    """
    A pydantic model that represents a simple response.
    """
    success: bool
