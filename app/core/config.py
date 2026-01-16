import os
from dotenv import load_dotenv

load_dotenv()  

APP_NAME = os.getenv("APP_NAME", "Internal Task Tracker")
APP_ENV = os.getenv("APP_ENV", "development")
APP_PORT = int(os.getenv("APP_PORT", 8000))
DATABASE_URL=os.getenv("DATABASE_URL")


