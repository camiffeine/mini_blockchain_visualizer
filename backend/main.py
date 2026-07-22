import sys
from pathlib import Path

# Add the parent directory to the sys.path to allow imports from the core packagecl
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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