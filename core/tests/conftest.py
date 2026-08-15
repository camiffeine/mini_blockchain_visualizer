"""
Pytest configuration and fixtures for blockchain tests.
"""

import pytest
from core.blockchain.transaction import Transaction
from core.blockchain.block import Block
from core.blockchain.blockchain import Blockchain


@pytest.fixture
def sample_transactions():
    """Fixture providing sample transactions for testing."""
    return [
        Transaction(None, None, 0, "Hola"),
        Transaction(None, None, 0, "Criptografía"),
        Transaction(None, None, 0, "Post-cuántica"),
        Transaction(None, None, 0, "UNAL!"),
    ]


@pytest.fixture
def blockchain_instance():
    """Fixture providing a fresh blockchain instance for each test."""
    return Blockchain()


@pytest.fixture
def block_with_transactions(sample_transactions):
    """Fixture providing a block with sample transactions."""
    block = Block(0, "0" * 64, sample_transactions)
    block.build_merkle_tree()
    block.calculate_hash()
    return block
