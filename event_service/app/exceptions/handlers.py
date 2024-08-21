from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP Exception: {exc.detail}, Status Code: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
