from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200

def test_chat_basic():
    payload = {
        "messages": [
            {"role": "user", "content": "I want to book an appointment"}
        ]
    }
    resp = client.post("/api/chat/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "appointment" in data["reply"].lower()

