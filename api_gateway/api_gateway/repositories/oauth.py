import uuid
from typing import Optional

from tortoise.exceptions import DoesNotExist

from api_gateway.models.user import OAuthClient
from api_gateway.repositories.dto.oauth import OAuthClientDto
from api_gateway.repositories.exceptions import ObjectDoesNotFound


class OAuthClientRepository:
    """
    OAuth clients repository
    """

    def __init__(self) -> None:
        self.model = OAuthClient

    async def create_oauth_client(
        self,
        *,
        id: Optional[uuid.uuid4] = None,
        user_id: uuid.uuid4,
        service: str,
        client_id: str,
    ):
        """
        Create new OAuth client
        """
        client = await self.model.create(
            id=id or uuid.uuid4(),
            user_id=user_id,
            service=service,
            client_id=client_id,
        )
        await client.save()
        await client.fetch_related('user')
        return OAuthClientDto(client)

    async def find_client_by_client_id(self, client_id: str):
        """
        Find client by client_id
        """
        try:
            client = await self.model \
                .get(client_id=client_id) \
                .prefetch_related("user")
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return OAuthClientDto(client)

    async def find_client_by_user_id(self, user_id: str) -> OAuthClientDto:
        """
        Find client by user_id
        """
        try:
            client = await self.model \
                .get(user_id=user_id) \
                .prefetch_related("user")
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return OAuthClientDto(client)
