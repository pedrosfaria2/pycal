import pytest
from sqlalchemy.orm import Session
from app import crud, schemas

@pytest.fixture
def sample_event():
    return schemas.EventCreate(
        title="Sample Event",
        description="This is a sample event.",
        start_time="2024-08-20T10:00:00",
        end_time="2024-08-20T12:00:00",
        location="Sample Location",
        participants=["Alice", "Bob"]
    )

def test_create_event(db_session: Session, sample_event: schemas.EventCreate):
    created_event = crud.create_event(db_session, sample_event)
    assert created_event.title == sample_event.title
    assert created_event.description == sample_event.description

def test_get_events(db_session: Session, sample_event: schemas.EventCreate):
    crud.create_event(db_session, sample_event)
    events = crud.get_events(db_session)
    assert len(events) > 0
    
    #for event in events:
        #print(f"Event Title in DB: {event.title}")

    assert events[0].title == sample_event.title

def test_get_event(db_session: Session, sample_event: schemas.EventCreate):
    created_event = crud.create_event(db_session, sample_event)
    event_id = created_event.id
    event = crud.get_event(db_session, event_id)
    assert event is not None
    assert event.title == sample_event.title

def test_update_event(db_session: Session, sample_event: schemas.EventCreate):
    created_event = crud.create_event(db_session, sample_event)
    event_id = created_event.id

    updated_data = schemas.EventCreate(
        title="Updated Event",
        description="This is an updated event.",
        start_time="2024-08-20T11:00:00",
        end_time="2024-08-20T13:00:00",
        location="Updated Location",
        participants=["Charlie", "Dave"]
    )

    updated_event = crud.update_event(db_session, event_id, updated_data)
    assert updated_event.title == updated_data.title
    assert updated_event.description == updated_data.description

def test_delete_event(db_session: Session, sample_event: schemas.EventCreate):
    created_event = crud.create_event(db_session, sample_event)
    event_id = created_event.id

    deleted_event = crud.delete_event(db_session, event_id)
    assert deleted_event is not None
    assert crud.get_event(db_session, event_id) is None
