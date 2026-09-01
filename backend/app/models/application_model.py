# =============================================
# application_model.py - Candidate Application Database Table
# =============================================
# This file defines the "applications" table in our database.
# Each row represents one candidate's job application.
#
# A candidate fills out the public form with:
#   - Their name, email, phone
#   - Which job they're applying for
#   - A brief note (cover letter / intro)
#   - Their resume file (PDF/DOCX)
#
# The admin then moves each candidate through the hiring pipeline:
#   Applied -> R1 -> R2 -> R3 -> Approved (or Reject at any stage)
# =============================================

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey  # Column types
from sqlalchemy.orm import relationship  # For linking tables together
from datetime import datetime, timezone  # For timestamps

from app.db.database import Base  # Our base class


class ApplicationModel(Base):
    """
    Represents the 'applications' table in the database.
    
    Columns:
        id              -> Unique application ID
        job_id          -> Which job this application is for (links to jobs table)
        full_name       -> Candidate's full name
        email           -> Candidate's email address
        phone           -> Candidate's phone number
        brief_note      -> Short message from the candidate
        resume_filename -> Original name of the uploaded file (e.g., "john_resume.pdf")
        resume_path     -> Where the file is saved on the server (e.g., "app/uploads/abc123.pdf")
        stage           -> Current position in the hiring pipeline
        created_at      -> When the application was submitted
        updated_at      -> When the stage was last changed
    
    Relationship:
        job -> Links to the JobModel to get job details (title, department, etc.)
    """

    # Name of the actual table in the database
    __tablename__ = "applications"

    # ---- Columns ----

    # Unique application ID
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Key = a link to another table
    # This connects each application to a specific job
    # If the job is deleted, we set this to NULL (SET NULL) instead of deleting the application
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)

    # Candidate's personal information
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)

    # A short message / cover note from the candidate
    brief_note = Column(Text, nullable=True)

    # Resume file details
    resume_filename = Column(String(255), nullable=True)  # Original filename
    resume_path = Column(String(500), nullable=True)       # Path where file is stored

    # ---- Hiring Pipeline Stage ----
    # This tracks where the candidate is in the hiring process.
    # Possible values:
    #   "Applied"    -> Just submitted (default/initial stage)
    #   "R1"         -> Passed to Round 1 interview
    #   "R1 Reject"  -> Rejected after Round 1
    #   "R2"         -> Passed to Round 2 interview
    #   "R2 Reject"  -> Rejected after Round 2
    #   "R3"         -> Passed to Round 3 interview
    #   "R3 Reject"  -> Rejected after Round 3
    #   "Reject"     -> General rejection
    #   "Approved"   -> Candidate is hired!
    stage = Column(String(20), default="Applied", nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ---- Relationship ----
    # This lets us access the job details directly from an application object.
    # Example: application.job.title -> gives us "AI Engineer"
    # "lazy='joined'" means: when we load an application, also load its job data
    job = relationship("JobModel", lazy="joined")
