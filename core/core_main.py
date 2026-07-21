from core.crypto.merkle import *
from core.blockchain.transaction import Transaction
from core.blockchain.block import Block
from core.blockchain.blockchain import Blockchain

def main_menu():
    print("Welcome to the Blockchain Application")
    print("1. Create a new transaction")
    print("2. Tamper with a transaction")
    print("3. Create a new block")
    print("4. Validate the blockchain")
    print("5. Print the entire blockchain")
    print("6. Print blockchain Status")
    print("7. Exit")

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

        elif choice == "2":
            block_index = int(input("Enter block index to tamper: "))
            transaction_index = int(input("Enter transaction index to tamper: "))
            new_metadata = input("Enter new transaction metadata: ")
            new_transaction = Transaction(new_metadata)
            blockchain.tamper_transaction(block_index, transaction_index, new_transaction)
            print(f"Transaction at index {transaction_index} in block {block_index} has been tampered.")

        elif choice == "3":
            blockchain.create_block()
            print("New block created.")

        elif choice == "4":
            is_valid = blockchain.validate_chain()
            print("Blockchain valid:", is_valid)

        elif choice == "5":
            blockchain.print_chain()

        elif choice == "6":
            last_block = blockchain.get_last_block()
            if last_block:
                print("Blockchain Status:")
                print(f"Blockchain Length: {blockchain.chain.length}")
                print(f"Last Block Index: {last_block.header.index}, Hash: {last_block.header.hash}")
                print(f"Number of Transactions in Last Block: {len(last_block.transactions)}")
                print(f"Pending Transactions: {len(blockchain.pending_transactions)}")
            else:
                print("Blockchain is empty.")

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()