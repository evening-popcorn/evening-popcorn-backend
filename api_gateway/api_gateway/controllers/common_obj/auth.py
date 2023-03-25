from pydantic import BaseModel


class AuthToken(BaseModel):
    """
    A pydantic model that represents an authentication token.
    """
    token: str
    renew_token: str
    expiration: int
