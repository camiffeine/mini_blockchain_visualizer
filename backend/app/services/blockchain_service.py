from core.blockchain.blockchain import Blockchain, Transaction
from core.crypto.merkle import MerkleTree

from ..schemas.blockchain_schemas import BlockchainStatusResponse, BlockchainGetBlockchainResponse
from ..schemas.block_schemas import BlockResponse, BlockResponseWithoutMerkleTree
from ..schemas.merkle_schemas import MerkleNodeResponse, MerkleTreeResponse, MerkleProofResponse, ProofStepResponse, MerkleProofVerificationResponse
from ..schemas.transaction_schemas import TransactionRequest, TransactionResponse


class BlockchainService:
    def __init__(self):
        self.blockchain = Blockchain()

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

    def tamper_transaction(self, block_index: int, transaction_index: int, new_transaction: TransactionRequest):
        block = self.blockchain.get_block(block_index)
        if block is None:
            return None
        if transaction_index < 0 or transaction_index >= len(block.transactions):
            return None

        tampered_transaction = Transaction(
            sender=new_transaction.sender,
            receiver=new_transaction.receiver,
            amount=new_transaction.amount,
            metadata=new_transaction.metadata
        )
        block.transactions[transaction_index] = tampered_transaction

        return TransactionResponse(
            sender=tampered_transaction.sender,
            receiver=tampered_transaction.receiver,
            amount=tampered_transaction.amount,
            metadata=tampered_transaction.metadata,
            timestamp=tampered_transaction.timestamp,
            hash=tampered_transaction.hash
        )

    def create_block(self):
        new_block = self.blockchain.create_block()
        return BlockResponse(
            index=new_block.header.index,
            valid=new_block.validate(),
            timestamp=new_block.header.timestamp,
            merkle_root=new_block.header.merkle_root,
            nonce=new_block.header.nonce,
            difficulty=new_block.header.difficulty,
            previous_hash=new_block.header.previous_hash,
            hash=new_block.header.hash,
            transactions=[TransactionResponse(**tx.to_dict()) for tx in new_block.transactions] if new_block.transactions else [],
            merkle_tree=self.merkle_tree_to_response(new_block.merkle_tree),
        )

    def get_status(self):
        pending_transactions = []
        for tx in self.blockchain.pending_transactions:
            pending_transactions.append(TransactionResponse(
                sender=tx.sender,
                receiver=tx.receiver,
                amount=tx.amount,
                metadata=tx.metadata,
                timestamp=tx.timestamp,
                hash=tx.hash
            ))

        if self.blockchain.get_last_block():
            return BlockchainStatusResponse(
                blockchain_valid=self.blockchain.validate_chain(),
                chain_length=self.blockchain.chain.length,
                last_block_index=self.blockchain.get_last_block().header.index,
                last_block_hash=self.blockchain.get_last_block().header.hash,
                pending_transactions=pending_transactions,
            )
        else:
            return BlockchainStatusResponse(
                blockchain_valid=self.blockchain.validate_chain(),
                chain_length=self.blockchain.chain.length,
                last_block_index=None,
                last_block_hash=None,
                pending_transactions=pending_transactions,
                message="Blockchain is empty.",
            )

    def get_blockchain(self):
         chain_data = self.blockchain.get_chain()
         chain_response = BlockchainGetBlockchainResponse(chain=[])
         for block in chain_data:
                block_response = BlockResponseWithoutMerkleTree(
                    index=block["index"],
                    valid=block["valid"],
                    timestamp=block["timestamp"],
                    merkle_root=block["merkle_root"],
                    nonce=block["nonce"],
                    difficulty=block["difficulty"],
                    previous_hash=block["previous_hash"],
                    hash=block["hash"],
                    transactions=[TransactionResponse(**tx) for tx in block["transactions"]] if block["transactions"] else [],
                )
                chain_response.chain.append(block_response)
         return chain_response

    def merkle_node_to_response(self, node):
        if node is None:
            return None
        return MerkleNodeResponse(
            hash=node.hash,
            left=self.merkle_node_to_response(node.left),
            right=self.merkle_node_to_response(node.right),
        )

    def merkle_tree_to_response(self, tree):
        if tree is None or tree.root is None:
            return None
        return MerkleTreeResponse(
            root=self.merkle_node_to_response(tree.root)
        )

    def get_block(self, index: int):
        block = self.blockchain.get_block(index)
        if block:
            return BlockResponse(
            index=block.header.index,
            valid=block.validate(),
            timestamp=block.header.timestamp,
            merkle_root=block.header.merkle_root,
            nonce=block.header.nonce,
            difficulty=block.header.difficulty,
            previous_hash=block.header.previous_hash,
            hash=block.header.hash,
            transactions=[TransactionResponse(**tx.to_dict()) for tx in block.transactions] if block.transactions else [],
            merkle_tree=self.merkle_tree_to_response(block.merkle_tree),
            )
        else:
            return None

    def merkle_proof_to_response(self, proof):
        return MerkleProofResponse(
            transaction_hash=proof.transaction_hash,
            merkle_root=proof.merkle_root,
            proof_steps=[
                ProofStepResponse(
                    hash=step.sibling_hash,
                    direction=step.position.value,
                )
                for step in proof.proof_steps
            ],
        )

    def get_merkle_proof(self, block_index: int, transaction_index: int):
        block = self.blockchain.get_block(block_index)
        if block is None:
            return None
        if transaction_index < 0 or transaction_index >= len(block.transactions):
            return None

        current_tree = MerkleTree()
        current_tree.build_tree(block.transactions)
        if current_tree.root is None:
            return None

        proof = current_tree.generate_proof(transaction_index)
        proof_response = self.merkle_proof_to_response(proof)

        leaf_hash = current_tree.leaves[transaction_index].hash
        is_valid = block.validate() and MerkleTree.verify_proof(leaf_hash, proof, block.header.merkle_root)

        return MerkleProofVerificationResponse(
            proof=proof_response,
            valid=is_valid
        )