from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

def test_create_event_with_empty_title():
    response = client.post("/events/", json={
        "title": "",  # Título vazio
        "description": "Event with empty title",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_event_with_invalid_dates():
    response = client.post("/events/", json={
        "title": "Invalid Dates Event",
        "description": "Event with invalid start and end times",
        "start_time": "2024-08-20T12:00:00",
        "end_time": "2024-08-20T10:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_event_with_too_long_title():
    long_title = "A" * 101
    response = client.post("/events/", json={
        "title": long_title,
        "description": "Event with too long title",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_event_with_too_long_description():
    long_description = "A" * 501
    response = client.post("/events/", json={
        "title": "Event with too long description",
        "description": long_description,
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_event_with_too_long_location():
    long_location = "A" * 201
    response = client.post("/events/", json={
        "title": "Event with too long location",
        "description": "This event has a location that is too long.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": long_location,
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_event_with_invalid_participant():
    response = client.post("/events/", json={
        "title": "Event with invalid participant",
        "description": "This event has a participant with an empty string.",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_event_with_no_participants():
    response = client.post("/events/", json={
        "title": "No Participants Event",
        "description": "Event with no participants",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": []
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["participants"] == []

def test_create_event_with_null_participants():
    response = client.post("/events/", json={
        "title": "Null Participants Event",
        "description": "Event with null participants",
        "start_time": "2024-08-20T10:00:00",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": None 
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["participants"] is None

def test_create_event_with_invalid_datetime_format():
    response = client.post("/events/", json={
        "title": "Invalid Date Format Event",
        "description": "This event has an invalid datetime format.",
        "start_time": "20-08-2024 10:00",
        "end_time": "20-08-2024 12:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

"""def test_create_event_with_missing_start_time():
    response = client.post("/events/", json={
        "title": "Missing Start Time Event",
        "description": "This event has a missing start time.",
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["start_time"] is not None"""

def test_create_event_with_start_time_in_past():
    past_time = "2023-08-20T10:00:00"
    response = client.post("/events/", json={
        "title": "Past Start Time Event",
        "description": "This event has a start time in the past.",
        "start_time": past_time,
        "end_time": "2024-08-20T12:00:00",
        "location": "Test Location",
        "participants": ["Alice", "Bob"]
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["start_time"] == past_time
