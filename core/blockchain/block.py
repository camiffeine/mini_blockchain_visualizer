from ..shared.hashable import Hashable
from ..crypto.merkle import MerkleTree
from .block_header import BlockHeader
import time

class Block(Hashable):
    """
    Represents a single block in the blockchain.
    
    A block contains a header (with metadata and hash pointers), a list of transactions,
    and a Merkle tree structure. The block's integrity is ensured through:
    - SHA-256 hashing of the block header
    - Merkle tree root hash of all transactions
    - Hash pointer to the previous block
    
    Attributes:
        index: The block's position in the blockchain
        header: BlockHeader object with metadata and hash information
        transactions: List of Transaction objects in this block
        merkle_tree: MerkleTree object for proof generation
        hash: The calculated SHA-256 hash of the block header
    """
    
    def __init__(self, block_index, previous_hash, transactions):
        """
        Initialize a new block.
        
        Args:
            block_index: The position of this block in the chain
            previous_hash: Hash of the previous block (for chain linking)
            transactions: List of Transaction objects to include in the block
        """
        super().__init__()
        # Store the block index passed to the constructor
        self.index = block_index
        self.header = None
        self.merkle_tree = None
        self.transactions = transactions
        self.build_merkle_tree()
        self.build_block_header(previous_hash)
        self.calculate_hash()

    def build_merkle_tree(self):
        """
        Build the Merkle tree from the block's transactions.
        
        Creates a complete binary tree where:
        - Leaves are hashes of individual transactions
        - Internal nodes are hashes of their children
        - Root hash is stored in the block header
        
        For blocks with no transactions, merkle_tree remains None.
        """
        if self.transactions is not None and len(self.transactions) > 0:
            self.merkle_tree = MerkleTree()
            self.merkle_tree.build_tree(self.transactions)

    def build_block_header(self, previous_hash):
        """
        Build the block header with metadata.
        
        The block header contains:
        - Index and timestamp
        - Merkle root (for transaction integrity)
        - Nonce and difficulty (for PoW, set to 0 in MVP)
        - Previous block's hash (for chain linking)
        
        Args:
            previous_hash: Hash of the previous block in the chain
        """
        self.header = BlockHeader(
            # Use the stored block index (fallback to 0)
            index=self.index if hasattr(self, 'index') else 0,
            timestamp=time.time(),
            # Store the merkle root as a string (hash) instead of the MerkleNode object
            merkle_root=self.merkle_tree.root.hash if (self.merkle_tree and self.merkle_tree.root) else "",
            nonce=0, # Nonce will be set during mining, 0 during Proof of Concept (PoC) phase
            difficulty=0, # Difficulty will be set during mining, 0 during Proof of Concept (PoC) phase
            hash=None, # Hash will be calculated after the block header is built
            previous_hash=previous_hash
        )

    def calculate_hash(self):
        """
        Calculate and store the SHA-256 hash of the block header.
        
        Updates both the header's hash field and the block's hash field to maintain
        consistency. This hash commits to all block data (transactions via merkle root,
        timestamp, nonce, difficulty, and previous block hash).
        """
        self.header.hash = self.header.calculate_hash()
        self.hash = self.header.hash

    def validate(self) -> bool:
        """
        Validate the block's integrity.
        
        Checks that:
        1. The block's hash matches the recalculated hash from header fields
        2. The Merkle root matches a freshly built tree from transactions
           (detects tampering with transactions)
        
        Returns:
            bool: True if block is valid, False if tampering or corruption detected
        """
        # Temporal new Merkle Tree build if not genesis block
        if len(self.transactions) > 0:
            rebuilt_tree = MerkleTree()
            rebuilt_tree.build_tree(self.transactions)
            rebuilt_root = rebuilt_tree.root.hash

        #print(f"Old Merkle Root: {self.header.merkle_root}")
        #print(f"New Merkle Root: {rebuilt_root if rebuilt_root else ''}")

        # Temporal new Block Header hash calc
        rebuilt_header = self.header.from_dict(self.header.to_dict())
        rebuilt_header.hash = None # Reset the hash to force recalculation
        recalculated_hash = rebuilt_header.calculate_hash()

        #print(f"Old Block Hash: {self.header.hash}")
        #print(f"New Block Hash: {recalculated_hash}")

        #print(f"Old Header: {self.header.to_dict()}")
        #print(f"New Header: {rebuilt_header.to_dict()}")

        if len(self.transactions) > 0 and rebuilt_root != self.header.merkle_root:
            return False

        if recalculated_hash != self.header.hash or recalculated_hash != self.hash:
            return False

        return True

    def to_dict(self):
        """
        Convert the block to a dictionary representation.
        
        Used for JSON serialization and API responses. Includes validation status
        calculated at serialization time.
        
        Returns:
            dict: Block data with keys:
                - index, valid, timestamp, merkle_root, nonce, difficulty
                - hash, previous_hash, transactions (as list of dicts)
        """
        return {
            "index": self.index,
            "valid": self.validate(),
            "timestamp": self.header.timestamp,
            "merkle_root": self.header.merkle_root,
            "nonce": self.header.nonce,
            "difficulty": self.header.difficulty,
            "hash": self.hash,
            "previous_hash": self.header.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions] if self.transactions else [],
        }

    def print_block(self):
        """
        Print a human-readable representation of the block and its contents.
        
        Output includes block header, validation status, all transaction details,
        and hash information. Useful for debugging and CLI inspection.
        """
        print(f"Block Index: {self.header.index}")
        print(f"Block Valid: {self.validate()}")
        print(f"Timestamp: {self.header.timestamp}")
        print(f"Merkle Root: {self.header.merkle_root}")
        print(f"Nonce: {self.header.nonce}")
        print(f"Difficulty: {self.header.difficulty}")
        print(f"Block Hash: {self.header.hash}")
        print(f"Previous Hash: {self.header.previous_hash}")
        print("Transactions:")
        if len(self.transactions) > 0:
            for transaction in self.transactions:
                print(transaction.to_dict())
        else:
            print("No available transactions at this block.")