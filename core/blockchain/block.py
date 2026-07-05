from ..shared.hashable import Hashable

class Block(Hashable):
    def __init__(self):
        super().__init__()
        self.header = None
        self.merkle_tree = None
        self.transactions = []

    def calculate_hash(self):
        pass

    def rebuild_merkle_tree(self):
        pass

    def mine(self):
        pass

    def validate(self):
        pass