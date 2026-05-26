import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


logger = logging.getLogger("volleyops.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            logger.exception(
                "request_failed",
                extra={
                    "extra_fields": {
                        "event": "request_failed",
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": 500,
                        "duration_ms": duration_ms,
                    }
                },
            )

            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "request_completed",
            extra={
                "extra_fields": {
                    "event": "request_completed",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            },
        )

        response.headers["X-Request-ID"] = request_id

        return response