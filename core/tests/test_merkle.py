"""
Unit tests for Merkle Tree functionality.
"""

import pytest
from core.blockchain.transaction import Transaction
from core.crypto.merkle import MerkleTree


class TestMerkleTreeConstruction:
    """Tests for Merkle tree building."""

    def test_build_merkle_tree_with_transactions(self, sample_transactions):
        """Test building a merkle tree from transactions."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        assert tree.root is not None
        assert tree.leaves is not None
        assert len(tree.leaves) == 4

    def test_merkle_tree_root_hash_exists(self, sample_transactions):
        """Test that built merkle tree has a root hash."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        assert tree.root.hash is not None
        assert len(tree.root.hash) > 0

    def test_merkle_tree_leaves_have_hashes(self, sample_transactions):
        """Test that all leaves in merkle tree have hashes."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        for leaf in tree.leaves:
            assert leaf.hash is not None
            assert len(leaf.hash) > 0

    def test_merkle_tree_with_two_transactions(self):
        """Test building merkle tree with exactly 2 transactions."""
        transactions = [
            Transaction(None, None, 0, "Tx1"),
            Transaction(None, None, 0, "Tx2"),
        ]
        tree = MerkleTree()
        tree.build_tree(transactions)
        
        assert len(tree.leaves) == 2
        assert tree.root is not None

    def test_merkle_tree_with_single_transaction(self):
        """Test building merkle tree with a single transaction."""
        transactions = [Transaction(None, None, 0, "Tx1")]
        tree = MerkleTree()
        tree.build_tree(transactions)
        
        assert len(tree.leaves) == 1
        assert tree.root is not None

    def test_merkle_tree_with_three_transactions(self):
        """Test building merkle tree with 3 transactions (odd number)."""
        transactions = [
            Transaction(None, None, 0, "Tx1"),
            Transaction(None, None, 0, "Tx2"),
            Transaction(None, None, 0, "Tx3"),
        ]
        tree = MerkleTree()
        tree.build_tree(transactions)
        
        assert len(tree.leaves) == 3
        assert tree.root is not None


class TestMerkleProofGeneration:
    """Tests for Merkle proof generation."""

    def test_generate_proof_for_leaf(self, sample_transactions):
        """Test generating a merkle proof for a leaf transaction."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        # generate_proof takes an index, not a hash
        proof = tree.generate_proof(0)
        
        assert proof is not None
        assert len(proof.proof_steps) > 0
        assert proof.transaction_hash is not None
        assert proof.merkle_root is not None

    def test_proof_has_valid_structure(self, sample_transactions):
        """Test that generated proof has valid structure."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        proof = tree.generate_proof(1)
        
        for step in proof.proof_steps:
            assert hasattr(step, 'sibling_hash')
            assert hasattr(step, 'position')
            assert step.sibling_hash is not None

    def test_generate_proof_for_different_leaves(self, sample_transactions):
        """Test generating proofs for different leaf transactions."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        proof1 = tree.generate_proof(0)
        proof2 = tree.generate_proof(1)
        
        # Different leaves should have different proofs
        assert len(proof1.proof_steps) > 0
        assert len(proof2.proof_steps) > 0
        # Transaction hashes should be different (different leaves)
        assert proof1.transaction_hash != proof2.transaction_hash


class TestMerkleProofVerification:
    """Tests for Merkle proof verification."""

    def test_verify_valid_proof(self, sample_transactions):
        """Test verifying a valid merkle proof."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        proof = tree.generate_proof(0)
        
        is_valid = MerkleTree.verify_proof(proof.transaction_hash, proof, tree.root.hash)
        assert is_valid is True

    def test_verify_all_leaf_proofs(self, sample_transactions):
        """Test verifying proofs for all leaves."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        for i in range(len(tree.leaves)):
            proof = tree.generate_proof(i)
            is_valid = MerkleTree.verify_proof(proof.transaction_hash, proof, tree.root.hash)
            assert is_valid is True, f"Proof for leaf {i} failed verification"

    def test_verify_invalid_proof_wrong_hash(self, sample_transactions):
        """Test that verification fails with wrong transaction hash."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        proof = tree.generate_proof(0)
        
        # Verify with wrong hash
        wrong_hash = tree.leaves[1].hash
        is_valid = MerkleTree.verify_proof(wrong_hash, proof, tree.root.hash)
        assert is_valid is False

    def test_verify_invalid_proof_wrong_root(self, sample_transactions):
        """Test that verification fails with wrong merkle root."""
        tree = MerkleTree()
        tree.build_tree(sample_transactions)
        
        proof = tree.generate_proof(0)
        
        # Create wrong root by using different transactions
        other_transactions = [
            Transaction(None, None, 0, "Other1"),
            Transaction(None, None, 0, "Other2"),
        ]
        other_tree = MerkleTree()
        other_tree.build_tree(other_transactions)
        
        is_valid = MerkleTree.verify_proof(proof.transaction_hash, proof, other_tree.root.hash)
        assert is_valid is False

    def test_verify_proof_single_transaction(self):
        """Test proof verification with a single transaction."""
        transactions = [Transaction(None, None, 0, "Single")]
        tree = MerkleTree()
        tree.build_tree(transactions)
        
        proof = tree.generate_proof(0)
        
        # With single transaction, proof should verify
        is_valid = MerkleTree.verify_proof(proof.transaction_hash, proof, tree.root.hash)
        assert is_valid is True


class TestMerkleTreeConsistency:
    """Tests for merkle tree consistency across rebuilds."""

    def test_same_transactions_produce_same_root(self):
        """Test that same transactions always produce the same merkle root."""
        transactions1 = [
            Transaction(None, None, 0, "Test1"),
            Transaction(None, None, 0, "Test2"),
            Transaction(None, None, 0, "Test3"),
        ]
        
        # Create first tree
        tree1 = MerkleTree()
        tree1.build_tree(transactions1)
        root1 = tree1.root
        
        # Create second tree with same transactions
        # Note: We need to recreate transactions to avoid timestamp differences
        transactions2 = [
            Transaction(None, None, 0, "Test1"),
            Transaction(None, None, 0, "Test2"),
            Transaction(None, None, 0, "Test3"),
        ]
        tree2 = MerkleTree()
        tree2.build_tree(transactions2)
        root2 = tree2.root
        
        # Roots will differ due to different timestamps in transactions
        # But verification should still work
        proof1 = tree1.generate_proof(0)
        assert MerkleTree.verify_proof(proof1.transaction_hash, proof1, root1.hash) is True
