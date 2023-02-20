from datetime import datetime

from pydantic import BaseModel

from src.models.auth import AuthTokens


class AuthTokenDto(BaseModel):
    """
    Auth token DTO
    """
    token: str
    renew_token: str
    expiration: datetime

    def __init__(self, model: AuthTokens):
        super(AuthTokenDto, self).__init__(
            token=model.token,
            renew_token=self.renew_token,
            expiration=self.expiration
        )
