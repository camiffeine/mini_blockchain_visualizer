from ..services.blockchain_service import BlockchainService

class AppState:
    def __init__(self):
        self.blockchain_service = BlockchainService()

app_state = AppState()

def get_blockchain_service():
    return app_state.blockchain_service