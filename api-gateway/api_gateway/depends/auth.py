from fastapi import Depends
from fastapi import Header

from api_gateway.controllers.auth import AuthController
from api_gateway.repositories.dto.user import UserDto


async def auth_user(
    x_token: str = Header(),
    auth_controller: AuthController = Depends(),
) -> UserDto:
    """
    Auth user from X-Token header
    """
    user = await auth_controller.auth_user(x_token)
    return user
