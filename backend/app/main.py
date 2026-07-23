from fastapi import FastAPI

from .routes import blockchain_router, transaction_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(blockchain_router.router)
app.include_router(transaction_router.router)