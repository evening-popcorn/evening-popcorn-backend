from datetime import datetime
from datetime import timedelta
from typing import Tuple

from authlib.jose import jwt


def generate_apple_client_secret(
    private_key: str,
    team_id: str,
    client_id: str,
    key_id: str,
    expiration_delta: timedelta,
) -> Tuple[str, datetime]:
    timestamp_now = datetime.now()
    timestamp_exp = timestamp_now + expiration_delta
    data = {
        "iss": team_id,
        "iat": timestamp_now.timestamp(),
        "exp": timestamp_exp.timestamp(),
        "aud": "https://appleid.apple.com",
        "sub": client_id
    }
    token = jwt.encode(
        payload=data,
        key=private_key,
        header={"kid": key_id, "alg": "ES256"}
    ).decode()
    return token, timestamp_exp
