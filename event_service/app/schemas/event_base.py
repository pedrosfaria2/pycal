from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import List, Optional


class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100,
                       description="The title of the event. Must be between 3 and 100 characters.")
    description: Optional[str] = Field("Sample Event Description", max_length=500,
                                       description="A detailed description of the event, with a maximum length of 500 "
                                                   "characters.")
    start_time: datetime = Field(...,
                                 description="The starting time of the event. Must be in the format "
                                             "'YYYY-MM-DDTHH:MM:SS'.")
    end_time: datetime = Field(...,
                               description="The ending time of the event. Must be after the start time and in the "
                                           "format 'YYYY-MM-DDTHH:MM:SS'.")
    location: Optional[str] = Field("Sample Location", max_length=200,
                                    description="The location where the event will be held, with a maximum length of "
                                                "200 characters.")
    participants: Optional[List[str]] = Field(default=["Participant1", "Participant2"],
                                              description="A list of participants for the event. Each participant "
                                                          "must be a non-empty string.")

    model_config = ConfigDict(from_attributes=True)

    @field_validator('end_time')
    def check_end_time(cls, end_time, info):
        start_time = info.data.get('start_time')
        if start_time and end_time and end_time < start_time:
            raise ValueError('End time must be after the start time.')
        return end_time

    @field_validator('participants')
    def validate_participants(cls, participants):
        if participants:
            for participant in participants:
                if not participant.strip():
                    raise ValueError("Each participant's name must be a non-empty string.")
        return participants
