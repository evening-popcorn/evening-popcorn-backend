from typing import Literal

from oauth2client import client

from src.config import APPLE_SIGN_IN_CONFIG


class SocialAuthController():

    def login(
        self,
        socialNetwork: Literal["apple", "google"],
        authCode: str
    ):
        match socialNetwork:
            case "apple":
                credentials = client.credentials_from_code(
                    client_id="239683451428-aa4dfoqsmkhmtoqtnqp3m4rfvjel4hk2.apps.googleusercontent.com",
                    client_secret='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',
                    scope=['profile', 'email'],
                    code=body.authCode,
                    redirect_uri="https://eveningpopcorn.dev/api/auth")
            case "google":
                credentials = client.credentials_from_code(
                    token_uri="https://appleid.apple.com/auth/token",
                    client_id=APPLE_SIGN_IN_CONFIG.client_id,
                    client_secret=APPLE_SIGN_IN_CONFIG.client_secret,
                    scope=['fullName', 'email'],
                    code=authCode,
                )
            case _:
                raise NotImplemented

        client_id = credentials.client_id
        user_obj = credentials.id_token

        print("Email:", user_obj["email"])
        print("Email verified:", user_obj['email_verified'])
        print("Name:", user_obj['name'])