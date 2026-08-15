"""
Unit tests for Blockchain class.
"""

import pytest
from core.blockchain.transaction import Transaction
from core.blockchain.blockchain import Blockchain
from core.exceptions import BlockchainException, TransactionError, InvalidBlockError


class TestBlockchainCreation:
    """Tests for blockchain initialization."""

    def test_blockchain_creates_genesis_block(self, blockchain_instance):
        """Test that blockchain creates a genesis block on initialization."""
        assert blockchain_instance.chain.head is not None
        genesis_block = blockchain_instance.chain.head.block
        assert genesis_block.index == 0
        assert len(genesis_block.transactions) == 0

    def test_blockchain_has_empty_pending_transactions(self, blockchain_instance):
        """Test that new blockchain starts with no pending transactions."""
        assert len(blockchain_instance.pending_transactions) == 0

    def test_blockchain_chain_length_after_genesis(self, blockchain_instance):
        """Test that blockchain length is 1 after genesis block creation."""
        assert blockchain_instance.chain.length == 1

    def test_get_genesis_block(self, blockchain_instance):
        """Test retrieving the genesis block."""
        genesis = blockchain_instance.get_block(0)
        assert genesis is not None
        assert genesis.index == 0


class TestBlockchainTransactions:
    """Tests for adding transactions to blockchain."""

    def test_add_valid_transaction(self, blockchain_instance, sample_transactions):
        """Test adding a valid transaction to pending transactions."""
        blockchain_instance.add_transaction(sample_transactions[0])
        assert len(blockchain_instance.pending_transactions) == 1

    def test_add_multiple_transactions(self, blockchain_instance, sample_transactions):
        """Test adding multiple transactions."""
        # Add only 3 transactions to avoid triggering auto-block creation (MAX=4)
        for i in range(3):
            blockchain_instance.add_transaction(sample_transactions[i])
        assert len(blockchain_instance.pending_transactions) == 3

    def test_add_invalid_transaction_raises_error(self, blockchain_instance):
        """Test that adding an invalid transaction raises TransactionError."""
        with pytest.raises(TransactionError):
            blockchain_instance.add_transaction("not a transaction")

    def test_invalid_transaction_prevents_block_creation(self, blockchain_instance):
        """Test that invalid transaction doesn't get added."""
        initial_count = len(blockchain_instance.pending_transactions)
        with pytest.raises(TransactionError):
            blockchain_instance.add_transaction(None)
        assert len(blockchain_instance.pending_transactions) == initial_count

    def test_create_block_with_no_pending_transactions_raises_error(self, blockchain_instance):
        """Test that creating a block with no pending transactions raises error."""
        with pytest.raises(BlockchainException):
            blockchain_instance.create_block()

    def test_create_block_with_pending_transactions(self, blockchain_instance, sample_transactions):
        """Test creating a block with pending transactions."""
        # Add 3 transactions (less than max 4)
        for i in range(3):
            blockchain_instance.add_transaction(sample_transactions[i])
        
        # Manually create block
        block = blockchain_instance.create_block()
        assert block is not None
        assert block.index == 1
        assert len(block.transactions) == 3
        assert len(blockchain_instance.pending_transactions) == 0

    def test_auto_block_creation_on_max_transactions(self, blockchain_instance, sample_transactions):
        """Test that block is automatically created when max transactions reached."""
        # Add exactly MAX_TRANSACTIONS_PER_BLOCK transactions
        for i in range(4):
            blockchain_instance.add_transaction(sample_transactions[i])
        
        # After 4th transaction, block should be created and pending list cleared
        assert len(blockchain_instance.pending_transactions) == 0
        assert blockchain_instance.chain.length == 2  # Genesis + first block


class TestBlockchainValidation:
    """Tests for blockchain validation."""

    def test_valid_blockchain_after_genesis(self, blockchain_instance):
        """Test that blockchain is valid right after creation."""
        assert blockchain_instance.validate_chain() is True

    def test_valid_blockchain_after_adding_block(self, blockchain_instance, sample_transactions):
        """Test that blockchain remains valid after adding a block."""
        for i in range(3):
            blockchain_instance.add_transaction(sample_transactions[i])
        blockchain_instance.create_block()
        assert blockchain_instance.validate_chain() is True

    def test_invalid_blockchain_after_tampering(self, blockchain_instance, sample_transactions):
        """Test that blockchain becomes invalid after tampering with a block."""
        for i in range(3):
            blockchain_instance.add_transaction(sample_transactions[i])
        blockchain_instance.create_block()
        
        # Verify initial state is valid
        assert blockchain_instance.validate_chain() is True
        
        # Tamper with a transaction in block 1 without rebuilding
        block = blockchain_instance.get_block(1)
        tampered_tx = Transaction(None, None, 0, "Tampering_tx!")
        block.transactions[0] = tampered_tx
        
        # Now blockchain should be invalid
        assert blockchain_instance.validate_chain() is False


class TestBlockchainTampering:
    """Tests for the tamper_transaction method."""

    def test_tamper_transaction_valid_indices(self, blockchain_instance, sample_transactions):
        """Test tampering with a transaction at valid indices."""
        for tx in sample_transactions:
            blockchain_instance.add_transaction(tx)
        
        new_tx = Transaction(None, None, 0, "Tampered!")
        blockchain_instance.tamper_transaction(1, 0, new_tx)
        
        block = blockchain_instance.get_block(1)
        assert block.transactions[0].metadata == "Tampered!"

    def test_tamper_transaction_rebuilds_merkle_tree(self, blockchain_instance, sample_transactions):
        """Test that tampering rebuilds the merkle tree."""
        for tx in sample_transactions:
            blockchain_instance.add_transaction(tx)
        
        block_before = blockchain_instance.get_block(1)
        hash_before = block_before.hash
        
        new_tx = Transaction(None, None, 0, "Tampered!")
        blockchain_instance.tamper_transaction(1, 0, new_tx)
        
        block_after = blockchain_instance.get_block(1)
        assert block_after.validate() is True  # Should be valid because merkle tree was rebuilt
        assert block_after.hash != hash_before  # Hash should change

    def test_tamper_transaction_invalid_block_index(self, blockchain_instance, sample_transactions):
        """Test tampering with invalid block index raises error."""
        for tx in sample_transactions:
            blockchain_instance.add_transaction(tx)
        
        new_tx = Transaction(None, None, 0, "Tampered!")
        with pytest.raises(InvalidBlockError):
            blockchain_instance.tamper_transaction(999, 0, new_tx)

    def test_tamper_transaction_invalid_tx_index(self, blockchain_instance, sample_transactions):
        """Test tampering with invalid transaction index raises error."""
        for tx in sample_transactions:
            blockchain_instance.add_transaction(tx)
        
        new_tx = Transaction(None, None, 0, "Tampered!")
        with pytest.raises(InvalidBlockError):
            blockchain_instance.tamper_transaction(1, 999, new_tx)


class TestBlockchainChainRetrieval:
    """Tests for blockchain chain retrieval methods."""

    def test_get_last_block(self, blockchain_instance, sample_transactions):
        """Test getting the last block in the blockchain."""
        for i in range(3):
            blockchain_instance.add_transaction(sample_transactions[i])
        blockchain_instance.create_block()
        
        last_block = blockchain_instance.get_last_block()
        assert last_block.index == 1

    def test_get_chain_as_list(self, blockchain_instance, sample_transactions):
        """Test getting entire chain as list of dictionaries."""
        for i in range(3):
            blockchain_instance.add_transaction(sample_transactions[i])
        blockchain_instance.create_block()
        
        chain_data = blockchain_instance.get_chain()
        assert len(chain_data) == 2  # Genesis + 1 block
        assert chain_data[0]['index'] == 0
        assert chain_data[1]['index'] == 1
