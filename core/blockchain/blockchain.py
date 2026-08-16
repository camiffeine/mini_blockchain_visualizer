from .transaction import Transaction
from .linked_list import LinkedList, Node
from .block import Block
from ..exceptions import (
    BlockchainException,
    TransactionError,
    InvalidBlockError,
    BlockchainValidationError
)

MAX_TRANSACTIONS_PER_BLOCK = 4

class Blockchain:
    def __init__(self):
        self.chain = LinkedList()
        self.pending_transactions = []
        self.max_transactions = MAX_TRANSACTIONS_PER_BLOCK
        self.difficulty = 0  # Difficulty will be set during mining, 0 during Proof of Concept (PoC) phase
        self.create_genesis_block()

    # Create the genesis block and add it to the blockchain
    def create_genesis_block(self):
        # Create block, index 0 and no transactions for genesis block
        genesis_block = Block(0, "0" * 64, [])
        genesis_block.build_merkle_tree()
        genesis_block.calculate_hash()

        # Append genesis block to the blockchain's linked list
        self.chain.append(Node())
        self.chain.tail.block = genesis_block

    # Add a transaction to the list of pending transactions and create a new block if the maximum number of transactions is reached
    def add_transaction(self, transaction: Transaction):
        """
        Add a transaction to the pending transactions list.
        
        Creates a new block automatically when the maximum number of pending
        transactions (MAX_TRANSACTIONS_PER_BLOCK) is reached.
        
        Args:
            transaction: The transaction to add to the blockchain
            
        Raises:
            TransactionError: If the transaction is invalid
        """
        # Check if the transaction is valid before adding it to pending transactions
        if not isinstance(transaction, Transaction):
            raise TransactionError(
                f"Invalid transaction. Must be an instance of Transaction class, got {type(transaction)}"
            )

        # Add the transaction to the list of pending transactions
        self.pending_transactions.append(transaction)

        # If the number of pending transactions reaches the maximum, create a new block
        if len(self.pending_transactions) >= self.max_transactions:
            self.create_block()

    # Create a new block with pending transactions and add it to the blockchain.
    def create_block(self):
        """
        Create a new block with pending transactions.
        
        Creates a new block from all currently pending transactions and appends
        it to the blockchain. The pending transactions list is cleared after
        the block is created.
        
        Returns:
            Block: The newly created block, or None if no pending transactions
            
        Raises:
            BlockchainException: If block creation fails
        """
        # Check if there are pending transactions to create a new block
        if len(self.pending_transactions) == 0:
            raise BlockchainException("No pending transactions to create a block.")

        # Create a new block with the next index and pending transactions
        previous_hash = self.chain.tail.block.header.hash if self.chain.tail else "0" * 64
        new_block = Block(self.chain.length, previous_hash, self.pending_transactions)
        new_block.build_merkle_tree()
        new_block.calculate_hash()

        # Append the new block to the blockchain's linked list
        self.chain.append(Node())
        self.chain.tail.block = new_block

        # Clear pending transactions after creating the block
        self.pending_transactions = []
        return new_block

    # Validate the blockchain integrity by checking the internal consistency of each block and the links between them. Returns True if valid, False otherwise
    def validate_chain(self):
        """
        Validate the entire blockchain integrity.
        
        Checks that:
        1. Each block's hash is valid (Merkle root matches transactions)
        2. Each block's previous hash matches the previous block's hash
        3. The chain is not tampered with
        
        Returns:
            bool: True if the entire blockchain is valid, False otherwise
        """
        current_block = self.chain.head.next  # Start from the second block (index 1) since the genesis block has no previous block
        previous_hash = self.chain.head.block.header.hash if self.chain.head else None
        current_hash = current_block.block.header.hash if current_block else None
        while current_block:
            # Validate the current block's integrity
            if not current_block.block.validate():
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.block.header.previous_hash != previous_hash:
                return False

            # Update previous_hash for the next iteration
            current_block = current_block.next
            previous_hash = current_hash
            current_hash = current_block.block.header.hash if current_block else None

        return True

    # Print the entire blockchain, including each block's details and transactions
    def print_chain(self):
        """Print the entire blockchain to stdout (for debugging purposes)."""
        current = self.chain.head
        while current:
            current.block.print_block()
            print("-" * 40)
            current = current.next

    # Get the last block in the blockchain. Returns None if the blockchain is empty
    def get_last_block(self):
        """
        Get the last block in the blockchain.
        
        Returns:
            Block: The last block in the chain, or None if empty
        """
        return self.chain.tail.block if self.chain.tail else None

    # Get a block from the blockchain by its index. Returns None if the block is not found
    def get_block(self, index: int):
        """
        Get a block from the blockchain by its index.
        
        Args:
            index: The block index to retrieve
            
        Returns:
            Block: The block at the specified index, or None if not found
        """
        current = self.chain.head
        while current:
            if current.block.header.index == index:
                return current.block
            current = current.next
        return None

    # Get the entire blockchain as a list of dictionaries, where each dictionary represents a block's data
    def get_chain(self):
        """
        Get the entire blockchain as a list of dictionaries.
        
        Each dictionary represents a block's complete data including transactions.
        
        Returns:
            list: List of block dictionaries
        """
        chain_data = []
        current = self.chain.head
        while current:
            block_data = current.block.to_dict()
            chain_data.append(block_data)
            current = current.next
        return chain_data

    # Tamper with a specific transaction in a block by providing the block index, transaction index, and new transaction. Rebuilds the Merkle tree and recalculates the block hash after tampering
    def tamper_transaction(self, block_index: int, transaction_index: int, new_transaction: Transaction):
        """
        Tamper with a specific transaction in a block for demonstration purposes.

        This intentionally mutates the committed data without rebuilding the Merkle tree
        or recalculating the block hash. The block should therefore fail validation and
        any Merkle proof generated from the original committed root becomes invalid.

        Args:
            block_index: The index of the block containing the transaction
            transaction_index: The index of the transaction within the block
            new_transaction: The new transaction to replace the old one with

        Raises:
            InvalidBlockError: If block or transaction index is invalid
        """
        block: Block | None = self.get_block(block_index)
        if block is None:
            raise InvalidBlockError(f"Block {block_index} not found.")

        if transaction_index < 0 or transaction_index >= len(block.transactions):
            raise InvalidBlockError(
                f"Transaction index {transaction_index} is out of bounds for block {block_index}."
            )

        # Intentionally mutate the transaction without reconciling the Merkle root or block hash.
        block.transactions[transaction_index] = new_transaction