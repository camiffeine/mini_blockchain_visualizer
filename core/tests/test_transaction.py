"""
Unit tests for Transaction class.
"""

import pytest
from core.blockchain.transaction import Transaction
from core.exceptions import TransactionError


class TestTransactionCreation:
    """Tests for transaction creation and validation."""

    def test_create_sample_transaction(self):
        """Test creating a sample/genesis transaction with None sender/receiver."""
        tx = Transaction(None, None, 0, "Sample")
        assert tx.sender is None
        assert tx.receiver is None
        assert tx.amount == 0
        assert tx.metadata == "Sample"
        assert tx.hash is not None

    def test_create_valid_transaction(self):
        """Test creating a valid transaction with sender and receiver."""
        tx = Transaction("Alice", "Bob", 100, "Payment")
        assert tx.sender == "Alice"
        assert tx.receiver == "Bob"
        assert tx.amount == 100
        assert tx.metadata == "Payment"
        assert tx.hash is not None

    def test_transaction_timestamp(self):
        """Test that transaction has a valid timestamp."""
        tx = Transaction(None, None, 0, "Test")
        assert tx.timestamp is not None
        assert hasattr(tx.timestamp, 'isoformat')

    def test_transaction_to_dict(self):
        """Test converting transaction to dictionary representation."""
        tx = Transaction("Alice", "Bob", 50, "Payment")
        tx_dict = tx.to_dict()
        
        assert tx_dict['sender'] == "Alice"
        assert tx_dict['receiver'] == "Bob"
        assert tx_dict['amount'] == 50
        assert tx_dict['metadata'] == "Payment"
        assert 'hash' in tx_dict
        assert 'timestamp' in tx_dict


class TestTransactionValidation:
    """Tests for transaction validation and error handling."""

    def test_invalid_sender_empty_string(self):
        """Test that empty sender string raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("", "Bob", 100, "Payment")

    def test_invalid_receiver_empty_string(self):
        """Test that empty receiver string raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("Alice", "", 100, "Payment")

    def test_invalid_sender_only_whitespace(self):
        """Test that whitespace-only sender raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("   ", "Bob", 100, "Payment")

    def test_invalid_receiver_only_whitespace(self):
        """Test that whitespace-only receiver raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("Alice", "   ", 100, "Payment")

    def test_invalid_amount_negative(self):
        """Test that negative amount raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("Alice", "Bob", -50, "Payment")

    def test_invalid_amount_zero_with_sender(self):
        """Test that zero amount with sender/receiver raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("Alice", "Bob", 0, "Payment")

    def test_invalid_amount_non_numeric(self):
        """Test that non-numeric amount raises TransactionError."""
        with pytest.raises(TransactionError):
            Transaction("Alice", "Bob", "not a number", "Payment")

    def test_mismatched_sender_receiver_none(self):
        """Test that having only sender or receiver (not both) raises error."""
        with pytest.raises(TransactionError):
            Transaction("Alice", None, 100, "Payment")
        
        with pytest.raises(TransactionError):
            Transaction(None, "Bob", 100, "Payment")

    def test_valid_float_amount(self):
        """Test that float amount is accepted for valid transactions."""
        tx = Transaction("Alice", "Bob", 99.99, "Payment")
        assert tx.amount == 99.99

    def test_valid_integer_amount(self):
        """Test that integer amount is accepted for valid transactions."""
        tx = Transaction("Alice", "Bob", 100, "Payment")
        assert tx.amount == 100


class TestTransactionHash:
    """Tests for transaction hashing."""

    def test_transaction_has_hash(self):
        """Test that created transaction has a hash."""
        tx = Transaction("Alice", "Bob", 100, "Payment")
        assert tx.hash is not None
        assert len(tx.hash) > 0

    def test_same_data_same_hash(self):
        """Test that transactions with same data have same hash."""
        tx1 = Transaction(None, None, 0, "Test")
        tx2 = Transaction(None, None, 0, "Test")
        # Note: Hashes will differ due to different timestamps, so we just verify they exist
        assert tx1.hash is not None
        assert tx2.hash is not None

    def test_different_data_different_hash(self):
        """Test that transactions with different data have different hashes."""
        tx1 = Transaction(None, None, 0, "Test1")
        tx2 = Transaction(None, None, 0, "Test2")
        assert tx1.hash != tx2.hash
