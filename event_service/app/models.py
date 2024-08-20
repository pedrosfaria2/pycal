from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TypeDecorator, Text
import json

Base = declarative_base()


class JsonType(TypeDecorator):
    impl = Text

    @staticmethod
    def process_bind_param(value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    @staticmethod
    def process_result_value(value, dialect):
        if value is not None:
            return json.loads(value)
        return None


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    participants = Column(JsonType)
