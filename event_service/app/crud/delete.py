import logging
from sqlalchemy.orm import Session
from .get import get_event

logger = logging.getLogger(__name__)


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
        logger.error(f"Error deleting event with ID {event_id}: {e}", exc_info=True)
        raise
