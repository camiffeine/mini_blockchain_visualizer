"""
Custom exceptions for the blockchain system.

This module defines all custom exceptions used throughout the blockchain
application for better error handling and reporting.
"""


class BlockchainException(Exception):
    """Base exception for all blockchain-related errors."""
    pass


class TransactionError(BlockchainException):
    """Exception raised when there's an error with a transaction."""
    pass


class InvalidBlockError(BlockchainException):
    """Exception raised when a block is invalid or fails validation."""
    pass


class BlockchainValidationError(BlockchainException):
    """Exception raised when the blockchain chain fails validation."""
    pass
