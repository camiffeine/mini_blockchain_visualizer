from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TransactionRequest(BaseModel):
    sender: str = Field(
        ...,
        description="The sender's address."
        )
    
    receiver: str = Field(
        ...,
        description="The recipient's address."
        )
    
    amount: float = Field(
        ...,
        gt=0,
        description="The amount to be transferred."
        )
    
    metadata: Optional[str] = Field(
        None,
        description="Optional metadata for the transaction."
        )

class TransactionResponse(BaseModel):
    sender: str = Field(
        ...,
        description="The sender's address."
        )
    
    receiver: str = Field(
        ...,
        description="The receiver's address."
        )
    
    amount: float = Field(
        ...,
        gt=0,
        description="The amount transferred."
        )
    
    metadata: Optional[str] = Field(
        None,
        description="Optional metadata for the transaction."
        )

    timestamp: datetime = Field(
        ...,
        description="The timestamp of the transaction."
        )
    
    hash: str = Field(
        ...,
        description="The hash of the transaction."
        )