from .transaction import Transaction
from .linked_list import LinkedList, Node
from .block import Block

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
        # Check if the transaction is valid before adding it to pending transactions
        if not isinstance(transaction, Transaction):
            print("Invalid transaction. Must be an instance of Transaction class.")
            return

        # TODO: Implement transaction validation

        # Add the transaction to the list of pending transactions
        self.pending_transactions.append(transaction)

        # If the number of pending transactions reaches the maximum, create a new block
        if len(self.pending_transactions) >= self.max_transactions:
            self.create_block()

    # Create a new block with pending transactions and add it to the blockchain.
    def create_block(self):
        # Check if there are pending transactions to create a new block
        if len(self.pending_transactions) == 0:
            print("No pending transactions to create a block.")
            return

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
        print("New block created.")
        return new_block

    # Validate the blockchain integrity by checking the internal consistency of each block and the links between them. Returns True if valid, False otherwise
    def validate_chain(self):
        current_block = self.chain.head.next  # Start from the second block (index 1) since the genesis block has no previous block
        previous_hash = self.chain.head.block.header.hash if self.chain.head else None
        current_hash = current_block.block.header.hash if current_block else None
        while current_block:
            # Validate the current block's integrity
            if not current_block.block.validate():
                print(f"Block {current_block.block.header.index} failed validation.")
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.block.header.previous_hash != previous_hash:
                print(f"Block {current_block.block.header.index} has an invalid previous hash.")
                return False

            # Update previous_hash for the next iteration
            current_block = current_block.next
            previous_hash = current_hash
            current_hash = current_block.block.header.hash if current_block else None

        return True

    # Print the entire blockchain, including each block's details and transactions
    def print_chain(self):
        current = self.chain.head
        while current:
            current.block.print_block()
            print("-" * 40)
            current = current.next

    # Get the last block in the blockchain. Returns None if the blockchain is empty
    def get_last_block(self):
        return self.chain.tail.block if self.chain.tail else None

    # Get a block from the blockchain by its index. Returns None if the block is not found
    def get_block(self, index: int):
        current = self.chain.head
        while current:
            if current.block.header.index == index:
                return current.block
            current = current.next
        return None

    # Get the entire blockchain as a list of dictionaries, where each dictionary represents a block's data
    def get_chain(self):
        chain_data = []
        current = self.chain.head
        while current:
            block_data = current.block.to_dict()
            chain_data.append(block_data)
            current = current.next
        return chain_data

    # Tamper with a specific transaction in a block by providing the block index, transaction index, and new transaction. Rebuilds the Merkle tree and recalculates the block hash after tampering
    def tamper_transaction(self, block_index: int, transaction_index: int, new_transaction: Transaction):
        block: Block | None = self.get_block(block_index)
        if block is None:
            print(f"Block {block_index} not found.")
            return

        if transaction_index < 0 or transaction_index >= len(block.transactions):
            print(f"Transaction index {transaction_index} is out of bounds for block {block_index}.")
            return

        # Tamper with the specified transaction
        block.transactions[transaction_index] = new_transaction
        # Rebuild the Merkle tree and recalculate the block hash after tampering
        #block.merkle_tree = None  # Reset the Merkle tree before rebuilding
        #block.build_merkle_tree()
        #block.calculate_hash()