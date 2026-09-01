# =============================================
# application_repository.py - Database Queries for Applications
# =============================================
# This file handles all database operations for candidate applications:
#   - Saving candidate submissions (with uploaded resume details)
#   - Multi-condition filtering (filter by job, filter by hiring stage, search by name/email)
#   - Changing candidate hiring pipeline stage (Applied, R1, Reject, Approved, etc.)
# =============================================

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.application_model import ApplicationModel


class ApplicationRepository:
    """
    Handles all database operations for the 'applications' table.
    """

    def create(
        self,
        db: Session,
        job_id: int,
        full_name: str,
        email: str,
        phone: str,
        brief_note: Optional[str] = None,
        resume_filename: Optional[str] = None,
        resume_path: Optional[str] = None
    ) -> ApplicationModel:
        """
        Save a new candidate application into the database.
        Default stage is automatically set to "Applied".
        """
        new_app = ApplicationModel(
            job_id=job_id,
            full_name=full_name,
            email=email,
            phone=phone,
            brief_note=brief_note,
            resume_filename=resume_filename,
            resume_path=resume_path,
            stage="Applied"  # Initial stage
        )
        db.add(new_app)
        db.commit()
        db.refresh(new_app)
        return new_app

    def get_all(
        self,
        db: Session,
        job_id: Optional[int] = None,
        stage: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[ApplicationModel]:
        """
        Fetch applications with dynamic multi-filtering:
          - Filter by specific Job (job_id)
          - Filter by Pipeline Stage (Applied, R1, R2, R3, Reject, Approved, etc.)
          - Search by Candidate Name or Email
        
        SQL Equivalent (example):
            SELECT * FROM applications
            WHERE job_id = 1 AND stage = 'Applied' AND (full_name LIKE '%rahul%' OR email LIKE '%rahul%')
            ORDER BY created_at DESC;
        """
        query = db.query(ApplicationModel)

        # 1. Apply Job Filter if provided
        if job_id is not None:
            query = query.filter(ApplicationModel.job_id == job_id)

        # 2. Apply Stage Filter if provided
        if stage is not None and stage.strip() != "":
            query = query.filter(ApplicationModel.stage == stage)

        # 3. Apply Search Filter if provided (checks both name and email)
        if search is not None and search.strip() != "":
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    ApplicationModel.full_name.ilike(search_pattern),
                    ApplicationModel.email.ilike(search_pattern)
                )
            )

        # Always return the newest applications first
        return query.order_by(ApplicationModel.created_at.desc()).all()

    def get_by_id(self, db: Session, application_id: int) -> Optional[ApplicationModel]:
        """
        Find a single application by its ID.
        """
        return db.query(ApplicationModel).filter(ApplicationModel.id == application_id).first()

    def update_stage(self, db: Session, application_id: int, new_stage: str) -> Optional[ApplicationModel]:
        """
        Move a candidate to a new hiring stage.
        Example: "Applied" -> "R1" or "R2 Reject" -> "Reject" or "R3" -> "Approved"
        """
        db_app = self.get_by_id(db, application_id)
        if not db_app:
            return None

        db_app.stage = new_stage
        db.commit()
        db.refresh(db_app)
        return db_app

    def count_by_stage(self, db: Session) -> dict:
        """
        Returns summary statistics for the admin dashboard:
        Counts how many candidates are in each stage.
        """
        apps = db.query(ApplicationModel).all()
        stats = {
            "total": len(apps),
            "applied": 0,
            "r1": 0,
            "r2": 0,
            "r3": 0,
            "approved": 0,
            "rejected": 0
        }
        for app in apps:
            stage_lower = app.stage.lower()
            if "applied" in stage_lower:
                stats["applied"] += 1
            elif "r1" in stage_lower and "reject" not in stage_lower:
                stats["r1"] += 1
            elif "r2" in stage_lower and "reject" not in stage_lower:
                stats["r2"] += 1
            elif "r3" in stage_lower and "reject" not in stage_lower:
                stats["r3"] += 1
            elif "approved" in stage_lower:
                stats["approved"] += 1
            elif "reject" in stage_lower:
                stats["rejected"] += 1

        return stats


# Create a reusable instance of ApplicationRepository
application_repository = ApplicationRepository()
