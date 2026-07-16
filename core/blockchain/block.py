from ..shared.hashable import Hashable
from ..crypto.merkle import MerkleTree
from .block_header import BlockHeader
import time

class Block(Hashable):
    def __init__(self, block_index, previous_hash, transactions):
        super().__init__()
        # Store the block index passed to the constructor
        self.index = block_index
        self.header = None
        self.merkle_tree = None
        self.transactions = transactions
        self.build_merkle_tree()
        self.build_block_header(previous_hash)
        self.calculate_hash()

    # Build the Merkle tree from the block's transactions
    def build_merkle_tree(self):
        if self.transactions is not None and len(self.transactions) > 0:
            self.merkle_tree = MerkleTree()
            self.merkle_tree.build_tree(self.transactions)

    # Build the block header using the previous block's hash
    def build_block_header(self, previous_hash):
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

    # Calculate the hash of the block header and update the block's hash
    def calculate_hash(self):
        self.header.hash = self.header.calculate_hash()
        self.hash = self.header.hash

    # Internally validate the block by checking the integrity of its hash and Merkle root
    def validate(self) -> bool:
        # Temporal new Merkle Tree build
        rebuilt_tree = MerkleTree()
        rebuilt_tree.build_tree(self.transactions)
        rebuilt_root = rebuilt_tree.root.hash

        print(f"Old Merkle Root: {self.header.merkle_root}")
        print(f"New Merkle Root: {rebuilt_root if rebuilt_root else ''}")

        # Temporal new Block Header hash calc
        rebuilt_header = self.header.from_dict(self.header.to_dict())
        rebuilt_header.hash = None # Reset the hash to force recalculation
        recalculated_hash = rebuilt_header.calculate_hash()

        print(f"Old Block Hash: {self.header.hash}")
        print(f"New Block Hash: {recalculated_hash}")

        print(f"Old Header: {self.header.to_dict()}")
        print(f"New Header: {rebuilt_header.to_dict()}")

        if rebuilt_root != self.header.merkle_root:
            return False

        if recalculated_hash != self.header.hash or recalculated_hash != self.hash:
            return False

        return True

    # Print the block's details, including its header and transactions
    def print_block(self):
        print(f"Block Index: {self.header.index}")
        print(f"Timestamp: {self.header.timestamp}")
        print(f"Merkle Root: {self.header.merkle_root}")
        print(f"Nonce: {self.header.nonce}")
        print(f"Difficulty: {self.header.difficulty}")
        print(f"Block Hash: {self.header.hash}")
        print(f"Previous Hash: {self.header.previous_hash}")
        print("Transactions:")
        for transaction in self.transactions:
            print(transaction.to_dict())