from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    A pydantic model that represents a user's information.
    """
    id: str
    email: str
    name: str

