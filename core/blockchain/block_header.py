from dataclasses import dataclass
from ..shared.hashable import Hashable

@dataclass(frozen=True)
class BlockHeader(Hashable):
    index: int
    timestamp: float
    merkle_root: str
    nonce: int
    difficulty: int
    block_hash: str
    previous_hash: str

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "block_hash": self.block_hash,
            "previous_hash": self.previous_hash
        }

    def from_dict(self, data):
        return BlockHeader(
            index=data.get("index"),
            timestamp=data.get("timestamp"),
            merkle_root=data.get("merkle_root"),
            nonce=data.get("nonce"),
            difficulty=data.get("difficulty"),
            block_hash=data.get("block_hash"),
            previous_hash=data.get("previous_hash")
        )