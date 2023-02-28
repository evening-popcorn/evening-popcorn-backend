from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header

from api_gateway.controllers.movie import MoviesController
from api_gateway.depends.auth import auth_user
from api_gateway.repositories.dto.user import UserDto

router = APIRouter()


@router.get("/{movie_id}")
async def get_movie_info(
    movie_id: int,
    user: UserDto = Depends(auth_user),
    movie_controller: MoviesController = Depends(),
    x_language: str = Header(default="RU")
):
    return await movie_controller.get_movie_info(
        movie_id=movie_id,
        user_id=user.id,
        locale=x_language,
    )
