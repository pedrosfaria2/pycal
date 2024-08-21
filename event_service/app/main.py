from fastapi import FastAPI, HTTPException
from app.logging_config import setup_logging
from app.middleware.log_exceptions import log_exceptions
from app.routers import events, health_check
from app.exceptions.handlers import http_exception_handler, general_exception_handler
from app.config import settings
from app.middleware.throttling import apply_throttling

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
)

setup_logging()

apply_throttling(app)

app.include_router(events.router)
app.include_router(health_check.router)

app.middleware("http")(log_exceptions)

app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(Exception)(general_exception_handler)


@app.get("/", summary="Root Endpoint", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Event Management API!",
        "docs_url": "Go to /docs for the Swagger documentation.",
        "redoc_url": "Go to /redoc for the ReDoc documentation."
    }
