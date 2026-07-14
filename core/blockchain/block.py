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
            # use the stored block index (fallback to 0)
            index=self.index if hasattr(self, 'index') else 0,
            #timestamp=time.time(),
            # store the merkle root as a string (hash) instead of the MerkleNode object
            merkle_root=self.merkle_tree.root.hash if (self.merkle_tree and self.merkle_tree.root) else "",
            nonce=0, # Nonce will be set during mining, 0 during Proof of Concept (PoC) phase
            difficulty=0, # Difficulty will be set during mining, 0 during Proof of Concept (PoC) phase
            block_hash="",
            previous_hash=previous_hash
        )

    # Calculate the hash of the block header and update the block's hash
    def calculate_hash(self):
        self.header.block_hash = self.header.calculate_hash()
        self.hash = self.header.block_hash

    # TODO: Internally validate the block by checking the integrity of its hash and Merkle root
    def validate(self):
        # Temporal Merkle Tree build
        new_tree = MerkleTree()
        new_tree.build_tree(self.transactions)
        new_root = new_tree.root

    # Print the block's details, including its header and transactions
    def print_block(self):
        print(f"Block Index: {self.header.index}")
        print(f"Timestamp: {self.header.timestamp}")
        print(f"Merkle Root: {self.header.merkle_root}")
        print(f"Nonce: {self.header.nonce}")
        print(f"Difficulty: {self.header.difficulty}")
        print(f"Block Hash: {self.header.block_hash}")
        print(f"Previous Hash: {self.header.previous_hash}")
        print("Transactions:")
        for transaction in self.transactions:
            print(transaction.to_dict())