from typing import List
from typing import Optional

from pydantic import BaseModel


class BacklogStatus(BaseModel):
    movie_id: int
    in_backlog: bool
    note: Optional[str]


class Backlog(BaseModel):
    page: int
    total_pages: int
    backlog: List[BacklogStatus]
