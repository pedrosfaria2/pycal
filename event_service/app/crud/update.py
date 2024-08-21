import logging
from sqlalchemy.orm import Session
from .. import schemas
from .get import get_event

logger = logging.getLogger(__name__)


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
        logger.error(f"Error updating event with ID {event_id}: {e}", exc_info=True)
        raise
