from fastapi import FastAPI

from .routes import blockchain_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(blockchain_router.router)