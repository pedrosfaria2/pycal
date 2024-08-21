from fastapi import FastAPI, HTTPException
from app.logging_config import setup_logging
from app.middleware.log_exceptions import log_exceptions
from app.routers import events
from app.exceptions.handlers import http_exception_handler, general_exception_handler
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
)

setup_logging()

app.include_router(events.router)

app.middleware("http")(log_exceptions)

app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(Exception)(general_exception_handler)
