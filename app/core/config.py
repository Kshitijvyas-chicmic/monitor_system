import os
from dotenv import load_dotenv

load_dotenv()  

APP_NAME = os.getenv("APP_NAME", "Internal Task Tracker")
APP_ENV = os.getenv("APP_ENV", "development")
APP_PORT = int(os.getenv("APP_PORT", 8000))
DATABASE_URL=os.getenv("DATABASE_URL")
JWT_SECRET_KEY=os.getenv("JWT_SECTRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GITHUB_CLIENT_ID= os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET=os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI= os.getenv("GITHUB_REDIRECT_URI")
