import logging
from sqlalchemy.orm import Session
from .. import models

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
        logger.error(f"Error fetching event with ID {event_id}: {e}", exc_info=True)
        raise


def get_events(db: Session, skip: int = 0, limit: int = 10):
    try:
        logger.debug(f"Fetching events with skip: {skip}, limit: {limit}")
        events = db.query(models.Event).offset(skip).limit(limit).all()
        logger.info(f"Fetched {len(events)} events")
        return events
    except Exception as e:
        logger.error(f"Error fetching events: {e}", exc_info=True)
        raise
