import hashlib
from ..utils.serializer import Serializer

# Encode a given string of text using hashlib
def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# Encode a given string of text using hashlib twice (double SHA-256)
def double_sha256(data: bytes) -> str:
    first = hashlib.sha256(data).digest()
    return hashlib.sha256(first).hexdigest()

# Serialize an object and calculate its SHA-256 hash
def hash_object(obj) -> str:
    serialized = Serializer.serialize(obj)
    return sha256(serialized.encode())