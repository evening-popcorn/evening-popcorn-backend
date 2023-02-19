import uvicorn
from fastapi import Body
from fastapi import FastAPI
from oauth2client import client
from pydantic import BaseModel

app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "This is new API"}

class GoogleAuthBody(BaseModel):
    authCode: str

@app.post("/api/google-auth")
async def google_auth(body:GoogleAuthBody = Body()):
    credentials = client.credentials_from_code(
        client_id="239683451428-aa4dfoqsmkhmtoqtnqp3m4rfvjel4hk2.apps.googleusercontent.com",
        client_secret='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',
        scope=['profile','email'],
        code=body.authCode,
        redirect_uri="https://eveningpopcorn.dev/api/auth"   )
    client_id = credentials.client_id
    user_obj = credentials.id_token

    print("Email:", user_obj["email"])
    print("Email verified:", user_obj['email_verified'])
    print("Name:", user_obj['name'])

@app.post("/api/apple-auth")
async def google_auth(body:GoogleAuthBody = Body()):
    credentials = client.credentials_from_code(
        token_uri="https://appleid.apple.com/auth/token",
        client_id="com.eveningPopcorn.eveningPopcorn",
        client_secret='eyJraWQiOiJUODVZNTM2Q01HIiwiYWxnIjoiRVMyNTYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJCSzlLOVQzMjNUIiwiaWF0IjoxNjc2ODMxNDI0LjQ0MzcyNiwiZXhwIjoxNjc2ODMyNjI0LjQ0MzcyNiwiYXVkIjoiaHR0cHM6Ly9hcHBsZWlkLmFwcGxlLmNvbSIsInN1YiI6ImNvbS5ldmVuaW5nUG9wY29ybi5ldmVuaW5nUG9wY29ybiJ9.Lp7bD6eMYSEFc7Q2WD8qi96uh6SaDmtDGSyAsJfOsGlTf6hNhXwmMQ96RgWDDOJnweK0nM46eUyPTphj5oYs3g',
        scope=['profile','email'],
        code=body.authCode,   )
    client_id = credentials.client_id
    user_obj = credentials.id_token

    print("Email:", user_obj["email"])
    print("Email verified:", user_obj['email_verified'])
    # print("Name:", user_obj['name'])


@app.post("/api/service/apple-user-update")
async def google_auth(body:GoogleAuthBody = Body()):
    pass



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
