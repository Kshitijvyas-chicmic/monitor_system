# app/core/exceptions.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.config_logging import logger

# Catch all HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("HTTP error", extra={"path": str(request.url), "status_code": exc.status_code, "detail": exc.detail})
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail},
    )

# Catch all uncaught exceptions
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", extra={"path": str(request.url), "error": str(exc)})
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal server error"},
    )
