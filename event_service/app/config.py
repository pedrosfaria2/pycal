import os

class Settings:
    APP_NAME: str = "Event Manager"
    APP_VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for managing calendar events"
    DEBUG: bool = os.getenv("DEBUG", False)

settings = Settings()
