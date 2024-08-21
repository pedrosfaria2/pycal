from fastapi import status
from fastapi.testclient import TestClient


def create_event(client: TestClient, title: str, description: str, start_time: str, end_time: str, location: str,
                 participants: list):
    response = client.post("/events/", json={
        "title": title,
        "description": description,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "participants": participants
    })
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def test_create_event(client: TestClient):
    event_data = create_event(client, "Test Event", "This is a test event.", "2024-08-20T10:00:00",
                              "2024-08-20T12:00:00", "Test Location", ["Alice", "Bob"])
    assert event_data["title"] == "Test Event"
    assert event_data["description"] == "This is a test event."


def test_read_events(client: TestClient):
    create_event(client, "Test Event", "This is a test event.", "2024-08-20T10:00:00", "2024-08-20T12:00:00",
                 "Test Location", ["Alice", "Bob"])

    response = client.get("/events/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0


def test_read_event(client: TestClient):
    event_data = create_event(client, "Test Event", "This is a test event.", "2024-08-20T10:00:00",
                              "2024-08-20T12:00:00", "Test Location", ["Alice", "Bob"])
    event_id = event_data["id"]

    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event_id
    assert data["title"] == "Test Event"


def test_update_event(client: TestClient):
    event_data = create_event(client, "Test Event", "This is a test event.", "2024-08-20T10:00:00",
                              "2024-08-20T12:00:00", "Test Location", ["Alice", "Bob"])
    event_id = event_data["id"]

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
    event_data = create_event(client, "Test Event", "This is a test event.", "2024-08-20T10:00:00",
                              "2024-08-20T12:00:00", "Test Location", ["Alice", "Bob"])
    event_id = event_data["id"]

    response = client.delete(f"/events/{event_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event_id

    response = client.get(f"/events/{event_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_events_by_title(client: TestClient):
    create_event(client, "Unique Title", "Description for unique title.", "2024-08-20T10:00:00", "2024-08-20T12:00:00",
                 "Test Location", ["Alice", "Bob"])

    response = client.get("/events/search/", params={"title": "Unique Title", "exact": "true"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Unique Title"

    response = client.get("/events/search/", params={"title": "Unique", "exact": "false"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert "Unique" in data[0]["title"]


def test_search_events_by_participant(client: TestClient):
    create_event(client, "Event with Alice", "Description for event with Alice.", "2024-08-20T10:00:00",
                 "2024-08-20T12:00:00", "Test Location", ["Alice", "Bob"])

    response = client.get("/events/search/participant/", params={"participant": "Alice", "exact": "true"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert "Alice" in data[0]["participants"]

    response = client.get("/events/search/participant/", params={"participant": "Ali", "exact": "false"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert any("Ali" in participant for participant in data[0]["participants"])


def test_search_events_by_description(client: TestClient):
    create_event(client, "Event with specific description", "A very specific description for this event.",
                 "2024-08-20T10:00:00", "2024-08-20T12:00:00", "Test Location", ["Alice", "Bob"])

    response = client.get("/events/search/description/",
                          params={"description": "A very specific description for this event.", "exact": "true"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["description"] == "A very specific description for this event."

    response = client.get("/events/search/description/",
                          params={"description": "specific description", "exact": "false"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert "specific description" in data[0]["description"]


def test_search_events_by_location(client: TestClient):
    create_event(client, "Event with specific location", "Description for event with specific location.",
                 "2024-08-20T10:00:00", "2024-08-20T12:00:00", "Unique Location", ["Alice", "Bob"])

    response = client.get("/events/search/location/", params={"location": "Unique Location", "exact": "true"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["location"] == "Unique Location"

    response = client.get("/events/search/location/", params={"location": "Unique", "exact": "false"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert "Unique" in data[0]["location"]
