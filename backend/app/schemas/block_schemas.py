from .transaction_schemas import TransactionResponse
from .merkle_schemas import MerkleTreeResponse

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BlockResponse(BaseModel):
    index: int = Field(
        ...,
        description="The index of the block in the blockchain."
    )

    valid: bool = Field(
        ...,
        description="Indicates whether the block is valid."
    )

    timestamp: datetime = Field(
        ...,
        description="The timestamp when the block was created."
    )

    merkle_root: str = Field(
        ...,
        description="The Merkle root of the transactions included in the block."
    )

    nonce: int = Field(
        ...,
        description="The nonce used in the proof-of-work algorithm."
    )

    difficulty: int = Field(
        ...,
        description="The difficulty level of the proof-of-work algorithm."
    )

    hash: str = Field(
        ...,
        description="The hash of the current block."
    )

    previous_hash: str = Field(
            ...,
            description="The hash of the previous block in the blockchain."
        )

    transactions: Optional[List[TransactionResponse]] = Field(
        ...,
        description="A list of transactions included in the block."
    )

    merkle_tree: Optional[MerkleTreeResponse] = Field(
        None,
        description="The Merkle tree of the transactions included in the block."
    )

class BlockResponseWithoutMerkleTree(BaseModel):
    index: int = Field(
        ...,
        description="The index of the block in the blockchain."
    )

    valid: bool = Field(
            ...,
            description="Indicates whether the block is valid."
    )

    timestamp: datetime = Field(
        ...,
        description="The timestamp when the block was created."
    )

    merkle_root: str = Field(
        ...,
        description="The Merkle root of the transactions included in the block."
    )

    nonce: int = Field(
        ...,
        description="The nonce used in the proof-of-work algorithm."
    )

    difficulty: int = Field(
        ...,
        description="The difficulty level of the proof-of-work algorithm."
    )

    hash: str = Field(
        ...,
        description="The hash of the current block."
    )

    previous_hash: str = Field(
            ...,
            description="The hash of the previous block in the blockchain."
        )

    transactions: Optional[List[TransactionResponse]] = Field(
        ...,
        description="A list of transactions included in the block."
    )