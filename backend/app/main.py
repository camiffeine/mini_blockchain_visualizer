from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routes import blockchain_router, transaction_router

app = FastAPI()

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
static_dir = frontend_dir / "static"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Hello World"}

app.include_router(blockchain_router.router)
app.include_router(transaction_router.router)