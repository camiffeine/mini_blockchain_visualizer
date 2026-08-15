"""
Unit tests for Block class.
"""

import pytest
from core.blockchain.transaction import Transaction
from core.blockchain.block import Block


class TestBlockCreation:
    """Tests for block creation and structure."""

    def test_create_block_with_transactions(self, sample_transactions):
        """Test creating a block with transactions."""
        block = Block(0, "0" * 64, sample_transactions)
        assert block.index == 0
        assert len(block.transactions) == 4
        assert block.header.previous_hash == "0" * 64

    def test_block_has_header(self, block_with_transactions):
        """Test that block has a properly formed header."""
        assert block_with_transactions.header is not None
        assert hasattr(block_with_transactions.header, 'hash')
        assert hasattr(block_with_transactions.header, 'previous_hash')
        assert hasattr(block_with_transactions.header, 'merkle_root')

    def test_block_has_valid_hash(self, block_with_transactions):
        """Test that block has a non-empty hash."""
        assert block_with_transactions.hash is not None
        assert len(block_with_transactions.hash) > 0

    def test_genesis_block_creation(self):
        """Test creating a genesis block (index 0, empty transactions)."""
        genesis_block = Block(0, "0" * 64, [])
        genesis_block.build_merkle_tree()
        genesis_block.calculate_hash()
        assert genesis_block.index == 0
        assert len(genesis_block.transactions) == 0

    def test_block_to_dict(self, block_with_transactions):
        """Test converting block to dictionary representation."""
        block_dict = block_with_transactions.to_dict()
        assert block_dict['index'] == 0
        assert block_dict['hash'] == block_with_transactions.hash
        assert block_dict['previous_hash'] == "0" * 64
        assert 'merkle_root' in block_dict
        assert 'transactions' in block_dict
        assert len(block_dict['transactions']) == 4


class TestBlockValidation:
    """Tests for block validation and tamper detection."""

    def test_valid_block_passes_validation(self, block_with_transactions):
        """Test that a valid block passes validation."""
        assert block_with_transactions.validate() is True

    def test_block_becomes_invalid_after_transaction_tampering(self, sample_transactions):
        """Test that tampering with a transaction invalidates the block."""
        block = Block(0, "0" * 64, sample_transactions)
        block.build_merkle_tree()
        block.calculate_hash()
        
        # Verify block is valid initially
        assert block.validate() is True
        
        # Tamper with a transaction (without recalculating hash - simulating undetected tampering)
        tampered_tx = Transaction(None, None, 0, "Tampering_tx!")
        block.transactions[1] = tampered_tx
        
        # Block should now be invalid
        assert block.validate() is False

    def test_block_recalculation_after_transaction_change(self, sample_transactions):
        """Test that block remains valid after tampering if merkle tree is rebuilt."""
        block = Block(0, "0" * 64, sample_transactions)
        block.build_merkle_tree()
        block.calculate_hash()
        
        initial_hash = block.hash
        assert block.validate() is True
        
        # Tamper with a transaction AND rebuild merkle tree
        tampered_tx = Transaction(None, None, 0, "Tampering_tx!")
        block.transactions[1] = tampered_tx
        block.merkle_tree = None
        block.build_merkle_tree()
        block.header.merkle_root = block.merkle_tree.root.hash if block.merkle_tree and block.merkle_tree.root else ""
        block.calculate_hash()
        
        # Block should still be valid (because we rebuilt everything)
        assert block.validate() is True
        # But hash should have changed
        assert block.hash != initial_hash


class TestBlockMerkleTree:
    """Tests for block's merkle tree functionality."""

    def test_block_builds_merkle_tree(self, block_with_transactions):
        """Test that block has a built merkle tree."""
        assert block_with_transactions.merkle_tree is not None
        assert block_with_transactions.merkle_tree.root is not None

    def test_merkle_root_stored_in_header(self, block_with_transactions):
        """Test that merkle root is properly stored in block header."""
        expected_root = block_with_transactions.merkle_tree.root.hash
        assert block_with_transactions.header.merkle_root == expected_root

    def test_empty_block_has_no_merkle_tree(self):
        """Test that a block with no transactions has no merkle tree."""
        block = Block(0, "0" * 64, [])
        block.build_merkle_tree()
        # Empty block should have None merkle tree (no transactions to hash)
        assert block.merkle_tree is None
