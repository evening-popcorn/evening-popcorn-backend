from typing import List
from typing import Optional

from pydantic import BaseModel


class BacklogStatus(BaseModel):
    """
    A pydantic model that represents a backlog status.
    """
    movie_id: int
    in_backlog: bool
    note: Optional[str]


class Backlog(BaseModel):
    """
    A pydantic model that represents a backlog.
    """
    page: int
    total_pages: int
    backlog: List[BacklogStatus]
