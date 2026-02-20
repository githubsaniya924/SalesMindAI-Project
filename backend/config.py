import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # --- Core ---
    SECRET_KEY = os.getenv("SECRET_KEY", "salesmindAI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # --- JWT (Corrected for Cookies & No-CSRF) ---
    # Now it looks for JWT_SECRET_KEY, and if missing, uses the SECRET_KEY
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY) 
    JWT_TOKEN_LOCATION = ["headers", "cookies"] # Allow both    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_SECURE = False  # Set to True in production (HTTPS)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_CSRF_PROTECT = False  # Critical to avoid 422 errors
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # --- Email Configuration (Missing in your previous version) ---
    # Use these names to match your email_utils.py logic
    EMAIL_USER = os.getenv("EMAIL_USER") 
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # If you are using Flask-Mail as well, keep these:
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # --- Celery ---
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # --- Stripe & APIs ---
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    PDL_API_KEY = os.getenv("PDL_API_KEY")


    