import asyncio
from typing import Dict
from typing import List

from fastapi import Depends

from ep_client.moviegeek.responses import MovieInfo
from ep_client.moviegeek.responses import MovieSearchResult
from ep_client.moviegeek.responses import SearchMovieInfo
from moviegeek.repositories.dto.tmdb import Movie
from moviegeek.repositories.tmdb import TMDBRepository
from moviegeek.utils import move_dto_to_movie_info


class MoviesController:
    """
    Controller for movies
    """

    def __init__(
        self,
        tmdb_repository: TMDBRepository = Depends()
    ) -> None:
        self.tmdb_repository = tmdb_repository

    async def get_movie(
        self,
        movie_id: int,
        locale: str
    ) -> MovieInfo:
        """
        Get movie info
        """
        movie = await self.tmdb_repository.get_movie(
            movie_id=movie_id,
            locale=locale,
        )
        return move_dto_to_movie_info(movie)

    async def _get_movie_safe(
        self,
        movie_id: int,
        locale: str
    ) -> Movie | None:
        """
        Get movie info
        """
        try:
            movie = await self.tmdb_repository.get_movie(
                movie_id=movie_id,
                locale=locale,
            )
        except RuntimeError:
            return None
        return movie

    async def get_movies(
        self,
        movie_ids: List[int], locale: str
    ) -> Dict[int, SearchMovieInfo]:
        """
        Get movies info
        """
        res = await asyncio.gather(
            *[
                self._get_movie_safe(movie_id=movie_id, locale=locale)
                for movie_id in movie_ids
            ]
        )
        return {
            movie.id: SearchMovieInfo(
                id=movie.id,
                title=movie.title,
                poster=movie.poster_path,
                original_title=movie.original_title,
                release_date=movie.release_date,
            )
            for movie in res if movie
        }

    async def search_movie(
        self,
        query: str,
        page: int,
        locale: str
    ) -> MovieSearchResult:
        """
        Search movie
        """
        res = await self.tmdb_repository.search_movie(
            query=query,
            page=page,
            locale=locale,
        )
        return MovieSearchResult(
            page=res.page,
            result=[
                SearchMovieInfo(
                    id=movie.id,
                    title=movie.title,
                    poster=movie.poster_path,
                    original_title=movie.original_title,
                    release_date=movie.release_date,
                ) for movie in res.results
            ],
            total_pages=res.total_pages
        )
