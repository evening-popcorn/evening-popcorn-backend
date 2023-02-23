from pydantic import BaseModel


class AuthToken(BaseModel):
    token: str
    renew_token: str
    expiration: int
