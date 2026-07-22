from core.crypto.merkle import *
from core.blockchain.transaction import Transaction
from core.blockchain.blockchain import Blockchain

def main_menu():
    print(" " * 40)
    print("Welcome to the Blockchain Application")
    print("-" * 40)
    print("1. Create a new transaction")
    print("2. Tamper with a transaction")
    print("3. Create a new block")
    print("4. Print blockchain status and validate the blockchain")
    print("5. Print the entire blockchain")
    print("6. Print a specific block")
    print("7. Create and verify a Merkle proof for a transaction")
    print("0. Exit")
    print(" " * 40)

# Create a new transaction by prompting the user for metadata and adding it to the blockchain's pending transactions
def create_transaction(blockchain):
    metadata = input("Enter transaction metadata: ")
    transaction = Transaction(metadata)
    blockchain.add_transaction(transaction)
    print("Transaction added.")
    print(" ")

# Tamper with a specific transaction in a block by providing the block index, transaction index, and new transaction metadata
def tamper_transaction(blockchain):
    block_index = int(input("Enter block index to tamper: "))
    transaction_index = int(input("Enter transaction index to tamper: "))
    new_metadata = input("Enter new transaction metadata: ")
    new_transaction = Transaction(new_metadata)
    blockchain.tamper_transaction(block_index, transaction_index, new_transaction)
    print(f"Transaction at index {transaction_index} in block {block_index} has been tampered.")
    print(" ")

# Print the blockchain status, including the last block's index and hash, and validate the blockchain
def print_blockchain_status(blockchain):
    last_block = blockchain.get_last_block()
    is_valid = blockchain.validate_chain()
    if last_block:
        print("Blockchain Status:")
        print("-" * 40)
        print("Blockchain valid:", is_valid)
        print(f"Blockchain Length: {blockchain.chain.length}")
        print(f"Last Block Index: {last_block.header.index}, Hash: {last_block.header.hash}")
        print(f"Number of Transactions in Last Block: {len(last_block.transactions)}")
        print(f"Pending Transactions: {len(blockchain.pending_transactions)}")
        print(" ")
    else:
        print("Blockchain is empty.")
        print(" ")

# Print a specific block's details, including its transactions and Merkle tree
def print_block(blockchain):
    block_index = int(input("Enter block index to print: "))
    block = blockchain.get_block(block_index)
    if block:
        block.print_block()
        print(f"Valid block: {block.validate()}")
        print("-" * 40)
        print(f"Merkle Tree of Block {block_index}:")
        if len(block.transactions) == 0:
            print("No Merkle Tree available.")
        else:
            block.merkle_tree.print_tree(block.merkle_tree.root)
        print(" ")
    else:
        print(f"Block {block_index} not found.")
        print(" ")

# Create and verify a Merkle proof for a specific transaction in a block
def create_and_verify_merkle_proof(blockchain):
    block_index = int(input("Enter block index to create Merkle proof: "))
    transaction_index = int(input("Enter transaction index to create Merkle proof: "))
    block = blockchain.get_block(block_index)
    if block:
        if 0 <= transaction_index < len(block.transactions):
            print("Creation of Merkle Proof")
            transaction = block.merkle_tree.leaves[transaction_index]
            print(f"Metadata of selected transaction: {block.transactions[transaction_index].metadata}")
            proof = block.merkle_tree.generate_proof(transaction_index)
            if proof:
                print(f"Merkle Proof for Transaction at index {transaction_index} in Block {block_index}:")
                proof.print_proof()
            else:
                print("Failed to generate Merkle proof.")

            print(" " * 40)
            print("Verification of Merkle Proof")
            is_valid = MerkleTree.verify_proof(transaction.hash, proof, block.header.merkle_root)
            print("Merkle Proof valid:", is_valid)
        else:
            print(f"Transaction index {transaction_index} is out of bounds for block {block_index}.")
    else:
        print(f"Block {block_index} not found.")
    print(" ")

def main():
    # Initialize blockchain
    blockchain = Blockchain()

    # Main loop
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            create_transaction(blockchain)

        elif choice == "2":
            tamper_transaction(blockchain)

        elif choice == "3":
            blockchain.create_block()
            print(" ")

        elif choice == "4":
            print_blockchain_status(blockchain)

        elif choice == "5":
            blockchain.print_chain()
            print(" ")

        elif choice == "6":
            print_block(blockchain)

        elif choice == "7":
            create_and_verify_merkle_proof(blockchain)

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
            print(" ")

if __name__ == "__main__":
    main()