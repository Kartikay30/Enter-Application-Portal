# =============================================
# job_model.py - Job Opening Database Table
# =============================================
# This file defines the "jobs" table in our database.
# Each row represents one job opening (e.g., "AI Engineer", "Frontend Developer").
# The admin can Create, Read, Update, and Delete (CRUD) these jobs.
# Candidates see only "Active" jobs in their application dropdown.
# =============================================

from sqlalchemy import Column, Integer, String, Text, DateTime  # Column types
from datetime import datetime, timezone  # For timestamps

from app.db.database import Base  # Our base class


class JobModel(Base):
    """
    Represents the 'jobs' table in the database.
    
    Columns:
        id           -> Unique job ID (auto-generated)
        title        -> Job title (e.g., "Full Stack Developer")
        department   -> Which team (e.g., "Engineering", "Design")
        location     -> Where the job is (e.g., "Remote", "Bangalore")
        job_type     -> Employment type (e.g., "Full-time", "Internship")
        description  -> Detailed job description
        requirements -> What skills/qualifications are needed
        status       -> "Active" (accepting applications) or "Closed" (no longer accepting)
        created_at   -> When this job was posted
        updated_at   -> When this job was last edited
    """

    # Name of the actual table in the database
    __tablename__ = "jobs"

    # ---- Columns ----

    # Unique job ID (auto-generated: 1, 2, 3, ...)
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Job title - what the position is called
    title = Column(String(255), nullable=False)

    # Department - which team this job belongs to
    department = Column(String(100), nullable=False)

    # Location - where the employee will work
    location = Column(String(200), nullable=False)

    # Job type - full-time, part-time, internship, contract
    job_type = Column(String(50), nullable=False, default="Full-time")

    # Description - detailed info about the role (can be long, so we use Text)
    description = Column(Text, nullable=False)

    # Requirements - skills and qualifications needed (also long text)
    requirements = Column(Text, nullable=True)

    # Status - is this job still accepting applications?
    # "Active" = visible to candidates, "Closed" = hidden
    status = Column(String(20), default="Active")

    # When this job was first created
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # When this job was last updated (auto-updates on every edit)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
