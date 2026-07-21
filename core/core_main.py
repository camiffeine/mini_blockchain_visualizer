from core.crypto.merkle import *
from core.blockchain.transaction import Transaction
from core.blockchain.block import Block
from core.blockchain.blockchain import Blockchain

def main_menu():
    print("Welcome to the Blockchain Application")
    print("1. Create a new transaction")
    print("2. Create a new block")
    print("3. Validate the blockchain")
    print("4. Print the entire blockchain")
    print("5. Print blockchain Status")
    print("6. Exit")

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
            blockchain.create_block()
            print("New block created.")

        elif choice == "3":
            is_valid = blockchain.validate_chain()
            print("Blockchain valid:", is_valid)

        elif choice == "4":
            blockchain.print_chain()

        elif choice == "5":
            last_block = blockchain.get_last_block()
            if last_block:
                print("Blockchain Status:")
                print(f"Blockchain Length: {blockchain.chain.length}")
                print(f"Last Block Index: {last_block.header.index}, Hash: {last_block.header.hash}")
                print(f"Number of Transactions in Last Block: {len(last_block.transactions)}")
                print(f"Pending Transactions: {len(blockchain.pending_transactions)}")
            else:
                print("Blockchain is empty.")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()