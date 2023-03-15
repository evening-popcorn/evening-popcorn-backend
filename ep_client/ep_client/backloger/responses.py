from typing import List

from pydantic.main import BaseModel


class BacklogEntry(BaseModel):
    movie_id: int
    note: str


class UserBacklog(BaseModel):
    page: int
    result: List[BacklogEntry]
    total_pages: int


class BacklogCheck(BaseModel):
    in_backlog: bool
    note: str | None
