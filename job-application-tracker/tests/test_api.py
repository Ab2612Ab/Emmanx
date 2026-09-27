from fastapi.testclient import TestClient

from api.index import app, applications

client = TestClient(app)


def setup_function():
    applications.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_application():
    payload = {
        "company": "Acme Labs",
        "role": "Frontend Developer",
        "location": "Remote",
        "contact_email": "recruiter@example.com",
        "salary_min": 70000,
        "salary_max": 90000,
    }

    created = client.post("/applications", json=payload)
    assert created.status_code == 201

    application = created.json()
    assert application["company"] == "Acme Labs"
    assert application["status"] == "applied"

    fetched = client.get(f"/applications/{application['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == application["id"]


def test_status_update_and_dashboard():
    created = client.post(
        "/applications",
        json={"company": "Example Inc", "role": "Python Developer"},
    )
    application_id = created.json()["id"]

    updated = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "interview"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "interview"

    dashboard = client.get("/dashboard")
    assert dashboard.status_code == 200
    assert dashboard.json()["total_applications"] == 1
    assert dashboard.json()["by_status"]["interview"] == 1


def test_invalid_salary_range():
    response = client.post(
        "/applications",
        json={
            "company": "Bad Range Co",
            "role": "Developer",
            "salary_min": 100000,
            "salary_max": 50000,
        },
    )
    assert response.status_code == 422
