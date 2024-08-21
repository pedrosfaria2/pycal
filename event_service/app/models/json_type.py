from sqlalchemy.types import TypeDecorator, Text
import json

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
