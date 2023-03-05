import uuid
from typing import List
from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    name: Optional[str]


class WatchProvider(BaseModel):
    logo: Optional[str]
    provider_name: Optional[str]


class Cast(BaseModel):
    profile: Optional[str]
    name: Optional[str]
    character: Optional[str]


class MovieInfo(BaseModel):
    id: int
    title: Optional[str]
    original_title: Optional[str]
    poster: Optional[str]
    release_date: Optional[str]
    genre: List[Genre]
    length: int
    adult: bool
    providers: List[WatchProvider]
    overview: Optional[str]
    cast: List[Cast]


class SearchMovieInfo(BaseModel):
    id: int
    title: Optional[str]
    poster: Optional[str]
    original_title: Optional[str]
    release_date: Optional[str]


class MovieSearchResult(BaseModel):
    page: int
    result: List[SearchMovieInfo]
    total_pages: int
