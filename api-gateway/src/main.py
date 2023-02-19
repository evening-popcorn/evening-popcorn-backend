import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "This is new API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
