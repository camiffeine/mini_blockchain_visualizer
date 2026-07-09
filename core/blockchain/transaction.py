from ..shared.hashable import Hashable

class Transaction(Hashable):
    # Represents a transaction in the blockchain
    def __init__(self, metadata):
        super().__init__()
        self.sender = None
        self.receiver = None
        self.amount = None
        self.timestamp = None
        self.metadata = metadata
        self.hash = self.calculate_hash()

    # Convert the transaction to a dictionary representation
    def to_dict(self):
        return {
            "hash": self.hash,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

    # Populate the transaction from a dictionary representation
    def from_dict(self, data):
        self.hash = data.get("hash")
        self.sender = data.get("sender")
        self.receiver = data.get("receiver")
        self.amount = data.get("amount")
        self.timestamp = data.get("timestamp")
        self.metadata = data.get("metadata")