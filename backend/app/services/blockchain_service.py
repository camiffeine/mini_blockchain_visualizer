from core.blockchain.blockchain import Blockchain, Transaction

from ..schemas.blockchain_schemas import BlockchainStatusResponse
from ..schemas.transaction_schemas import TransactionRequest, TransactionResponse

class BlockchainService:
    def __init__(self):
        self.blockchain = Blockchain()

    def get_status(self):
        if self.blockchain.get_last_block():
            return BlockchainStatusResponse(
                blockchain_valid=self.blockchain.validate_chain(),
                chain_length=self.blockchain.chain.length,
                last_block_index=self.blockchain.get_last_block().header.index,
                last_block_hash=self.blockchain.get_last_block().header.hash,
                pending_transactions=self.blockchain.pending_transactions,
            )
        else:
            return BlockchainStatusResponse(
                blockchain_valid=self.blockchain.validate_chain(),
                chain_length=self.blockchain.chain.length,
                last_block_index=None,
                last_block_hash=None,
                pending_transactions=self.blockchain.pending_transactions,
                message="Blockchain is empty.",
            )

    def add_transaction(self, transaction: TransactionRequest):
        new_transaction = Transaction(
            sender=transaction.sender,
            receiver=transaction.receiver,
            amount=transaction.amount,
            metadata=transaction.metadata
        )
        self.blockchain.add_transaction(new_transaction)
        return TransactionResponse(
            sender=new_transaction.sender,
            receiver=new_transaction.receiver,
            amount=new_transaction.amount,
            metadata=new_transaction.metadata,
            timestamp=new_transaction.timestamp,
            hash=new_transaction.hash
        )
