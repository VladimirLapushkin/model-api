from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body


def test_predict_validation():
    payload = {
        "transaction_id": 1,
        "customer_id": 1001,
        "terminal_id": 501,
        "tx_amount": 250.75,
        "tx_time_seconds": 36000,
        "tx_time_days": 12,
        "tx_fraud_scenario": 0
    }

    response = client.post("/predict", json=payload)
    assert response.status_code in (200, 503)
