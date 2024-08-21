import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import create, get, update, delete
from app.database import get_db
from typing import List
from app.schemas import EventCreate, Event

router = APIRouter(
    prefix="/events",
    tags=["Events"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"}

    }
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
    description="Creates a new event with the specified details.",
    response_description="The details of the created event."
)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event with the specified details.

    This endpoint allows you to create a new event. It checks for scheduling conflicts
    with existing events based on the event's time, location, and participants.

    - **title**: Title of the event.
    - **description**: Description of the event (optional).
    - **start_time**: Starting time of the event.
    - **end_time**: Ending time of the event.
    - **location**: Location of the event.
    - **participants**: List of participants in the event.
    """
    try:
        new_event = create.create_event(db=db, event=event)
        logger.info(f"Event created with ID: {new_event.id}")
        return new_event
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="Error creating event")


@router.get(
    "/",
    response_model=List[Event],
    summary="List all events",
    description="Retrieves a list of all events. You can use query parameters to limit and skip results.",
    response_description="A list of events."
)
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of events.

    - **skip**: Number of events to skip (useful for pagination).
    - **limit**: Maximum number of events to return.
    """
    try:
        events = get.get_events(db, skip=skip, limit=limit)
        return events
    except Exception as e:
        logger.error(f"Error fetching events: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching events")


@router.get(
    "/{event_id}",
    response_model=Event,
    summary="Get an event by ID",
    description="Retrieve details of an event by its ID.",
    response_description="The details of the event."
)
def read_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get the details of an event by its ID.

    - **event_id**: The ID of the event to retrieve.
    """
    try:
        db_event = get.get_event(db, event_id=event_id)
        if db_event is None:
            logger.warning(f"Event with ID {event_id} not found")
            raise HTTPException(status_code=404, detail="Event not found")
        return db_event
    except HTTPException as e:
        logger.warning(f"Event not found: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error fetching event with ID {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching event")


@router.put(
    "/{event_id}",
    response_model=Event,
    summary="Update an event",
    description="Update the details of an event by its ID.",
    response_description="The updated event details."
)
def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    """
    Update an existing event.

    - **event_id**: The ID of the event to update.
    - **event**: The updated event data.
    """
    try:
        db_event = update.update_event(db, event_id=event_id, event_data=event)
        if db_event is None:
            logger.warning(f"Event with ID {event_id} not found for update")
            raise HTTPException(status_code=404, detail="Event not found")
        logger.info(f"Event updated with ID: {event_id}")
        return db_event
    except HTTPException as e:
        logger.warning(f"Error updating event: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error updating event with ID {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating event")


@router.delete(
    "/{event_id}",
    response_model=Event,
    summary="Delete an event",
    description="Delete an event by its ID.",
    response_description="The details of the deleted event."
)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Delete an event by its ID.

    - **event_id**: The ID of the event to delete.
    """
    try:
        db_event = delete.delete_event(db, event_id=event_id)
        if db_event is None:
            logger.warning(f"Event with ID {event_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Event not found")
        logger.info(f"Event deleted with ID: {event_id}")
        return db_event
    except HTTPException as e:
        logger.warning(f"Error deleting event: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error deleting event with ID {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error deleting event")
