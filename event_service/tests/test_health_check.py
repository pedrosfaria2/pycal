import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db


@pytest.fixture(scope="function")
def client_with_db(db_session: Session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_without_db():
    app.dependency_overrides[get_db] = lambda: None
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_health_check_with_db(client_with_db):
    response = client_with_db.get("/health")
    assert response.status_code == 200, "The health check should return 200 OK"
    data = response.json()
    assert data["status"] == "healthy", "The status should be 'healthy'"
    assert data["db_status"] == "connected", "The db_status should be 'connected'"


def test_health_check_without_db(client_without_db):
    response = client_without_db.get("/health")
    assert response.status_code == 500, "The health check should return 500 when the DB is not available"
    data = response.json()
    detail = data.get("detail", {})
    assert "status" in detail, "The response should contain 'status' key"
    assert detail["status"] == "unhealthy", "The status should be 'unhealthy'"
    assert detail["db_status"] == "disconnected", "The db_status should be 'disconnected'"
    assert "error" in detail, "The response should contain 'error' key"
