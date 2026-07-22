from dataclasses import dataclass, field
from enum import Enum

from .hashing import sha256

class SiblingPosition(Enum):
    LEFT = "left"
    RIGHT = "right"

# ProofStep represents a single step in the Merkle proof, containing the sibling hash and its position (left or right)
@dataclass(frozen=True)
class ProofStep:
    sibling_hash: str
    position: SiblingPosition

# MerkleProof represents the entire Merkle proof for a transaction, including the transaction hash, the Merkle root, and a list of proof steps
@dataclass(frozen=True)
class MerkleProof:
    transaction_hash: str
    merkle_root: str
    proof_steps: list[ProofStep] = field(default_factory=list)

    @property
    def depth(self) -> int:
        return len(self.proof_steps)

    @property
    def is_empty(self) -> bool:
        return len(self.proof_steps) == 0

    def print_proof(self):
        print(f"Transaction Hash: {self.transaction_hash}")
        print(f"Merkle Root: {self.merkle_root}")
        print("Proof Steps:")
        for step in self.proof_steps:
            print(f"  Sibling Hash: {step.sibling_hash}, Position: {step.position.value}")

# MerkleNode represents a node in the Merkle tree, containing references to its left and right child nodes and its hash value
class MerkleNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.hash = None

# MerkleTree represents the entire Merkle tree structure, allowing for building the tree from transactions, generating proofs, and verifying proofs
class MerkleTree:
    def __init__(self):
        self.root = None
        self.leaves = []

    def build_tree(self, transactions):
        # Create leaf nodes
        self.leaves = [MerkleNode() for _ in transactions]
        for i, transaction in enumerate(transactions):
            self.leaves[i].hash = sha256(transaction.serialize().encode())

        # Build the tree
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []

            # Pair up nodes and create parent nodes
            for i in range(0, len(current_level), 2):
                parent_node = MerkleNode()
                parent_node.left = current_level[i]

                # If there's an odd number of nodes, duplicate the last node
                if i + 1 < len(current_level):
                    parent_node.right = current_level[i + 1]
                    combined_hash = current_level[i].hash + current_level[i + 1].hash
                else:
                    combined_hash = current_level[i].hash + current_level[i].hash  # Duplicate last node if odd number of nodes

                parent_node.hash = sha256(combined_hash.encode())
                next_level.append(parent_node)

            current_level = next_level

        # Set the root of the tree
        self.root = current_level[0] if current_level else None

    # This method should generate a proof for a given transaction, which consists of the hashes of the sibling nodes along the path from the leaf node to the root
    def generate_proof(self, transaction_hash: str) -> MerkleProof:
        #Raises ValueError if the transaction_hash is not found among leaves.
        if not self.leaves:
            raise ValueError("Tree has no leaves")

        # Build levels of hashes (level[0] = leaves)
        levels: list[list[str]] = [[leaf.hash for leaf in self.leaves]]

        while len(levels[-1]) > 1:
            current = levels[-1]
            next_level: list[str] = []
            for i in range(0, len(current), 2):
                left = current[i]
                if i + 1 < len(current):
                    right = current[i + 1]
                else:
                    # duplicate last when odd number of nodes
                    right = left
                parent_hash = sha256((left + right).encode())
                next_level.append(parent_hash)
            levels.append(next_level)

        # Find the leaf index for the requested transaction_hash
        try:
            index = levels[0].index(transaction_hash)
        except ValueError:
            raise ValueError("Transaction hash not found in tree leaves")

        proof_steps: list[ProofStep] = []
        idx = index

        # For each level, collect sibling info and move index to parent
        for level in levels[:-1]:
            # determine sibling index and position
            if idx % 2 == 0:
                # current is left node; sibling is right (or duplicate)
                sibling_idx = idx + 1 if (idx + 1) < len(level) else idx
                position = SiblingPosition.RIGHT
            else:
                # current is right node; sibling is left
                sibling_idx = idx - 1
                position = SiblingPosition.LEFT

            sibling_hash = level[sibling_idx]
            proof_steps.append(ProofStep(sibling_hash=sibling_hash, position=position))

            idx //= 2  # move to parent index

        merkle_root: str = levels[-1][0] if levels[-1] else str(None)
        return MerkleProof(transaction_hash=transaction_hash, merkle_root=merkle_root, proof_steps=proof_steps)

    # This method should verify a proof for a given transaction by reconstructing the path from the leaf node to the root using the provided proof and comparing the resulting hash with the root hash
    @staticmethod
    def verify_proof(transaction_hash: str, proof: MerkleProof, expected_merkle_root: str) -> bool:
        # Optional sanity check: ensure proof was generated for this tx hash
        if proof.transaction_hash and proof.transaction_hash != transaction_hash:
            return False

        current_hash = transaction_hash

        for step in proof.proof_steps:
            if step.position == SiblingPosition.RIGHT:
                # sibling is to the right: H(current || sibling)
                current_hash = sha256((current_hash + step.sibling_hash).encode())
            else:
                # sibling is to the left: H(sibling || current)
                current_hash = sha256((step.sibling_hash + current_hash).encode())

        return current_hash == expected_merkle_root

    # Utility function to print the tree structure
    def print_tree(self, node, level=0):
        if node is not None:
            self.print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.hash)
            self.print_tree(node.left, level + 1)