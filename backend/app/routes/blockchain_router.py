from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from ..dependencies.app_state import get_blockchain_service
from ..services.blockchain_service import BlockchainService

router = APIRouter()

@router.get("/blockchain/validate", tags=["Blockchain"])
async def validate_blockchain(
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Validate the blockchain."
    ]
):
    is_valid = blockchain_service.blockchain.validate_chain()
    return {"blockchain_valid": is_valid}

@router.get("/blockchain/status", tags=["Blockchain"])
async def get_blockchain_status(
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Get the status of the blockchain."
    ]
):
    status = blockchain_service.get_status()
    return status