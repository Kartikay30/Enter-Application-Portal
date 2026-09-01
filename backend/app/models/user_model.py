# =============================================
# user_model.py - Admin User Database Table
# =============================================
# This file defines the "users" table in our database.
# Right now, we only have ONE admin user (admin@enter.in),
# but the table structure supports multiple users if needed.
#
# WHAT IS A MODEL?
#   A model is a Python class that represents a database table.
#   Each attribute of the class = a column in the table.
#   Each instance of the class = a row in the table.
# =============================================

from sqlalchemy import Column, Integer, String, DateTime  # Column types
from datetime import datetime, timezone  # For timestamps

from app.db.database import Base  # Our base class (all models inherit from this)


class UserModel(Base):
    """
    Represents the 'users' table in the database.
    
    Columns:
        id            -> Unique number for each user (auto-generated)
        email         -> User's email address (must be unique)
        hashed_password -> The password stored in encrypted form (NEVER plain text!)
        role          -> What type of user ("admin" for now)
        created_at    -> When this user was created
    """

    # Name of the actual table in the database
    __tablename__ = "users"

    # ---- Columns ----

    # Primary Key = unique identifier for each row
    # autoincrement=True means the database auto-assigns 1, 2, 3, etc.
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Email must be unique (no two users can have the same email)
    # index=True makes searching by email faster
    email = Column(String(255), unique=True, index=True, nullable=False)

    # We NEVER store plain passwords! Always store the hashed version.
    # Example: "admin123" becomes "$2b$12$LJ3m5..." (unreadable gibberish)
    hashed_password = Column(String(255), nullable=False)

    # Role of the user (for now, always "admin")
    role = Column(String(50), default="admin")

    # Automatically records when this user was created
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
