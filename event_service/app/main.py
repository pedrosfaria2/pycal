from fastapi import FastAPI
from app.routers import events

app = FastAPI(
    title="Event Manager",
    description="API for managing calendar events",
    version="1.0.0"
)

app.include_router(events.router)
