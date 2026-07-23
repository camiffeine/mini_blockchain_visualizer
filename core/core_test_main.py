from core.crypto.merkle import *
from core.blockchain.transaction import Transaction
from core.blockchain.block import Block
from core.blockchain.blockchain import Blockchain

# Test the Merkle tree implementation
def test_merkle_tree(transactions):
    # Build and print the Merkle tree
    tree = MerkleTree()
    tree.build_tree(transactions)
    tree.print_tree(tree.root)

    # Pick index 1 ("Criptografía")
    tx_hash = tree.leaves[1].hash
    proof = tree.generate_proof(tx_hash)
    print("Generated proof:")
    proof.print_proof()

    # Verify
    is_valid = tree.verify_proof(tx_hash, proof, tree.root.hash)
    print("Proof valid:", is_valid)

# Test the Block structure implementation
def test_block(transactions):
    block = Block(0, "0" * 64, transactions)
    block.build_merkle_tree()
    block.calculate_hash()
    block.print_block()

# Test Block internal verification before and after tampering
def test_block_tampering(transactions, transaction_index, new_transaction):
    block = Block(0, "0" * 64, transactions)
    # Perform initial test to validate current state
    print(f"Transactions (initial test):")
    for tx in transactions:
        tx_data = tx.to_dict()
        print(f"Transaction metadata: {tx_data['metadata']}")
    print(f"Valid block (initial test): {block.validate()}")

    if transaction_index < 0 or transaction_index >= len(block.transactions):
        print(f"Transaction index {transaction_index} is out of bounds for block.")
        return

    # Tamper with the specified transaction
    block.transactions[transaction_index] = new_transaction

    # Perform second test to validate after modifying a transaction
    print(f"Transactions (tampering test):")
    for tx in transactions:
        tx_data = tx.to_dict()
        print(f"Transaction metadata: {tx_data['metadata']}")
    print(f"Valid block (tampering test): {block.validate()}")

# Test the Blockchain implementation
def test_blockchain(transactions):
    blockchain = Blockchain()
    # Add some transactions
    for transaction in transactions:
        blockchain.add_transaction(transaction)

    # Create a new block with the pending transactions
    blockchain.create_block()

    # Validate the blockchain
    is_valid = blockchain.validate_chain()
    print("Blockchain valid:", is_valid)

    # Print the entire blockchain
    blockchain.print_chain()

# Test Blockchain and Block verification, before and after performing a tx tampering
def test_blockchain_tampering(transactions, tamper_tx):
    blockchain = Blockchain()
    print(f"Genesis block hash: {blockchain.get_block(0).header.hash}")
    # Add some transactions
    for transaction in transactions:
        blockchain.add_transaction(transaction)
    # Create a new block with the pending transactions
    blockchain.create_block()

    # Print the entire blockchain
    blockchain.print_chain()

    # Validate the blockchain
    is_valid = blockchain.validate_chain()
    print("Valid blockchain (initial test):", is_valid)

    # Tamper with the specified transaction
    blockchain.tamper_transaction(1, 1, tamper_tx)

    # Print the entire blockchain again after tampering
    blockchain.print_chain()
    is_valid = blockchain.validate_chain()
    print("Valid blockchain (tampering test):", is_valid)

def main():
    # Create sample transactions
    transactions = [
        Transaction(None, None, 0, "Hola"),
        Transaction(None, None, 0, "Criptografía"),
        Transaction(None, None, 0, "Post-cuántica"),
        Transaction(None, None, 0, "UNAL!"),
    ]

    tamper_tx = Transaction(None, None, 0, "Tampering_tx!")

    #test_merkle_tree(transactions)
    #test_block(transactions)
    #test_blockchain(transactions)
    #test_block_tampering(transactions, 1, tamper_tx)
    test_blockchain_tampering(transactions, tamper_tx)

if __name__ == "__main__":
    main()