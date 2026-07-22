from core.blockchain.blockchain import Blockchain
from fastapi import FastAPI

app = FastAPI()
blockchain = Blockchain()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/blockchain/validate")
async def validate_blockchain():
    is_valid = blockchain.validate_chain()
    return {"is_valid": is_valid}