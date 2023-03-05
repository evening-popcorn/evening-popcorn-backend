from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class WatchProvider(BaseModel):
    display_priority: Optional[int] = None
    logo_path: Optional[str] = None
    provider_id: Optional[int] = None
    provider_name: Optional[str] = None


class Genre(BaseModel):
    id: int
    name: str


class ProductionCompany(BaseModel):
    id: int
    logo_path: Optional[str]
    name: str
    origin_country: str


class ProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class SpokenLanguage(BaseModel):
    iso_639_1: str
    name: str


class CastItem(BaseModel):
    adult: bool
    gender: int
    id: int
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: Optional[str]
    cast_id: int
    character: str
    credit_id: str
    order: int


class CrewItem(BaseModel):
    adult: bool
    gender: int
    id: int
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: Optional[str]
    credit_id: str
    department: str
    job: str


class Credits(BaseModel):
    id: Optional[int] = None
    cast: Optional[List[CastItem]] = None
    crew: Optional[List[CrewItem]] = None


class Movie(BaseModel):
    adult: Optional[bool] = None
    backdrop_path: Optional[str] = None
    budget: Optional[int] = None
    genres: Optional[List[Genre]] = None
    homepage: Optional[str] = None
    id: Optional[int] = None
    imdb_id: Optional[str] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    production_companies: Optional[List[ProductionCompany]] = None
    production_countries: Optional[List[ProductionCountry]] = None
    release_date: Optional[str] = None
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    spoken_languages: Optional[List[SpokenLanguage]] = None
    status: Optional[str] = None
    tagline: Optional[str] = None
    title: Optional[str] = None
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

    watch_providers: Optional[List[WatchProvider]] = None
    credits: Optional[Credits] = None


class Result(BaseModel):
    adult: Optional[bool]
    backdrop_path: Optional[str]
    genre_ids: Optional[List[int]]
    id: Optional[int]
    original_language: Optional[str]
    original_title: Optional[str]
    overview: Optional[str]
    popularity: Optional[float]
    poster_path: Optional[str]
    release_date: Optional[str]
    title: Optional[str]
    video: Optional[bool]
    vote_average: Optional[float]
    vote_count: Optional[int]


class MovieSearchResult(BaseModel):
    page: Optional[int] = None
    results: Optional[List[Result]] = None
    total_pages: Optional[int] = None
    total_results: Optional[int] = None
