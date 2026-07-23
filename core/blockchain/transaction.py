from datetime import datetime

from ..shared.hashable import Hashable

class Transaction(Hashable):
    # Represents a transaction in the blockchain
    def __init__(
            self,
            sender,
            receiver,
            amount,
            metadata
            ):
        super().__init__()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()
        self.metadata = metadata
        self.hash = self.calculate_hash()

    # Convert the transaction to a dictionary representation
    def to_dict(self):
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
        self.hash = data.get("hash")
        self.sender = data.get("sender")
        self.receiver = data.get("receiver")
        self.amount = data.get("amount")
        self.timestamp = datetime.fromisoformat(data.get("timestamp"))
        self.metadata = data.get("metadata")