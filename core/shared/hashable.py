from ..crypto.hashing import sha256, hash_object
from ..utils.serializer import Serializer

class Hashable:
    def __init__(self):
        self.hash = None

    # Subclasses must implement the to_dict() and from_dict() methods to convert the object to and from a dictionary representation.
    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict() method.")

    def from_dict(self, data):
        raise NotImplementedError("Subclasses must implement from_dict() method.")

    # Serialize the object to a JSON string using the Serializer class.
    def serialize(self):
        return Serializer.serialize(self.to_dict())

    # Calculate the SHA-256 hash of the serialized object and store it in the hash attribute.
    def calculate_hash(self):
        # Serialize the object to a JSON string and calculate the SHA-256 hash
        self.hash = sha256(hash_object(self.to_dict()).encode())