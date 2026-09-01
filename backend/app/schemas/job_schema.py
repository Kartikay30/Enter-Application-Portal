# =============================================
# job_schema.py - Job Data Validation
# =============================================
# These schemas control what data is accepted when
# creating/editing jobs, and what data is sent back
# in API responses.
# =============================================

from pydantic import BaseModel  # Base class for all schemas
from typing import Optional     # For fields that are not required
from datetime import datetime   # For timestamp fields


class JobCreate(BaseModel):
    """
    Data required to CREATE a new job.
    The admin fills a form and sends this data.
    
    Example request body:
    {
        "title": "AI Engineer",
        "department": "Engineering",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "We are looking for an AI Engineer...",
        "requirements": "3+ years of Python experience..."
    }
    """
    title: str                          # Job title (required)
    department: str                     # Department name (required)
    location: str                       # Job location (required)
    job_type: str = "Full-time"         # Employment type (defaults to "Full-time")
    description: str                    # Detailed description (required)
    requirements: Optional[str] = None  # Qualifications (optional)
    status: str = "Active"              # Default status when creating a job


class JobUpdate(BaseModel):
    """
    Data for UPDATING an existing job.
    All fields are Optional because the admin might
    only want to change the title without touching other fields.
    
    Example: Admin only wants to change location:
    {
        "location": "Bangalore, India"
    }
    """
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    status: Optional[str] = None


class JobResponse(BaseModel):
    """
    Data sent back to the frontend when fetching jobs.
    This is what the React app receives.
    
    Example response:
    {
        "id": 1,
        "title": "AI Engineer",
        "department": "Engineering",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "We are looking for...",
        "requirements": "3+ years...",
        "status": "Active",
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    }
    """
    id: int
    title: str
    department: str
    location: str
    job_type: str
    description: str
    requirements: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Allows Pydantic to read data from SQLAlchemy model objects
        from_attributes = True
