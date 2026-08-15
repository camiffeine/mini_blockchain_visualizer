from dataclasses import dataclass, field
from enum import Enum

from .hashing import sha256

class SiblingPosition(Enum):
    """Enumeration for sibling node position in Merkle proof steps."""
    LEFT = "left"
    RIGHT = "right"

@dataclass(frozen=True)
class ProofStep:
    """
    Represents a single step in a Merkle proof.
    
    A proof step contains the hash of a sibling node and its position (left or right)
    relative to the current node being verified. Used to authenticate a transaction
    by reconstructing the path from leaf to root.
    
    Attributes:
        sibling_hash: The SHA-256 hash of the sibling node
        position: The position of the sibling (LEFT or RIGHT)
    """
    sibling_hash: str
    position: SiblingPosition

@dataclass(frozen=True)
class MerkleProof:
    """
    Represents a complete Merkle proof for a transaction.
    
    A Merkle proof is a minimal set of sibling hashes required to authenticate
    a transaction's presence in a block's Merkle tree. The proof can be verified
    by reconstructing the path from the transaction hash to the root and comparing
    the result with the known Merkle root.
    
    Attributes:
        transaction_hash: The hash of the transaction being proven
        merkle_root: The root hash of the Merkle tree
        proof_steps: List of ProofStep objects representing the authentication path
    """
    transaction_hash: str
    merkle_root: str
    proof_steps: list[ProofStep] = field(default_factory=list)

    @property
    def depth(self) -> int:
        """Returns the depth (number of steps) in the proof."""
        return len(self.proof_steps)

    @property
    def is_empty(self) -> bool:
        """Returns True if the proof contains no steps (single-leaf tree)."""
        return len(self.proof_steps) == 0

    def print_proof(self):
        """Print a human-readable representation of the proof."""
        print(f"Transaction Hash: {self.transaction_hash}")
        print(f"Merkle Root: {self.merkle_root}")
        print("Proof Steps:")
        for step in self.proof_steps:
            print(f"  Sibling Hash: {step.sibling_hash}, Position: {step.position.value}")

class MerkleNode:
    """
    Represents a single node in a Merkle tree.
    
    A node can be either a leaf (representing a transaction) or an internal node
    (representing a combination of child nodes). Each node stores its SHA-256 hash
    and references to its left and right children.
    
    Attributes:
        left: Reference to the left child node (or None if leaf)
        right: Reference to the right child node (or None if leaf)
        hash: The SHA-256 hash of this node
    """
    def __init__(self):
        self.left = None
        self.right = None
        self.hash = None

class MerkleTree:
    """
    Implements a complete binary Merkle tree structure.
    
    A Merkle tree enables efficient verification of large datasets through
    proof of membership. Features:
    - O(n) tree construction from transactions
    - O(log n) proof generation
    - O(log n) proof verification
    - Handles odd numbers of leaves by duplicating the last leaf
    
    Attributes:
        root: The root node of the tree
        leaves: List of leaf nodes (one per transaction)
    """
    def __init__(self):
        self.root = None
        self.leaves = []

    def build_tree(self, transactions):
        """
        Build a Merkle tree from a list of transactions.
        
        Algorithm:
        1. Hash each transaction to create leaf nodes
        2. Pair adjacent leaves and hash their combination
        3. Repeat until only root remains
        4. For odd number of nodes, duplicate the last node
        
        Args:
            transactions: List of Transaction objects to include in the tree
        """
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

    def generate_proof(self, transaction_index: int) -> MerkleProof:
        """
        Generate a Merkle proof for a transaction at the specified index.
        
        The proof contains the minimal set of sibling hashes needed to reconstruct
        the path from the transaction to the root. This can be verified later
        without knowing other transactions.
        
        Args:
            transaction_index: The index of the transaction in the leaves list
            
        Returns:
            MerkleProof: Object containing transaction hash, merkle root, and proof steps
            
        Raises:
            ValueError: If transaction_index is out of bounds or tree is empty
        """
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

        # Find the leaf index for the requested transaction index
        try:
            leaf = levels[0][transaction_index]
        except IndexError:
            raise ValueError("Transaction index out of bounds or not found in leaves.")

        proof_steps: list[ProofStep] = []
        idx = transaction_index

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
        return MerkleProof(transaction_hash=leaf, merkle_root=merkle_root, proof_steps=proof_steps)

    @staticmethod
    def verify_proof(transaction_hash: str, proof: MerkleProof, expected_merkle_root: str) -> bool:
        """
        Verify a Merkle proof against a known root hash.
        
        Reconstructs the authentication path by combining the transaction hash
        with each sibling hash in sequence. If the final computed hash matches
        the expected root, the proof is valid and the transaction is authenticated.
        
        Args:
            transaction_hash: The hash of the transaction being verified
            proof: The MerkleProof object containing proof steps
            expected_merkle_root: The known root hash to verify against
            
        Returns:
            bool: True if proof is valid, False otherwise
        """
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

    def print_tree(self, node, level=0):
        """
        Print a visual representation of the tree structure.
        
        Outputs an indented tree diagram showing the hierarchy of nodes and their hashes.
        Useful for debugging and understanding tree structure.
        
        Args:
            node: The node to start printing from (typically root)
            level: Current indentation level (used for recursion)
        """
        if node is not None:
            self.print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.hash)
            self.print_tree(node.left, level + 1)