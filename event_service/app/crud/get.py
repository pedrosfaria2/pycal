import logging
from sqlalchemy.orm import Session
from app.models import Event
from sqlalchemy import func

logger = logging.getLogger(__name__)


def get_event(db: Session, event_id: int):
    try:
        logger.debug(f"Fetching event with ID: {event_id}")
        event = db.query(Event).filter(Event.id == event_id).first()
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
        events = db.query(Event).offset(skip).limit(limit).all()
        logger.info(f"Fetched {len(events)} events")
        return events
    except Exception as e:
        logger.error(f"Error fetching events: {e}", exc_info=True)
        raise


def get_events_by_title(db: Session, title: str, exact: bool = False):
    try:
        logger.debug(f"Fetching events with title: {title} (exact match: {exact})")

        if exact:
            events = db.query(Event).filter(func.lower(Event.title) == title.lower()).all()
        else:
            events = db.query(Event).filter(func.lower(Event.title).contains(title.lower())).all()

        logger.info(f"Fetched {len(events)} events with title matching: {title}")
        return events
    except Exception as e:
        logger.error(f"Error fetching events by title '{title}': {e}", exc_info=True)
        raise


def get_events_by_participant(db: Session, participant: str, exact: bool = False):
    try:
        logger.debug(f"Fetching events with participant: {participant} (exact match: {exact})")

        if exact:
            events = db.query(Event).filter(
                func.json_contains(Event.participants, f'["{participant}"]')
            ).all()
        else:
            events = db.query(Event).filter(
                func.lower(func.json_unquote(func.json_extract(Event.participants, '$[*]'))).contains(
                    participant.lower())
            ).all()

        logger.info(f"Fetched {len(events)} events with participant matching: {participant}")
        return events
    except Exception as e:
        logger.error(f"Error fetching events by participant '{participant}': {e}", exc_info=True)
        raise


def get_events_by_description(db: Session, description: str, exact: bool = False):
    try:
        logger.debug(f"Fetching events with description: '{description}' (exact match: {exact})")

        if exact:
            events = db.query(Event).filter(func.lower(Event.description) == description.lower()).all()
        else:
            events = db.query(Event).filter(func.lower(Event.description).contains(description.lower())).all()

        logger.info(f"Fetched {len(events)} events with description matching: '{description}'")

        return events
    except Exception as e:
        logger.error(f"Error fetching events by description '{description}': {e}", exc_info=True)
        raise


def get_events_by_location(db: Session, location: str, exact: bool = False):
    try:
        logger.debug(f"Fetching events with location: {location} (exact match: {exact})")

        if exact:
            events = db.query(Event).filter(func.lower(Event.location) == location.lower()).all()
        else:
            events = db.query(Event).filter(func.lower(Event.location).contains(location.lower())).all()

        logger.info(f"Fetched {len(events)} events with location matching: {location}")
        return events
    except Exception as e:
        logger.error(f"Error fetching events by location '{location}': {e}", exc_info=True)
        raise
