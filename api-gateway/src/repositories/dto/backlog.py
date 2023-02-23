from pydantic import BaseModel


class BacklogStatus(BaseModel):
    movie_id: int
    in_backlog: bool
