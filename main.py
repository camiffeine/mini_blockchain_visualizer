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
    is_valid = MerkleTree.verify_proof(tx_hash, proof, tree.root.hash)
    print("Proof valid:", is_valid)

# Test the Block structure implementation
def test_block(transactions):
    block = Block(0, "0" * 64, transactions)
    block.build_merkle_tree()
    block.calculate_hash()
    block.print_block()

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

def main():
    # Create sample transactions
    transactions = [
        Transaction("Hola"),
        Transaction("Criptografía"),
        Transaction("Post-cuántica"),
        Transaction("UNAL!"),
    ]
    #test_merkle_tree(transactions)
    #test_block(transactions)
    #test_blockchain(transactions)

if __name__ == "__main__":
    main()