from ep_client.moviegeek.responses import Cast
from ep_client.moviegeek.responses import Genre
from ep_client.moviegeek.responses import MovieInfo
from ep_client.moviegeek.responses import WatchProvider
from moviegeek.repositories.dto.tmdb import Movie


def move_dto_to_movie_info(movie: Movie) -> MovieInfo:
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