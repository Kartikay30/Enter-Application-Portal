# =============================================
# job_controller.py - Business Logic for Job Operations
# =============================================
# This file handles business logic for jobs:
#   - Fetching active jobs for public candidate dropdown
#   - Fetching all jobs for admin dashboard
#   - Creating new jobs
#   - Updating existing jobs
#   - Deleting jobs
# =============================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse
from app.repositories.job_repository import job_repository


class JobController:
    """
    Business logic for Job management.
    """

    def get_all_jobs(self, db: Session, active_only: bool = False) -> List[JobResponse]:
        """
        Retrieves all jobs and transforms them into JobResponse schemas.
        """
        jobs = job_repository.get_all(db, active_only=active_only)
        return [JobResponse.model_validate(job) for job in jobs]

    def get_job_by_id(self, db: Session, job_id: int) -> JobResponse:
        """
        Retrieves a single job by ID or raises 404 if not found.
        """
        job = job_repository.get_by_id(db, job_id=job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} was not found."
            )
        return JobResponse.model_validate(job)

    def create_job(self, db: Session, job_data: JobCreate) -> JobResponse:
        """
        Validates and creates a new job listing.
        """
        created_job = job_repository.create(db, job_data=job_data)
        return JobResponse.model_validate(created_job)

    def update_job(self, db: Session, job_id: int, job_update: JobUpdate) -> JobResponse:
        """
        Updates an existing job or raises 404 if not found.
        """
        updated_job = job_repository.update(db, job_id=job_id, job_update=job_update)
        if not updated_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cannot update: Job with ID {job_id} was not found."
            )
        return JobResponse.model_validate(updated_job)

    def delete_job(self, db: Session, job_id: int) -> dict:
        """
        Deletes a job or raises 404 if not found.
        """
        success = job_repository.delete(db, job_id=job_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cannot delete: Job with ID {job_id} was not found."
            )
        return {"message": f"Job {job_id} deleted successfully."}


# Reusable singleton instance
job_controller = JobController()
