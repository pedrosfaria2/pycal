from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
from .json_type import JsonType


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    participants = Column(JsonType)
