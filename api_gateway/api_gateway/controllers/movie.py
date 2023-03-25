import uuid
from typing import List
from typing import Optional

from fastapi import Depends
from pydantic import BaseModel

from api_gateway.repositories.backlog import BacklogRepository
from api_gateway.repositories.movie import MoviesRepository


class Genre(BaseModel):
    """
    A pydantic model that represents a movie genre.
    """
    id: int
    name: str


class WatchProvider(BaseModel):
    """
    A pydantic model that represents a movie watch provider.
    """
    logo: str
    provider_name: str


class Cast(BaseModel):
    """
    A pydantic model that represents a movie cast member.
    """
    profile: Optional[str]
    name: str
    character: str


class MovieInfo(BaseModel):
    """
    A pydantic model that represents a movie's information.
    """
    id: int
    title: str
    original_title: str
    poster: str
    release_date: str
    genre: List[Genre]
    length: int
    adult: bool
    in_backlog: bool
    backlog_note: str
    providers: List[WatchProvider]
    overview: str
    cast: List[Cast]


class SearchMovieInfo(BaseModel):
    """
    A pydantic model that represents a movie's information.
    """
    id: int
    title: Optional[str]
    poster: Optional[str]
    original_title: Optional[str]
    release_date: Optional[str]
    in_backlog: bool
    backlog_note: Optional[str]


class MovieSearchResult(BaseModel):
    """
    A pydantic model that represents a movie search result.
    """
    page: int
    result: List[SearchMovieInfo]
    total_pages: int


class MoviesController:
    """
    Controller for the movie information.
    """

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
        """
        Get the movie information.
        """
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
            backlog_note=backlog_status.note,
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

    async def search_movie(
        self, query: str,
        page: int,
        user_id: uuid.uuid4,
        locale: str,
    ) -> MovieSearchResult:
        """
        Search for a movie.
        """
        search_res = await self.movies_repository.search_movie(
            q=query,
            page=page,
            locale=locale
        )
        statuses = await self.backlog_repository.bulk_get_movie_status(
            user_id=user_id,
            movie_ids=list(map(lambda movie: movie.id, search_res.result))
        )
        return MovieSearchResult(
            page=search_res.page,
            result=[
                SearchMovieInfo(
                    id=movie.id,
                    title=movie.title,
                    poster=movie.poster,
                    original_title=movie.original_title,
                    release_date=movie.release_date,
                    in_backlog=statuses[movie.id].in_backlog,
                    backlog_note=statuses[movie.id].note
                )
                for movie in search_res.result
            ],
            total_pages=search_res.total_pages,
        )
