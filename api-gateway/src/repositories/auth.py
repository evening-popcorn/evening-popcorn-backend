import uuid
from datetime import datetime

from tortoise.exceptions import DoesNotExist

from src.models.auth import AuthTokens
from src.repositories.dto.auth import AuthTokenDto
from src.repositories.exceptions import ObjectDoesNotFound


class AuthRepository:
    """
    Repository to work with users tokens
    """

    def __init__(self) -> None:
        self.model = AuthTokens

    async def create_auth_token(
        self,
        id: uuid.uuid4,
        user_id: uuid.uuid4,
        token: str,
        renew_token: str,
        expiration: datetime,
        renew_expiration: datetime,
    ) -> AuthTokenDto:
        """
        Create new token
        :return:
        """
        token = await self.model.create(
            id=id,
            user_id=user_id,
            token=token,
            renew_token=renew_token,
            expiration=expiration,
            renew_expiration=renew_expiration,
        )
        return AuthTokenDto(token)

    async def find_token(self, token: str) -> UserDto:
        """
        Find user by token
        """
        try:
            token = await self.model.get(token=token).prefetch_related("user")
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return token.user.get_dto()
