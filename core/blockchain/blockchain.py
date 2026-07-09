from .transaction import Transaction
from .linked_list import LinkedList, Node
from .block import Block
from .block_header import BlockHeader

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

        # Validate transaction
        if transaction.sender != "" or transaction.receiver != "" or transaction.amount < 0:
            print("Invalid transaction.")
            return

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
        previous_hash = self.chain.tail.block.header.block_hash if self.chain.tail else "0" * 64
        new_block = Block(self.chain.length, previous_hash, self.pending_transactions)
        new_block.build_merkle_tree()
        new_block.calculate_hash()

        # Append the new block to the blockchain's linked list
        self.chain.append(Node())
        self.chain.tail.block = new_block

        # Clear pending transactions after creating the block
        self.pending_transactions = []