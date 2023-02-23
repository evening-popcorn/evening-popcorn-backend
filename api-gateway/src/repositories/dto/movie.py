from typing import List

from pydantic import BaseModel


class GenreDto(BaseModel):
    id: int
    name: str


class WatchProviderDto(BaseModel):
    logo: str
    provider_name: str


class CastDto(BaseModel):
    profile: str
    name: str
    character: str


class MovieInfoDto(BaseModel):
    id: int
    title: str
    original_title: str
    poster: str
    release_date: str
    genre: List[GenreDto]
    length: int
    adult: bool
    providers: List[WatchProviderDto]
    overview: str
    cast: List[CastDto]
