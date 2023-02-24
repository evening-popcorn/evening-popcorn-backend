import os
from datetime import datetime
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
from ep_utils.config_model import ConfigModel
from pydantic import PrivateAttr

from src.utils.apple_secret_generator import generate_apple_client_secret

load_dotenv()


class PostgresConfig(ConfigModel):
    user: str
    pwd: str
    host: str
    port: int = 5432
    db_name: str = ""
    ssl: bool = False

    def get_connection_url(self):
        string = f"postgres://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db_name}"
        if self.ssl:
            string += "?sslmode=require"
        return string


POSTGRES_CONFIG = PostgresConfig()
TORTOISE_ORM = {
    "connections": {"default": POSTGRES_CONFIG.get_connection_url()},
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class AppleSighInConfig(ConfigModel):
    client_id: str
    team_id: str

    key_id: str
    secret_cert: str

    _secret_cache: Optional[str] = PrivateAttr()
    _secret_expiration: Optional[datetime] = PrivateAttr()

    def __init__(self) -> None:
        super().__init__()
        self._secret_cache = None
        self._secret_expiration = None

    @property
    def client_secret(self):
        now = datetime.now()
        if self._secret_cache and self._secret_expiration < now:
            return self._secret_cache
        token, expiration = generate_apple_client_secret(
            private_key=self.secret_cert,
            team_id=self.team_id,
            client_id=self.client_id,
            key_id=self.key_id,
            expiration_delta=timedelta(hours=24)
        )
        self._secret_cache = token
        self._secret_expiration = expiration
        return self._secret_cache


APPLE_SIGN_IN_CONFIG = AppleSighInConfig()


class GoogleAuthConfig(ConfigModel):
    client_id: str
    client_secret: str
    redirect_uri: str = "https://eveningpopcorn.dev/api/auth"


GOOGLE_AUTH_CONFIG = GoogleAuthConfig()

if __name__ == "__main__":
    configs = [
        PostgresConfig.get_fields_defaults(),
        AppleSighInConfig.get_fields_defaults(),
        GoogleAuthConfig.get_fields_defaults(),
    ]

    if os.path.exists("../.env"):
        os.remove("../.env")
    with open("../.env", "w") as file:
        for config in configs:
            file.writelines([f"{k}={v}\n" for k, v in config.items()])
            file.write("\n")
