from fastapi import Depends
from fastapi import HTTPException

from src.repositories.auth import AuthRepository
from src.repositories.dto.user import UserDto
from src.repositories.exceptions import ObjectDoesNotFound
from src.repositories.user import UserRepository


class AuthController:
    """
    Controller for authentication and authorization
    """

    def __init__(
        self,
        auth_repository: AuthRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    async def auth_user(self, token: str) -> UserDto:
        """
        Authenticate user with X-Token
        """
        try:
            user = await self.auth_repository.find_token(token)
        except ObjectDoesNotFound:
            raise HTTPException(
                status_code=401, detail="Method requires authorization"
            )
        return user
