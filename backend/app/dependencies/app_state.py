import uuid

from fastapi import Request

from ..services.blockchain_service import BlockchainService


class AppState:
    def __init__(self):
        self.blockchain_services = {}


app_state = AppState()


def get_blockchain_service(request: Request):
    session = request.session
    session_id = session.get("blockchain_session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        session["blockchain_session_id"] = session_id

    if session_id not in app_state.blockchain_services:
        app_state.blockchain_services[session_id] = BlockchainService()

    return app_state.blockchain_services[session_id]