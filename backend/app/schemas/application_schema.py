# =============================================
# application_schema.py - Candidate Application Data Validation
# =============================================
# These schemas handle:
# 1. What data a candidate sends when applying (ApplicationCreate)
# 2. What data the admin sends to change a candidate's stage (StageUpdate)
# 3. What data is sent back in responses (ApplicationResponse)
#
# NOTE: The resume FILE is handled separately (as a file upload),
# not through these schemas. These only handle text/JSON data.
# =============================================

from pydantic import BaseModel  # Base class for schemas
from typing import Optional     # For optional fields
from datetime import datetime   # For timestamp fields


class ApplicationCreate(BaseModel):
    """
    Data a candidate provides when applying for a job.
    
    NOTE: The resume file is uploaded separately as a file,
    not as part of this JSON body. The route handler combines
    this data with the uploaded file info.
    
    Example:
    {
        "job_id": 1,
        "full_name": "Rahul Sharma",
        "email": "rahul@example.com",
        "phone": "9876543210",
        "brief_note": "I am passionate about AI and have 2 years of experience..."
    }
    """
    job_id: int                          # Which job they're applying for
    full_name: str                       # Candidate's full name
    email: str                           # Candidate's email
    phone: str                           # Candidate's phone number
    brief_note: Optional[str] = None     # Optional cover note / message


class StageUpdate(BaseModel):
    """
    Data the admin sends to move a candidate to a new stage.
    
    Example:
    {
        "stage": "R1"
    }
    
    Valid stages:
        "Applied", "R1", "R1 Reject", "R2", "R2 Reject",
        "R3", "R3 Reject", "Reject", "Approved"
    """
    stage: str  # The new stage to move the candidate to
    reason: Optional[str] = None  # Reason for stage move, selection, or rejection


class ApplicationResponse(BaseModel):
    """
    Complete application data sent back in API responses.
    Includes all candidate info + the job title they applied for.
    """
    id: int
    job_id: Optional[int] = None
    job_title: Optional[str] = None          # We'll fill this from the related Job
    full_name: str
    email: str
    phone: str
    brief_note: Optional[str] = None
    resume_filename: Optional[str] = None
    stage: str
    stage_reason: Optional[str] = None       # Reason for current stage / decision
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Allows Pydantic to read from SQLAlchemy objects
        from_attributes = True
