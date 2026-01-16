from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.config_logging import logger

async def global_exception_handler(request:Request, exc:Exception):
    logger.error(f"unhandled error: {exc} | path: {request.url}")
    return JSONResponse(
        status_code = 500,
        content ={"detail":"internal server Error"}
    )