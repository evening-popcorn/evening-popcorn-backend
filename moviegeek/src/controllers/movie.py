from fastapi import Depends

from src.repositories.tmdb import TMDBRepository


class MoviesController:

    def __init__(
        self,
        tmdb_repository: TMDBRepository = Depends()
    ) -> None:
        self.tmdb_repository = tmdb_repository

    async def get_movie(
        self,
        movie_id: int,
        locale: str
    ):
        return await self.tmdb_repository.get_movie(movie_id=movie_id,
                                                    locale=locale)
