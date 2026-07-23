from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from backend.app.schemas.transaction_schemas import TransactionRequest

from ..dependencies.app_state import get_blockchain_service
from ..services.blockchain_service import BlockchainService
from ..schemas.transaction_schemas import TransactionRequest, TransactionResponse

router = APIRouter()

@router.post("/transactions/add", tags=["Transaction"], status_code=201)
async def add_transaction(
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Add a new transaction to the blockchain."
    ],
    transaction: Annotated[
        TransactionRequest,
        "The transaction data to be added."
    ]):
    new_transaction = blockchain_service.add_transaction(transaction)
    return new_transaction

@router.post("/transactions/tamper", tags=["Transaction"], status_code=200)
async def tamper_transaction(
    blockchain_service: Annotated[
        BlockchainService,
        Depends(get_blockchain_service),
        "Tamper with a specific transaction in the blockchain."
    ],
    block_index: int,
    transaction_index: int,
    new_transaction: Annotated[
        TransactionRequest,
        "The new transaction data to replace the existing one."
    ]):
    try:
        blockchain_service.tamper_transaction(block_index, transaction_index, new_transaction)
        return {"message": f"Transaction at index {transaction_index} in block {block_index} has been tampered."}
    except IndexError as e:
        raise HTTPException(status_code=400, detail=str(e))