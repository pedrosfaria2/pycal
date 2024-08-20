from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.logging_config import setup_logging
from app.routers import events

app = FastAPI(
    title="Event Manager",
    description="API for managing calendar events",
    version="1.0.0"
)

setup_logging()

app.include_router(events.router)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            logging.error(f"HTTP Error {response.status_code} for request {request.method} {request.url}")
        return response
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP Exception: {exc.detail}, Status Code: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
