from fastapi import Request
from fastapi.responses import JSONResponse
import logging

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
