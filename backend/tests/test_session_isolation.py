from fastapi.testclient import TestClient

from backend.app.main import app


def test_different_sessions_have_isolated_blockchains():
    client_1 = TestClient(app)
    client_2 = TestClient(app)

    transaction = {
        "sender": "alice",
        "receiver": "bob",
        "amount": 10,
        "metadata": "session 1 tx",
    }

    response = client_1.post("/transactions/add", json=transaction)
    assert response.status_code == 201, response.text

    status_1 = client_1.get("/blockchain/status")
    status_2 = client_2.get("/blockchain/status")

    assert status_1.status_code == 200, status_1.text
    assert status_2.status_code == 200, status_2.text
    assert len(status_1.json()["pending_transactions"]) == 1
    assert len(status_2.json()["pending_transactions"]) == 0
