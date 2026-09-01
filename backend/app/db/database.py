# =============================================
# database.py - Database Connection Setup
# =============================================
# This file sets up our connection to the SQLite database.
#
# WHAT IS SQLAlchemy?
#   SQLAlchemy is an ORM (Object Relational Mapper).
#   Instead of writing raw SQL like "SELECT * FROM jobs",
#   we can write Python code like "db.query(Job).all()"
#   It converts our Python code into SQL behind the scenes.
#
# WHAT IS SQLite?
#   SQLite is a lightweight database that stores ALL data
#   in a single file (hiring.db). No setup needed!
#   Perfect for development and small projects.
# =============================================

from sqlalchemy import create_engine  # Creates the database connection
from sqlalchemy.orm import sessionmaker, declarative_base  # Tools for sessions and models

from app.config import settings  # Import our app settings

# ---- Step 1: Create the Database Engine ----
# The engine is like a "connection pool" to our database.
# connect_args={"check_same_thread": False} is needed ONLY for SQLite
# because SQLite by default only allows one thread to use it.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite only
)

# ---- Step 2: Create a Session Factory ----
# A "session" is like a conversation with the database.
# You open a session, do your queries, then close it.
# SessionLocal is a factory that creates new sessions when needed.
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-save changes (we want to control when to save)
    autoflush=False,   # Don't auto-send changes to DB (we flush manually)
    bind=engine        # Connect this session factory to our database engine
)

# ---- Step 3: Create a Base Class for Models ----
# All our database table classes (User, Job, Application)
# will inherit from this Base class.
# This tells SQLAlchemy "hey, this Python class is a database table!"
Base = declarative_base()


# ---- Step 4: Dependency Function for FastAPI ----
# FastAPI uses "dependencies" to inject things into route functions.
# This function:
#   1. Opens a new database session
#   2. Gives it to the route function to use
#   3. Automatically closes the session when the route is done
#
# We use "yield" (not "return") because we need to clean up
# (close the session) AFTER the route function finishes.
def get_db():
    """
    Creates a database session for each API request.
    
    Usage in routes:
        @router.get("/jobs")
        def get_jobs(db: Session = Depends(get_db)):
            # 'db' is now a live database session you can query with
            return db.query(Job).all()
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Give the session to the route function
    finally:
        db.close()  # Always close the session when done (even if there's an error)
