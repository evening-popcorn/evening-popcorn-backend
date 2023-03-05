from fastapi import Depends

from ep_client.moviegeek.responses import Cast
from ep_client.moviegeek.responses import Genre
from ep_client.moviegeek.responses import MovieInfo
from ep_client.moviegeek.responses import MovieSearchResult
from ep_client.moviegeek.responses import SearchMovieInfo
from ep_client.moviegeek.responses import WatchProvider
from moviegeek.repositories.tmdb import TMDBRepository


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
    ) -> MovieInfo:
        movie = await self.tmdb_repository.get_movie(
            movie_id=movie_id,
            locale=locale,
        )
        return MovieInfo(
            id=movie.id,
            title=movie.title,
            original_title=movie.original_title,
            poster=movie.poster_path,
            release_date=movie.release_date,
            genre=[
                Genre(
                    id=genre.id,
                    name=genre.name
                )
                for genre in movie.genres
            ],
            length=movie.runtime,
            adult=movie.adult,
            providers=[
                WatchProvider(
                    logo=wp.logo_path,
                    provider_name=wp.provider_name,
                )
                for wp in movie.watch_providers
            ],
            overview=movie.overview,
            cast=[
                Cast(
                    profile=cast.profile_path,
                    name=cast.name,
                    character=cast.character,
                )
                for cast in movie.credits.cast
            ],
        )

    async def search_movie(
        self,
        query: str,
        page: int,
        locale: str
    ) -> MovieSearchResult:
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
