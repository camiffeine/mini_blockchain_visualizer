from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from ..dependencies.app_state import get_blockchain_service
from ..services.blockchain_service import BlockchainService

router = APIRouter()

@router.get("/blockchain/blocks", tags=["Blockchain", "Block"])
async def create_block(
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Create a new block in the blockchain."
    ]
):
    new_block = blockchain_service.create_block()
    return new_block

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

@router.get("/blockchain", tags=["Blockchain"])
async def get_blockchain(
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Get the entire blockchain."
    ]
):
    blockchain_data = blockchain_service.get_blockchain()
    return blockchain_data

@router.get("/blockchain/blocks/{index}", tags=["Blockchain", "Block"])
async def get_block_by_index(
    index: int,
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Get a specific block by its index."
    ]
):
    block = blockchain_service.get_block(index)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Block with index {index} not found.")
    return block

@router.get("/blockchain/blocks/{block_index}/transactions/{transaction_index}/merkle-proof", tags=["Blockchain", "Block", "Merkle Tree"])
async def get_merkle_proof(
    block_index: int,
    transaction_index: int,
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Get the Merkle proof for a specific transaction in a block."
    ]
):
    proof_response = blockchain_service.get_merkle_proof(block_index, transaction_index)
    if proof_response is None:
        raise HTTPException(status_code=404, detail=f"Block with index {block_index} or transaction with index {transaction_index} not found.")
    return proof_response