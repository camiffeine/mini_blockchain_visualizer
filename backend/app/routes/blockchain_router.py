from fastapi import APIRouter, Depends, HTTPException

from ..dependencies.blockchain_dep import get_blockchain_service
from ..services.blockchain_service import BlockchainService

router = APIRouter()

@router.get("/blockchain/validate", tags=["Blockchain"])
async def validate_blockchain(
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    is_valid = blockchain_service.blockchain.validate_chain()
    return {"is_valid": is_valid}