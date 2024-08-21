import os
from app.middleware.throttling import MAX_REQUESTS


class Settings:
    APP_NAME: str = "Event Manager"
    APP_VERSION: str = "1.0.0"
    DESCRIPTION: str = f"API for managing calendar events. Note: All endpoints have throttling applied of {MAX_REQUESTS}/minute."
    DEBUG: bool = os.getenv("DEBUG", False)


settings = Settings()
