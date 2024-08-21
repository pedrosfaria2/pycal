import logging
from sqlalchemy.orm import Session
from app.schemas import EventCreate
from app.models import Event

logger = logging.getLogger(__name__)


def create_event(db: Session, event: EventCreate):
    try:
        logger.debug(f"Creating event: {event.title}")
        db_event = Event(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        logger.info(f"Event created with ID: {db_event.id}")
        return db_event
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        raise
