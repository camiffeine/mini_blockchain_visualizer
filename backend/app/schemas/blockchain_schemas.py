from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BlockchainStatusResponse(BaseModel):
    blockchain_valid: bool = Field(
        ...,
        description="Indicates whether the blockchain is valid."
    )

    chain_length: int = Field(
        ...,
        description="The length of the blockchain."
    )

    last_block_index: Optional[int] = Field(
        None,
        description="The index of the last block in the blockchain. None if the blockchain is empty."
    )

    last_block_hash: str = Field(
        ...,
        description="The hash of the last block in the blockchain."
    )

    pending_transactions: list = Field(
        ...,
        description="A list of pending transactions that have not yet been included in a block."
    )

    message: Optional[str] = Field(
        None,
        description="An optional message providing additional information about the blockchain status."
    )