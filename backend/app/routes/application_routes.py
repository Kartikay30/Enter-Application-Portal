# =============================================
# application_routes.py - API Endpoints for Candidate Applications
# =============================================
# Routes for candidate applications & hiring pipeline:
#   - POST /api/applications (Public: candidate submits application + uploads resume)
#   - GET /api/applications (Admin: view candidate list with job & stage filters + search)
#   - GET /api/applications/stats (Admin: pipeline count stats)
#   - GET /api/applications/{id} (Admin: single candidate details)
#   - PATCH /api/applications/{id}/stage (Admin: move candidate to next stage)
#   - GET /api/applications/{id}/resume (Admin/Public: download/view resume)
# =============================================

from fastapi import APIRouter, Depends, Form, File, UploadFile, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas.application_schema import ApplicationResponse, StageUpdate
from app.controllers.application_controller import application_controller
from app.utils.security import get_current_admin
from app.models.user_model import UserModel

router = APIRouter(
    prefix="/api/applications",
    tags=["Candidate Applications & ATS Pipeline"]
)


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    job_id: int = Form(..., description="ID of the job selected from dropdown"),
    full_name: str = Form(..., description="Candidate full name"),
    email: str = Form(..., description="Candidate email address"),
    phone: str = Form(..., description="Candidate phone number"),
    brief_note: Optional[str] = Form(None, description="Optional brief cover note"),
    resume: UploadFile = File(..., description="Resume file (PDF, DOC, DOCX - max 10MB)"),
    db: Session = Depends(get_db)
):
    """
    **Submit Job Application (Public - Candidate Form)**
    
    Accepts multipart/form-data with candidate information and uploaded resume file.
    Automatically assigns initial stage: `Applied`.
    """
    return await application_controller.submit_application(
        db=db,
        job_id=job_id,
        full_name=full_name,
        email=email,
        phone=phone,
        brief_note=brief_note,
        resume_file=resume
    )


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **Get Candidate Pipeline Stats (Protected - Admin only)**
    
    Returns counts for total, applied, R1, R2, R3, approved, and rejected.
    """
    return application_controller.get_dashboard_stats(db=db)


@router.get("", response_model=List[ApplicationResponse])
def get_applications(
    job_id: Optional[int] = Query(None, description="Filter candidates by specific job"),
    stage: Optional[str] = Query(None, description="Filter candidates by hiring stage"),
    search: Optional[str] = Query(None, description="Search by candidate name or email"),
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **List Candidate Applications (Protected - Admin only)**
    
    Supports multi-filtering:
      - Filter by Job ID (`?job_id=1`)
      - Filter by Stage (`?stage=R1` or `?stage=Applied`)
      - Search by candidate name or email (`?search=rahul`)
    """
    return application_controller.get_applications(
        db=db,
        job_id=job_id,
        stage=stage,
        search=search
    )


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(
    application_id: int,
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **Get Application Details by ID (Protected - Admin only)**
    """
    return application_controller.get_application_by_id(
        db=db, application_id=application_id
    )


@router.patch("/{application_id}/stage", response_model=ApplicationResponse)
def update_application_stage(
    application_id: int,
    stage_data: StageUpdate,
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **Move Candidate Stage (Protected - Admin only)**
    
    Valid stages:
    - `Applied`
    - `R1`
    - `R1 Reject`
    - `R2`
    - `R2 Reject`
    - `R3`
    - `R3 Reject`
    - `Reject`
    - `Approved`
    """
    return application_controller.update_stage(
        db=db,
        application_id=application_id,
        new_stage=stage_data.stage,
        reason=stage_data.reason
    )


@router.get("/{application_id}/resume")
def download_resume(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    **Download / View Candidate Resume (PDF/DOCX)**
    
    Returns the file with appropriate attachment headers for browser viewing/download.
    """
    file_path, original_filename = application_controller.get_resume_filepath(
        db=db, application_id=application_id
    )
    return FileResponse(
        path=file_path,
        filename=original_filename,
        media_type="application/octet-stream"
    )
