# =============================================
# application_controller.py - Business Logic for Applications
# =============================================
# This file handles candidate application logic:
#   - Saving candidate submissions and processing uploaded resumes
#   - Fetching applications with multi-filter and search support
#   - Moving candidates across pipeline stages:
#     Applied, R1, R1 Reject, R2, R2 Reject, R3, R3 Reject, Reject, Approved
#   - Serving candidate resumes for admin view/download
# =============================================

import os
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import List, Optional

from app.schemas.application_schema import ApplicationResponse
from app.repositories.application_repository import application_repository
from app.repositories.job_repository import job_repository
from app.utils.file_handler import save_uploaded_resume

# List of valid hiring pipeline stages as required by the assignment
VALID_STAGES = [
    "Applied",
    "R1",
    "R1 Reject",
    "R2",
    "R2 Reject",
    "R3",
    "R3 Reject",
    "Reject",
    "Approved"
]


class ApplicationController:
    """
    Business logic for candidate applications.
    """

    async def submit_application(
        self,
        db: Session,
        job_id: int,
        full_name: str,
        email: str,
        phone: str,
        brief_note: Optional[str],
        resume_file: UploadFile
    ) -> ApplicationResponse:
        """
        Processes a new candidate submission:
          1. Verifies that the selected job exists and is Active
          2. Validates and saves the uploaded resume file
          3. Creates database record via repository
          4. Returns formatted ApplicationResponse
        """
        # 1. Verify Job exists
        job = job_repository.get_by_id(db, job_id=job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Selected job ID {job_id} does not exist."
            )

        # 2. Save uploaded resume file
        original_filename, stored_path = await save_uploaded_resume(resume_file)

        # 3. Create record in DB
        app_model = application_repository.create(
            db=db,
            job_id=job_id,
            full_name=full_name.strip(),
            email=email.strip().lower(),
            phone=phone.strip(),
            brief_note=brief_note.strip() if brief_note else None,
            resume_filename=original_filename,
            resume_path=stored_path
        )

        # 4. Format and return response
        return ApplicationResponse(
            id=app_model.id,
            job_id=app_model.job_id,
            job_title=job.title if job else None,
            full_name=app_model.full_name,
            email=app_model.email,
            phone=app_model.phone,
            brief_note=app_model.brief_note,
            resume_filename=app_model.resume_filename,
            stage=app_model.stage,
            stage_reason=app_model.stage_reason,
            created_at=app_model.created_at,
            updated_at=app_model.updated_at
        )

    def get_applications(
        self,
        db: Session,
        job_id: Optional[int] = None,
        stage: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[ApplicationResponse]:
        """
        Retrieves applications filtered by job, stage, or candidate name/email.
        """
        apps = application_repository.get_all(db, job_id=job_id, stage=stage, search=search)
        
        results = []
        for app in apps:
            results.append(
                ApplicationResponse(
                    id=app.id,
                    job_id=app.job_id,
                    job_title=app.job.title if app.job else "General / Deleted Job",
                    full_name=app.full_name,
                    email=app.email,
                    phone=app.phone,
                    brief_note=app.brief_note,
                    resume_filename=app.resume_filename,
                    stage=app.stage,
                    stage_reason=app.stage_reason,
                    created_at=app.created_at,
                    updated_at=app.updated_at
                )
            )
        return results

    def get_application_by_id(self, db: Session, application_id: int) -> ApplicationResponse:
        """
        Fetches a single candidate application.
        """
        app = application_repository.get_by_id(db, application_id=application_id)
        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} was not found."
            )
        return ApplicationResponse(
            id=app.id,
            job_id=app.job_id,
            job_title=app.job.title if app.job else None,
            full_name=app.full_name,
            email=app.email,
            phone=app.phone,
            brief_note=app.brief_note,
            resume_filename=app.resume_filename,
            stage=app.stage,
            stage_reason=app.stage_reason,
            created_at=app.created_at,
            updated_at=app.updated_at
        )

    def update_stage(self, db: Session, application_id: int, new_stage: str, reason: Optional[str] = None) -> ApplicationResponse:
        """
        Updates the hiring stage and decision reason of a candidate.
        Validates that the stage is in the approved list.
        """
        if new_stage not in VALID_STAGES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid stage '{new_stage}'. Allowed stages: {', '.join(VALID_STAGES)}"
            )

        updated_app = application_repository.update_stage(
            db, application_id=application_id, new_stage=new_stage, reason=reason
        )
        if not updated_app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} was not found."
            )

        return ApplicationResponse(
            id=updated_app.id,
            job_id=updated_app.job_id,
            job_title=updated_app.job.title if updated_app.job else None,
            full_name=updated_app.full_name,
            email=updated_app.email,
            phone=updated_app.phone,
            brief_note=updated_app.brief_note,
            resume_filename=updated_app.resume_filename,
            stage=updated_app.stage,
            stage_reason=updated_app.stage_reason,
            created_at=updated_app.created_at,
            updated_at=updated_app.updated_at
        )

    def get_resume_filepath(self, db: Session, application_id: int) -> tuple[str, str]:
        """
        Retrieves the saved file path on disk for downloading/viewing the resume.
        Returns: (actual_file_path, original_filename)
        """
        app = application_repository.get_by_id(db, application_id=application_id)
        if not app or not app.resume_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found for this candidate."
            )

        if not os.path.exists(app.resume_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume file does not exist on disk."
            )

        return app.resume_path, app.resume_filename or "resume.pdf"

    def get_dashboard_stats(self, db: Session) -> dict:
        """
        Returns stats for admin dashboard summary metrics.
        """
        return application_repository.count_by_stage(db)


# Reusable singleton instance
application_controller = ApplicationController()
