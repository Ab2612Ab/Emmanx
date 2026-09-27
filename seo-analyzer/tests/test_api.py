from fastapi.testclient import TestClient
from api.index import app

client=TestClient(app)

def test_root():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()["python"] is True

def test_health():
    assert client.get("/health").json()["status"]=="healthy"
