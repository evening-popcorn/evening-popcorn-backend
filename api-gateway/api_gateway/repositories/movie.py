from ep_client.moviegeek.client import MovieGeekClient
from ep_client.moviegeek.responses import MovieInfo
from fastapi import Depends


class MoviesRepository:
    def __init__(self, moviegeek_client: MovieGeekClient = Depends()) -> None:
        self.moviegeek_client = moviegeek_client

    async def get_movie_info(self, movie_id: int, locale: str) -> MovieInfo:
        return await self.moviegeek_client.get_movie(movie_id=movie_id,
                                                     locale=locale)
