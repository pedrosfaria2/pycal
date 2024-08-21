import pytest
from sqlalchemy.orm import Session
from app.crud import create, get, update, delete
from app.schemas import EventCreate


@pytest.fixture
def sample_event():
    return EventCreate(
        title="Sample Event",
        description="This is a sample event",
        start_time="2024-08-20T10:00:00",
        end_time="2024-08-20T12:00:00",
        location="Sample Location",
        participants=["Alice", "Bob"]
    )


def test_create_event(db_session: Session, sample_event: EventCreate):
    created_event = create.create_event(db_session, sample_event)
    assert created_event.title == sample_event.title
    assert created_event.description == sample_event.description


def test_get_events(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events(db_session)
    assert len(events) > 0
    assert events[0].title == sample_event.title


def test_get_event(db_session: Session, sample_event: EventCreate):
    created_event = create.create_event(db_session, sample_event)
    event_id = created_event.id
    event = get.get_event(db_session, event_id)
    assert event is not None
    assert event.title == sample_event.title


def test_update_event(db_session: Session, sample_event: EventCreate):
    created_event = create.create_event(db_session, sample_event)
    event_id = created_event.id

    updated_data = EventCreate(
        title="Updated Event",
        description="This is an updated event.",
        start_time="2024-08-20T11:00:00",
        end_time="2024-08-20T13:00:00",
        location="Updated Location",
        participants=["Charlie", "Dave"]
    )

    updated_event = update.update_event(db_session, event_id, updated_data)
    assert updated_event.title == updated_data.title
    assert updated_event.description == updated_data.description


def test_delete_event(db_session: Session, sample_event: EventCreate):
    created_event = create.create_event(db_session, sample_event)
    event_id = created_event.id

    deleted_event = delete.delete_event(db_session, event_id)
    assert deleted_event is not None
    assert get.get_event(db_session, event_id) is None


def test_get_events_by_title(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_title(db_session, title="Sample Event")
    assert len(events) > 0
    assert events[0].title == "Sample Event"


def test_get_events_by_title_exact(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_title(db_session, title="Sample Event", exact=True)
    assert len(events) > 0
    assert events[0].title == "Sample Event"


def test_get_events_by_participant(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_participant(db_session, participant="Alice")
    assert len(events) > 0
    assert "Alice" in events[0].participants


def test_get_events_by_participant_exact(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_participant(db_session, participant="Alice", exact=True)
    assert len(events) > 0
    assert "Alice" in events[0].participants


def test_get_events_by_description(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_description(db_session, description="sample event")
    assert len(events) > 0
    assert events[0].description == "This is a sample event"


def test_get_events_by_description_exact(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_description(db_session, description="This is a sample event", exact=True)
    assert len(events) > 0
    assert events[0].description == "This is a sample event"


def test_get_events_by_location(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_location(db_session, location="Sample Location")
    assert len(events) > 0
    assert events[0].location == "Sample Location"


def test_get_events_by_location_exact(db_session: Session, sample_event: EventCreate):
    create.create_event(db_session, sample_event)
    events = get.get_events_by_location(db_session, location="Sample Location", exact=True)
    assert len(events) > 0
    assert events[0].location == "Sample Location"
