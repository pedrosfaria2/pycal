from pydantic import Field
from .event_base import EventBase
from pydantic import ConfigDict

class Event(EventBase):
    id: int = Field(..., description="The unique identifier of the event.")

    model_config = ConfigDict(from_attributes=True)
