# =============================================
# config.py - Application Settings
# =============================================
# This file loads all settings from the .env file.
# We use pydantic-settings so that if any required
# setting is missing, the app will crash immediately
# with a clear error (instead of breaking randomly later).
# =============================================

from pydantic_settings import BaseSettings  # Helps load .env file automatically


class Settings(BaseSettings):
    """
    All the configuration/settings our app needs.
    These values come from the .env file in the backend folder.
    """

    # Secret key used to create JWT tokens (like a password for your tokens)
    SECRET_KEY: str = "enter-hiring-system-secret-key-2024"

    # How long a login token stays valid (in minutes)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database connection string
    # "sqlite:///./hiring.db" means: use SQLite and store data in a file called hiring.db
    DATABASE_URL: str = "sqlite:///./hiring.db"

    # Default admin account credentials (used when seeding the database)
    ADMIN_EMAIL: str = "admin@enter.in"
    ADMIN_PASSWORD: str = "admin123"

    # Algorithm used for JWT token encoding
    ALGORITHM: str = "HS256"

    # Folder where uploaded resumes will be saved
    UPLOAD_DIR: str = "app/uploads"

    class Config:
        # Tell pydantic-settings to read from .env file
        env_file = ".env"


# Create a single instance of Settings that the entire app will use
# This is called a "singleton pattern" - only one settings object exists
settings = Settings()
