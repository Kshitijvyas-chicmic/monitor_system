from fastapi import FastAPI
from app.core.config import APP_NAME
from app.core.config_logging import logger
from app.core.exceptions import global_exception_handler
from app.routes import userroutes  # import auth routes




app = FastAPI(title = APP_NAME)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(userroutes.router)
@app.on_event("startup")
def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("application shutting down")

@app.get("/health")
def health_check():
    logger.info("Health endpoint called")
    return {"status":"ok"}

@app.get("/wealt")
def wealth_check():
    logger.info("Health endpoint called")
    return {"status":"ok"}