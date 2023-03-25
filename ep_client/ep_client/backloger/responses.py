from typing import List

from pydantic.main import BaseModel


class BacklogEntry(BaseModel):
    """
    Backlog entry
    """
    movie_id: int
    note: str


class UserBacklog(BaseModel):
    """
    User backlog
    """
    page: int
    result: List[BacklogEntry]
    total_pages: int


class BacklogCheck(BaseModel):
    """
    Backlog check
    """
    in_backlog: bool
    note: str | None
