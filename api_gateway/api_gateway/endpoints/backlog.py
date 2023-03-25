from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Header
from fastapi import Query

from api_gateway.controllers.backlog import BacklogController
from api_gateway.controllers.backlog import UserBacklog
from api_gateway.controllers.common_obj.simple_response import SimpleResponse
from api_gateway.controllers.exceptions import MovieNotFound
from api_gateway.depends.auth import auth_user
from api_gateway.repositories.dto.user import UserDto

router = APIRouter()


@router.get("/")
async def get_my_backlog(
    page: int = Query(ge=1, default=1),
    user: UserDto = Depends(auth_user),
    x_language: str = Header(default="RU"),
    backlog_controller: BacklogController = Depends()
) -> UserBacklog:
    """
    Get user's backlog
    """
    return await backlog_controller.get_user_backlog(user_id=user.id,
                                                     locale=x_language,
                                                     page=page)


@router.post("/")
async def add_to_backlog(
    movie_id: int = Body(),
    note: str = Body(default="", max_length=280),
    user: UserDto = Depends(auth_user),
    backlog_controller: BacklogController = Depends()
) -> SimpleResponse:
    """
    Add movie to user's backlog
    """
    try:
        res = await backlog_controller.add_to_backlog(
            user_id=user.id,
            movie_id=movie_id,
            note=note
        )
    except MovieNotFound:
        raise HTTPException(status_code=404, detail="Movie not found")
    return SimpleResponse(
        success=res,
    )


@router.delete("/")
async def delete_from_backlog(
    movie_id: int = Query(),
    user: UserDto = Depends(auth_user),
    backlog_controller: BacklogController = Depends()
) -> SimpleResponse:
    """
    Delete movie from user's backlog
    """
    res = await backlog_controller.delete_from_backlog(
        user_id=user.id,
        movie_id=movie_id,
    )
    return SimpleResponse(
        success=res,
    )
