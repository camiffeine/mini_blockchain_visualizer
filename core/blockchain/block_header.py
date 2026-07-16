from dataclasses import dataclass
from ..shared.hashable import Hashable
from ..crypto.hashing import sha256, hash_object

@dataclass()
class BlockHeader(Hashable):
    index: int
    timestamp: float
    merkle_root: str
    nonce: int
    difficulty: int
    hash: str | None
    previous_hash: str

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "hash": self.hash,
            "previous_hash": self.previous_hash
        }

    def to_hash_dict(self):  # For hashing purposes only
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "previous_hash": self.previous_hash
        }

    def calculate_hash(self):
        h = sha256(hash_object(self.to_hash_dict()).encode())
        self.hash = h
        return h

    def from_dict(self, data):
        return BlockHeader(
            index=data.get("index"),
            timestamp=data.get("timestamp"),
            merkle_root=data.get("merkle_root"),
            nonce=data.get("nonce"),
            difficulty=data.get("difficulty"),
            hash=data.get("hash"),
            previous_hash=data.get("previous_hash")
        )