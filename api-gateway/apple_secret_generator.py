from datetime import datetime

from authlib.jose import jwt

with open("AuthKey_T85Y536CMG.p8", "r") as f:
    private_key = f.read()
team_id = "BK9K9T323T"
client_id = "com.eveningPopcorn.eveningPopcorn"
key_id = "T85Y536CMG"
validity_minutes = 20
timestamp_now = datetime.now().timestamp()
timestamp_exp = timestamp_now + (60 * validity_minutes)
last_token_expiration = timestamp_exp
data = {
    "iss": team_id,
    "iat": timestamp_now,
    "exp": timestamp_exp,
    "aud": "https://appleid.apple.com",
    "sub": client_id
}
token = jwt.encode(payload=data, key=private_key,
                   header={"kid": key_id, "alg": "ES256"}).decode()
print(token)