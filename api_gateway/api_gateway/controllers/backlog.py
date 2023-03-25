from typing import List
from typing import Optional
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from api_gateway.controllers.exceptions import MovieNotFound
from api_gateway.repositories.backlog import BacklogRepository
from api_gateway.repositories.movie import MoviesRepository


class UserBacklogEntry(BaseModel):
    id: int
    title: Optional[str]
    poster: Optional[str]
    original_title: Optional[str]
    release_date: Optional[str]
    backlog_note: Optional[str]


class UserBacklog(BaseModel):
    page: int
    total_pages: int
    backlog: List[UserBacklogEntry]


class BacklogController:

    def __init__(
        self,
        movies_repository: MoviesRepository = Depends(),
        backlog_repository: BacklogRepository = Depends()
    ) -> None:
        self.movies_repository = movies_repository
        self.backlog_repository = backlog_repository

    async def get_user_backlog(
        self,
        user_id: UUID,
        locale: str,
        page: int = 1
    ) -> UserBacklog:
        backlog = await self.backlog_repository.get_user_backlog(
            user_id=user_id, page=page)
        movie_ids = [entry.movie_id for entry in backlog.backlog]
        movies = await self.movies_repository.get_movies_info(
            movie_ids=movie_ids,
            locale=locale,
        )
        return UserBacklog(
            page=backlog.page,
            total_pages=backlog.total_pages,
            backlog=[
                UserBacklogEntry(
                    id=entry.movie_id,
                    title=movies[entry.movie_id].title,
                    poster=movies[entry.movie_id].poster,
                    original_title=movies[entry.movie_id].original_title,
                    release_date=movies[entry.movie_id].release_date,
                    backlog_note=entry.note,
                )
                for entry in backlog.backlog if entry.movie_id in movies
            ],
        )

    async def add_to_backlog(
        self,
        user_id: UUID,
        movie_id: int,
        note: str,
    ) -> bool:
        movie = await self.movies_repository.get_movie_info(movie_id=movie_id,
                                                            locale="en-US")
        if not movie:
            raise MovieNotFound()
        return await self.backlog_repository.add_to_backlog(
            user_id=user_id,
            movie_id=movie_id,
            note=note
        )

    async def delete_from_backlog(
        self,
        user_id: UUID,
        movie_id: int,
    ):
        return await self.backlog_repository.remove_from_backlog(
            user_id=user_id,
            movie_id=movie_id
        )
