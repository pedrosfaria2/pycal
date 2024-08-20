import logging
from sqlalchemy.orm import Session
from . import models, schemas

logger = logging.getLogger(__name__)

def get_event(db: Session, event_id: int):
    try:
        logger.debug(f"Fetching event with ID: {event_id}")
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if event:
            logger.info(f"Event found: {event.title}")
        else:
            logger.warning(f"No event found with ID: {event_id}")
        return event
    except Exception as e:
        logger.error(f"Error fetching event with ID {event_id}: {e}")
        raise

def get_events(db: Session, skip: int = 0, limit: int = 10):
    try:
        logger.debug(f"Fetching events with skip: {skip}, limit: {limit}")
        events = db.query(models.Event).offset(skip).limit(limit).all()
        logger.info(f"Fetched {len(events)} events")
        return events
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise

def create_event(db: Session, event: schemas.EventCreate):
    try:
        logger.debug(f"Creating event: {event.title}")
        db_event = models.Event(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        logger.info(f"Event created with ID: {db_event.id}")
        return db_event
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise

def delete_event(db: Session, event_id: int):
    try:
        logger.debug(f"Deleting event with ID: {event_id}")
        db_event = get_event(db, event_id)
        if db_event:
            db.delete(db_event)
            db.commit()
            logger.info(f"Event deleted with ID: {event_id}")
        else:
            logger.warning(f"No event found to delete with ID: {event_id}")
        return db_event
    except Exception as e:
        logger.error(f"Error deleting event with ID {event_id}: {e}")
        raise

def update_event(db: Session, event_id: int, event_data: schemas.EventCreate):
    try:
        logger.debug(f"Updating event with ID: {event_id}")
        db_event = get_event(db, event_id)
        if db_event:
            for key, value in event_data.model_dump().items():
                setattr(db_event, key, value)
            db.commit()
            db.refresh(db_event)
            logger.info(f"Event updated with ID: {event_id}")
        else:
            logger.warning(f"No event found to update with ID: {event_id}")
        return db_event
    except Exception as e:
        logger.error(f"Error updating event with ID {event_id}: {e}")
        raise
