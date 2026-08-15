from datetime import datetime

from ..shared.hashable import Hashable
from ..exceptions import TransactionError


class Transaction(Hashable):
    """
    Represents a transaction in the blockchain.
    
    A transaction contains information about a transfer from a sender to a receiver,
    with an amount and optional metadata. Each transaction is immutable and has a
    unique hash calculated from its contents.
    
    Attributes:
        sender: The sender of the transaction (can be None for genesis transactions)
        receiver: The receiver of the transaction (can be None for genesis transactions)
        amount: The amount being transferred (must be > 0 if sender/receiver are set)
        metadata: Additional information about the transaction
        timestamp: The time when the transaction was created
        hash: The SHA-256 hash of the transaction
    """
    
    def __init__(
            self,
            sender,
            receiver,
            amount,
            metadata
            ):
        """
        Initialize a new transaction.
        
        Args:
            sender: The sender of the transaction
            receiver: The receiver of the transaction
            amount: The amount being transferred
            metadata: Additional information about the transaction
            
        Raises:
            TransactionError: If validation fails (invalid amount, etc.)
        """
        super().__init__()
        self._validate_transaction(sender, receiver, amount)
        
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()
        self.metadata = metadata
        self.hash = self.calculate_hash()
    
    @staticmethod
    def _validate_transaction(sender, receiver, amount):
        """
        Validate transaction parameters.
        
        Args:
            sender: The sender of the transaction
            receiver: The receiver of the transaction
            amount: The amount being transferred
            
        Raises:
            TransactionError: If any validation check fails
        """
        # If both sender and receiver are None, it's a genesis/sample transaction (allowed)
        if sender is None and receiver is None:
            if amount < 0:
                raise TransactionError(f"Amount cannot be negative: {amount}")
            return
        
        # If either sender or receiver is set, validate both
        if sender is None or receiver is None:
            raise TransactionError("Both sender and receiver must be provided together (or both None)")
        
        if not isinstance(sender, str) or not sender.strip():
            raise TransactionError(f"Sender must be a non-empty string: {sender}")
        
        if not isinstance(receiver, str) or not receiver.strip():
            raise TransactionError(f"Receiver must be a non-empty string: {receiver}")
        
        if not isinstance(amount, (int, float)):
            raise TransactionError(f"Amount must be a number: {amount}")
        
        if amount <= 0:
            raise TransactionError(f"Amount must be greater than 0: {amount}")

    # Convert the transaction to a dictionary representation
    def to_dict(self):
        """
        Convert the transaction to a dictionary representation.
        
        Returns:
            dict: A dictionary containing all transaction data with keys:
                - hash: The transaction hash
                - sender: The sender
                - receiver: The receiver
                - amount: The transfer amount
                - timestamp: ISO format timestamp
                - metadata: Additional metadata
        """
        return {
            "hash": self.hash,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    # Populate the transaction from a dictionary representation
    def from_dict(self, data):
        """
        Populate the transaction from a dictionary representation.
        
        Args:
            data: Dictionary containing transaction data
        """
        self.hash = data.get("hash")
        self.sender = data.get("sender")
        self.receiver = data.get("receiver")
        self.amount = data.get("amount")
        self.timestamp = datetime.fromisoformat(data.get("timestamp"))
        self.metadata = data.get("metadata")