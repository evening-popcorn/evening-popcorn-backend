import uuid
from datetime import datetime
from typing import Optional

from tortoise.exceptions import DoesNotExist

from src.models.auth import AuthTokens
from src.repositories.dto.auth import AuthTokenDto
from src.repositories.dto.user import UserDto
from src.repositories.exceptions import ObjectDoesNotFound


class AuthRepository:
    """
    Repository to work with users tokens
    """

    def __init__(self) -> None:
        self.model = AuthTokens

    async def create_auth_token(
        self,
        *,
        id: Optional[uuid.uuid4] = None,
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
            id=id or uuid.uuid4(),
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
        return UserDto(token.user)

    async def find_token_by_user_id(self, user_id: uuid.uuid4) -> AuthTokenDto:
        """
        Find user by token
        """
        token = await self.model.filter(
            user_id=user_id,
            expiration__gt=datetime.now()
        ).first()
        if token is None:
            raise ObjectDoesNotFound()
        return AuthTokenDto(token)
