from fastapi import Depends

from backloger.repository import BacklogRepository


class BacklogController:
    def __init__(
        self, backlog_repository: BacklogRepository = Depends()
    ) -> None:
        self.backlog_repository = backlog_repository
