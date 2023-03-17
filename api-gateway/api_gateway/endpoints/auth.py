from fastapi import APIRouter
from fastapi import Depends

from api_gateway.controllers.common_obj.user import UserInfo
from api_gateway.depends.auth import auth_user
from api_gateway.repositories.dto.user import UserDto

router = APIRouter()


@router.get("/me")
def get_me(
    user: UserDto = Depends(auth_user),
) -> UserInfo:
    return UserInfo(
        id=str(user.id),
        name=user.name,
        email=user.email,
    )
