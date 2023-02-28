from datetime import datetime
from datetime import timedelta
from typing import Literal

from fastapi import Depends
from oauth2client import client as client
from oauth2client.client import FlowExchangeError
from pydantic import BaseModel
from tortoise.transactions import atomic

from api_gateway.config import APPLE_SIGN_IN_CONFIG
from api_gateway.config import GOOGLE_AUTH_CONFIG
from api_gateway.controllers.common_obj.auth import AuthToken
from api_gateway.controllers.common_obj.user import UserInfo
from api_gateway.repositories.auth import AuthRepository
from api_gateway.repositories.exceptions import ObjectDoesNotFound
from api_gateway.repositories.oauth import OAuthClientRepository
from api_gateway.repositories.user import UserRepository
from api_gateway.utils.rand_string import generate_random_string


class LoginResponse(BaseModel):
    is_new_user: bool
    user: UserInfo
    token: AuthToken


class InvalidCodeException(Exception):
    """
    Invalid code
    """

class EmailNotVerifiedException(Exception):
    """
    Email not verified
    """


class UserNotLinkedOAuthException(Exception):
    """
    This user not linked with this OAuth
    """


class SocialAuthController:
    def __init__(
        self,
        auth_repository: AuthRepository = Depends(),
        oauth_repository: OAuthClientRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.auth_repository = auth_repository
        self.oauth_repository = oauth_repository
        self.user_repository = user_repository

    @atomic()
    async def login(
        self,
        oauth_type: Literal["apple", "google"],
        auth_code: str,
    ) -> LoginResponse:
        try:
            match oauth_type:
                case "apple":
                    credentials = client.credentials_from_code(
                        token_uri="https://appleid.apple.com/auth/token",
                        client_id=APPLE_SIGN_IN_CONFIG.client_id,
                        client_secret=APPLE_SIGN_IN_CONFIG.client_secret,
                        scope=['name+email'],
                        code=auth_code,
                    )

                case "google":
                    credentials = client.credentials_from_code(
                        client_id=GOOGLE_AUTH_CONFIG.client_id,
                        client_secret=GOOGLE_AUTH_CONFIG.client_secret,
                        scope=['profile', 'email'],
                        code=auth_code,
                        redirect_uri=GOOGLE_AUTH_CONFIG.redirect_uri,
                    )
                case _:
                    raise NotImplemented
        except FlowExchangeError:
            raise InvalidCodeException
        client_id = credentials.client_id
        try:
            oauth_client = await self.oauth_repository.find_client_by_client_id(
                client_id
            )
            try:
                token = await self.auth_repository \
                    .find_token_by_user_id(user_id=oauth_client.user.id)
            except ObjectDoesNotFound:
                now = datetime.now()
                token = await  self.auth_repository.create_auth_token(
                    user_id=oauth_client.user.id,
                    token=generate_random_string(64),
                    renew_token=generate_random_string(64),
                    expiration=now + timedelta(days=30),
                    renew_expiration=now + timedelta(days=60),
                )
            return LoginResponse(
                is_new_user=False,
                user=UserInfo(
                    id=oauth_client.user.id,
                    email=oauth_client.user.email,
                    name=oauth_client.user.name
                ),
                token=AuthToken(
                    token=token.token,
                    renew_token=token.renew_token,
                    expiration=token.expiration.timestamp()
                )
            )
        except ObjectDoesNotFound:
            pass
        user_obj = credentials.id_token

        if not user_obj['email_verified']:
            raise EmailNotVerifiedException

        is_new_user = False
        try:
            user = await self.user_repository \
                .find_user_by_email(user_obj["email"])
        except ObjectDoesNotFound:
            is_new_user = True
            user = await self.user_repository.create_user(
                email=user_obj["email"],
                name=user_obj.get('name', user_obj["email"])
            )

        try:
            oauth_client = await self.oauth_repository\
                .find_client_by_user_id(
                    user_id=user.id
                )
            if oauth_client.client_id != client_id:
                raise UserNotLinkedOAuthException
        except ObjectDoesNotFound:
            if not is_new_user:
                raise UserNotLinkedOAuthException
            await self.oauth_repository.create_oauth_client(
                user_id=user.id,
                service=oauth_type,
                client_id=client_id
            )

        try:
            token = await self.auth_repository \
                .find_token_by_user_id(user_id=user.id)
        except ObjectDoesNotFound:
            now = datetime.now()
            token = await  self.auth_repository.create_auth_token(
                user_id=user.id,
                token=generate_random_string(64),
                renew_token=generate_random_string(64),
                expiration=now + timedelta(days=30),
                renew_expiration=now + timedelta(days=60),
            )

        return LoginResponse(
            is_new_user=is_new_user,
            user=UserInfo(
                id=user.id,
                email=user.email,
                name=user.name
            ),
            token=AuthToken(
                token=token.token,
                renew_token=token.renew_token,
                expiration=token.expiration.timestamp()
            )
        )
