from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProofStepResponse(BaseModel):
    hash: str = Field(
        ...,
        description="The hash of the proof step."
    )

    direction: str = Field(
        ...,
        description="The direction of the proof step (left or right)."
    )

class MerkleProofResponse(BaseModel):
    transaction_hash: str = Field(
        ...,
        description="The hash of the transaction for which the proof is generated."
    )

    merkle_root: str = Field(
        ...,
        description="The Merkle root of the tree."
    )

    proof_steps: List[ProofStepResponse] = Field(
        ...,
        description="A list of proof steps from the leaf to the root."
    )

class MerkleProofVerificationResponse(BaseModel):
    proof: MerkleProofResponse = Field(
        ...,
        description="The Merkle proof that was verified."
    )
    valid: bool = Field(
        ...,
        description="Indicates whether the proof is valid."
    )

class MerkleNodeResponse(BaseModel):
    hash: str = Field(
        ...,
        description="The hash of the Merkle node."
    )

    left: Optional["MerkleNodeResponse"] = Field(
        None,
        description="The left child of the Merkle node."
    )

    right: Optional["MerkleNodeResponse"] = Field(
        None,
        description="The right child of the Merkle node."
    )

class MerkleTreeResponse(BaseModel):
    root: Optional["MerkleNodeResponse"] = Field(
        None,
        description="The root node of the Merkle tree."
    )