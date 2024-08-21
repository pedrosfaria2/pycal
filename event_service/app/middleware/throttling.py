import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler

MAX_REQUESTS = 150

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{MAX_REQUESTS}/minute"]
)


def apply_throttling(app: FastAPI):
    if os.getenv("DISABLE_THROTTLE", "false").lower() == "true":
        return

    app.state.limiter = limiter
    app.state.max_requests = MAX_REQUESTS
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
