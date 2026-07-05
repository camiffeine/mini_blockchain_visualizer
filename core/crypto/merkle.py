from .hashing import sha256
from ..blockchain.transaction import Transaction

class MerkleNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.hash = None

class MerkleTree:
    def __init__(self):
        self.root = None
        self.leaves = []

    def build_tree(self, transactions):
        # Create leaf nodes
        self.leaves = [MerkleNode() for _ in transactions]
        for i, transaction in enumerate(transactions):
            self.leaves[i].hash = sha256(transaction.serialize().encode())

        # Build the tree
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []

            # Pair up nodes and create parent nodes
            for i in range(0, len(current_level), 2):
                parent_node = MerkleNode()
                parent_node.left = current_level[i]

                # If there's an odd number of nodes, duplicate the last node
                if i + 1 < len(current_level):
                    parent_node.right = current_level[i + 1]
                    combined_hash = current_level[i].hash + current_level[i + 1].hash
                else:
                    combined_hash = current_level[i].hash + current_level[i].hash  # Duplicate last node if odd number of nodes

                parent_node.hash = sha256(combined_hash.encode())
                next_level.append(parent_node)

            current_level = next_level

        # Set the root of the tree
        self.root = current_level[0] if current_level else None

    # TODO: Implement the proof generation method
    # This method should generate a proof for a given transaction, which consists of the hashes of the sibling nodes along the path from the leaf node to the root.
    def generate_proof(self):
        pass

    # TODO: Implement the proof verification method
    # This method should verify a proof for a given transaction by reconstructing the path from the leaf node to the root using the provided proof and comparing the resulting hash with the root hash.
    def verify_proof(self):
        pass

    # Utility function to print the tree structure
    def print_tree(self, node, level=0):
        if node is not None:
            self.print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.hash)
            self.print_tree(node.left, level + 1)

# Test usage (provisional)
def main():
    messages = [
        Transaction("Hola"),
        Transaction("Criptografía"),
        Transaction("Post-cuántica"),
        Transaction("UNAL!")
    ]

    tree = MerkleTree()
    tree.build_tree(messages)
    tree.print_tree(tree.root)

if __name__ == "__main__":
    main()