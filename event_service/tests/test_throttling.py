import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.middleware.throttling import apply_throttling, limiter
from app.routers import events


@pytest.fixture(scope="function")
def client_with_throttling():
    app = FastAPI()
    apply_throttling(app)
    app.include_router(events.router)
    return TestClient(app)


def test_throttling(client_with_throttling):
    client = client_with_throttling

    max_requests = client.app.state.max_requests

    url = "/events/"

    for i in range(max_requests):
        response = client.get(url)
        assert response.status_code != 429, f"Failed on attempt {i + 1} with status {response.status_code}"

    response = client.get(url)
    assert response.status_code == 429
