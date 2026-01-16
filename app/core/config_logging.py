import logging
import sys
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger



console_handler = logging.StreamHandler(sys.stdout)
console_formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(message)s'
)

console_handler.setFormatter(console_formatter)

file_handler = RotatingFileHandler(
    'logs/app.log', maxBytes = 5*1024*1024
,backupCount = 3)
file_handler.setFormatter(console_formatter)

logger = logging.getLogger("task-tracker")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("logger initialized")
