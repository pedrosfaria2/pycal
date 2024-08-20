from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base


def test_create_event(client: TestClient):
    response = client.post("/events/", json={
        "title": "Test Event",
        "description": "This is a test event.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Event"
    assert data["description"] == "This is a test event."


def test_read_events(client: TestClient):
    client.post("/events/", json={
        "title": "Test Event",
        "description": "This is a test event.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    
    response = client.get("/events/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0


def test_read_event(client: TestClient):
    response = client.post("/events/", json={
        "title": "Test Event",
        "description": "This is a test event.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    event_id = response.json()["id"]
    
    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event_id
    assert data["title"] == "Test Event"


def test_update_event(client: TestClient):
    response = client.post("/events/", json={
        "title": "Test Event",
        "description": "This is a test event.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    event_id = response.json()["id"]

    response = client.put(f"/events/{event_id}", json={
        "title": "Updated Test Event",
        "description": "This is an updated test event.",
        "start_time": "2024-08-20T11:00:00",
        "end_time": "2024-08-20T13:00:00",
        "location": "Updated Location",
        "participants": ["Alice", "Bob", "Charlie"]
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Test Event"
    assert data["location"] == "Updated Location"


def test_delete_event(client: TestClient):
    response = client.post("/events/", json={
        "title": "Test Event",
        "description": "This is a test event.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    event_id = response.json()["id"]

    response = client.delete(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event_id

    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
