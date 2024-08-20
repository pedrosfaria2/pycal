from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import List, Optional

class EventBase(BaseModel):
    title: str = Field("Sample Event Title", min_length=3, max_length=100, description="The title of the event.")
    description: Optional[str] = Field("Sample Event Description", max_length=500, description="A detailed description of the event.")
    start_time: datetime = Field(default_factory=datetime.now, description="The starting time of the event.")
    end_time: datetime = Field(default_factory=datetime.now, description="The ending time of the event.")
    location: Optional[str] = Field("Sample Location", max_length=200, description="The location where the event will be held.")
    participants: Optional[List[str]] = Field(default=["Participant1", "Participant2"], description="A list of participants for the event.")

    model_config = ConfigDict(from_attributes=True)

    @field_validator('end_time')
    def check_end_time(cls, end_time, info):
        start_time = info.data['start_time']
        if start_time and end_time < start_time:
            raise ValueError('end_time must be after start_time')
        return end_time

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int = Field(default=1, description="The unique identifier of the event.")

    model_config = ConfigDict(from_attributes=True)
