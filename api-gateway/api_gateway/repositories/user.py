import uuid
from typing import Optional

from tortoise.exceptions import DoesNotExist

from api_gateway.models.user import Users
from api_gateway.repositories.dto.user import UserDto
from api_gateway.repositories.exceptions import ObjectDoesNotFound


class UserRepository:
    """
    Users repository
    """

    def __init__(self) -> None:
        self.model = Users

    async def create_user(
        self,
        *,
        id: Optional[uuid.uuid4] = None,
        email: str,
        name: str,
        password_hash: Optional[str] = None,
    ) -> UserDto:
        """
        Create new user in DB
        """
        user = await self.model.create(
            id=id or uuid.uuid4(),
            email=email,
            name=name,
            password_hash=password_hash,
        )
        await user.save()
        return UserDto(user)

    async def find_user_by_id(self, id: str) -> UserDto:
        """
        Find user by id
        """
        try:
            user = await self.model.get(id=id)
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return UserDto(user)

    async def find_user_by_email(self, email: str) -> UserDto:
        try:
            user = await self.model.get(email=email)
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return UserDto(user)
