from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_find_email_patterns():
    response = client.post(
        "/find-email",
        json={"first_name": "Taiwo", "last_name": "Emmanuel", "domain": "example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["candidates"][0]["email"] == "taiwo.emmanuel@example.com"
    assert len(data["candidates"]) == 5


def test_lead_scoring():
    response = client.post(
        "/score-lead",
        json={
            "company": "Acme Studio",
            "website": "https://example.com",
            "email": "hello@example.com",
            "job_title": "Founder",
            "industry": "Software",
            "company_size": 20,
            "location": "Toronto",
        },
    )
    assert response.status_code == 200
    assert response.json()["score"] == 100
    assert response.json()["grade"] == "A"


def test_invalid_email():
    response = client.post(
        "/verify-email",
        json={"email": "not-an-email"},
    )
    assert response.status_code == 422
