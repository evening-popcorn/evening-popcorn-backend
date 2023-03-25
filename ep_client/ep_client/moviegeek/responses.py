import uuid
from typing import List
from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    """
    Genre
    """
    id: int
    name: Optional[str]


class WatchProvider(BaseModel):
    """
    Watch provider
    """
    logo: Optional[str]
    provider_name: Optional[str]


class Cast(BaseModel):
    """
    Cast
    """
    profile: Optional[str]
    name: Optional[str]
    character: Optional[str]


class MovieInfo(BaseModel):
    """
    Movie info
    """
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
    """
    Info about movie in search result
    """
    id: int
    title: Optional[str]
    poster: Optional[str]
    original_title: Optional[str]
    release_date: Optional[str]


class MovieSearchResult(BaseModel):
    """
    Search result
    """
    page: int
    result: List[SearchMovieInfo]
    total_pages: int
