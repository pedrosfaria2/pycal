from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    participants: Optional[List[str]] = []

    model_config = ConfigDict(from_attributes=True)

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
