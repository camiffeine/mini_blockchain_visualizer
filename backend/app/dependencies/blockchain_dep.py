from ..services.blockchain_service import BlockchainService

blockchain_service = BlockchainService()

def get_blockchain_service():
    return blockchain_service