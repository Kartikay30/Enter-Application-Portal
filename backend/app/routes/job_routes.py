# =============================================
# job_routes.py - API Endpoints for Job Openings
# =============================================
# Routes for managing job listings:
#   - GET /api/jobs (Public: candidate dropdown & admin dashboard)
#   - GET /api/jobs/{id} (Public: view single job)
#   - POST /api/jobs (Admin: create new job)
#   - PUT /api/jobs/{id} (Admin: edit existing job)
#   - DELETE /api/jobs/{id} (Admin: delete job)
# =============================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse
from app.controllers.job_controller import job_controller
from app.utils.security import get_current_admin
from app.models.user_model import UserModel

router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs (CRUD & Candidate Portal)"]
)


@router.get("", response_model=List[JobResponse])
def get_jobs(
    active_only: bool = Query(False, description="If true, returns only active jobs for the candidate form"),
    db: Session = Depends(get_db)
):
    """
    **List Jobs (Public)**
    
    - `active_only=true`: Used by the candidate application dropdown to list open positions.
    - `active_only=false`: Used by the admin dashboard to see all jobs (both Active and Closed).
    """
    return job_controller.get_all_jobs(db=db, active_only=active_only)


@router.get("/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    """
    **Get Single Job by ID (Public)**
    """
    return job_controller.get_job_by_id(db=db, job_id=job_id)


@router.post("", response_model=JobResponse, status_code=201)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **Create a New Job (Protected - Admin only)**
    
    Requires Bearer Token in Authorization header.
    """
    return job_controller.create_job(db=db, job_data=job_data)


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **Update an Existing Job (Protected - Admin only)**
    
    Allows modifying title, department, location, job_type, description, requirements, or status.
    """
    return job_controller.update_job(db=db, job_id=job_id, job_update=job_update)


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(get_current_admin)
):
    """
    **Delete a Job (Protected - Admin only)**
    """
    return job_controller.delete_job(db=db, job_id=job_id)
