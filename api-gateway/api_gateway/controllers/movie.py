import uuid
from typing import List
from typing import Optional

from fastapi import Depends
from pydantic import BaseModel

from api_gateway.repositories.backlog import BacklogRepository
from api_gateway.repositories.movie import MoviesRepository


class Genre(BaseModel):
    id: int
    name: str


class WatchProvider(BaseModel):
    logo: str
    provider_name: str


class Cast(BaseModel):
    profile: Optional[str]
    name: str
    character: str


class MovieInfo(BaseModel):
    id: int
    title: str
    original_title: str
    poster: str
    release_date: str
    genre: List[Genre]
    length: int
    adult: bool
    in_backlog: bool
    providers: List[WatchProvider]
    overview: str
    cast: List[Cast]


class MoviesController:

    def __init__(
        self,
        movies_repository: MoviesRepository = Depends(),
        backlog_repository: BacklogRepository = Depends()
    ) -> None:
        self.movies_repository = movies_repository
        self.backlog_repository = backlog_repository

    async def get_movie_info(
        self,
        movie_id: int,
        user_id: uuid.uuid4,
        locale: str,
    ) -> MovieInfo:
        movie_info = await self.movies_repository.get_movie_info(
            movie_id=movie_id,
            locale=locale
        )
        backlog_status = await self.backlog_repository.get_movie_status(
            movie_id=movie_id,
            user_id=user_id
        )
        return MovieInfo(
            id=movie_info.id,
            title=movie_info.title,
            original_title=movie_info.original_title,
            poster=movie_info.poster,
            release_date=movie_info.release_date,
            genre=[
                Genre(
                    id=genre.id,
                    name=genre.name
                )
                for genre in movie_info.genre
            ],
            length=movie_info.length,
            adult=movie_info.adult,
            in_backlog=backlog_status.in_backlog,
            providers=[
                WatchProvider(
                    logo=provider.logo,
                    provider_name=provider.provider_name
                )
                for provider in movie_info.providers
            ],
            overview=movie_info.overview,
            cast=[
                Cast(
                    profile=cast.profile,
                    name=cast.name,
                    character=cast.character
                )
                for cast in movie_info.cast
            ],
        )
