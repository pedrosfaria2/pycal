import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"}
    }
)

logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        new_event = crud.create_event(db=db, event=event)
        logger.info(f"Event created with ID: {new_event.id}")
        return new_event
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="Error creating event")

@router.get("/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        events = crud.get_events(db, skip=skip, limit=limit)
        return events
    except Exception as e:
        logger.error(f"Error fetching events: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching events")

@router.get("/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    try:
        db_event = crud.get_event(db, event_id=event_id)
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

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        db_event = crud.update_event(db, event_id=event_id, event_data=event)
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

@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    try:
        db_event = crud.delete_event(db, event_id=event_id)
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
