from core.crypto.merkle import *
from core.blockchain.transaction import Transaction
from core.blockchain.block import Block
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

def main():
    # Initialize blockchain
    blockchain = Blockchain()

    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            metadata = input("Enter transaction metadata: ")
            transaction = Transaction(metadata)
            blockchain.add_transaction(transaction)
            print("Transaction added.")
            print(" ")

        elif choice == "2":
            block_index = int(input("Enter block index to tamper: "))
            transaction_index = int(input("Enter transaction index to tamper: "))
            new_metadata = input("Enter new transaction metadata: ")
            new_transaction = Transaction(new_metadata)
            blockchain.tamper_transaction(block_index, transaction_index, new_transaction)
            print(f"Transaction at index {transaction_index} in block {block_index} has been tampered.")
            print(" ")

        elif choice == "3":
            blockchain.create_block()
            print(" ")

        elif choice == "4":
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

        elif choice == "5":
            blockchain.print_chain()
            print(" ")

        elif choice == "6":
            block_index = int(input("Enter block index to print: "))
            block = blockchain.get_block(block_index)
            if block:
                block.print_block()
                print(f"Valid block: {block.validate()}")
                print("-" * 40)
                print(f"Merkle Tree of Block {block_index}:")
                block.merkle_tree.print_tree(block.merkle_tree.root) if block.merkle_tree else 'No Merkle Tree available.'
                print(" ")
            else:
                print(f"Block {block_index} not found.")
                print(" ")

        elif choice == "7":
            block_index = int(input("Enter block index to create Merkle proof: "))
            transaction_index = int(input("Enter transaction index to create Merkle proof: "))
            block = blockchain.get_block(block_index)
            if block:
                if 0 <= transaction_index < len(block.transactions):
                    print("Creation of Merkle Proof")
                    transaction = block.merkle_tree.leaves[transaction_index]
                    print(f"Metadata of selected transaction: {block.transactions[transaction_index].metadata}")
                    proof = block.merkle_tree.generate_proof(transaction.hash)
                    if proof:
                        print(f"Merkle Proof for Transaction at index {transaction_index} in Block {block_index}:")
                        proof.print_proof()
                    else:
                        print("Failed to generate Merkle proof.")

                    print(" " * 40)
                    print("Verification of Merkle Proof")
                    is_valid = MerkleTree.verify_proof(transaction.hash, proof, block.merkle_tree.root.hash)
                    print("Merkle Proof valid:", is_valid)
                else:
                    print(f"Transaction index {transaction_index} is out of bounds for block {block_index}.")
            else:
                print(f"Block {block_index} not found.")
            print(" ")

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
            print(" ")

if __name__ == "__main__":
    main()