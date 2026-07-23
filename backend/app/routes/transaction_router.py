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