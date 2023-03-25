from typing import Any
from typing import Optional

from pydantic import BaseModel

from api_gateway.models.user import OAuthClient
from api_gateway.repositories.dto.user import UserDto


class OAuthClientDto(BaseModel):
    """
    A pydantic model that represents an OAuth client.
    """
    id: str
    user: Optional[UserDto]
    service: str
    client_id: str

    def __init__(self, model: OAuthClient) -> None:
        super().__init__(
            id=str(model.id),
            user=UserDto(model.user) if model.user else None,
            service=model.service,
            client_id=model.client_id
        )