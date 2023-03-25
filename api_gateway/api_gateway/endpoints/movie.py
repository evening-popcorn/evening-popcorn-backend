from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import Query

from api_gateway.controllers.movie import MovieInfo
from api_gateway.controllers.movie import MovieSearchResult
from api_gateway.controllers.movie import MoviesController
from api_gateway.depends.auth import auth_user
from api_gateway.repositories.dto.user import UserDto

router = APIRouter()


@router.get("/search")
async def search_movie(
    q: str = Query(min_length=3),
    page: int = Query(ge=1, default=1),
    user: UserDto = Depends(auth_user),
    movie_controller: MoviesController = Depends(),
    x_language: str = Header(default="RU")
) -> MovieSearchResult:
    """
    Search movie by query
    """
    return await movie_controller.search_movie(
        query=q,
        page=page,
        user_id=user.id,
        locale=x_language,
    )


@router.get("/{movie_id}")
async def get_movie_info(
    movie_id: int,
    user: UserDto = Depends(auth_user),
    movie_controller: MoviesController = Depends(),
    x_language: str = Header(default="RU")
) -> MovieInfo:
    """
    Get movie info by id
    """
    return await movie_controller.get_movie_info(
        movie_id=movie_id,
        user_id=user.id,
        locale=x_language,
    )
