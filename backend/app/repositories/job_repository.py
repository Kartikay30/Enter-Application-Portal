# =============================================
# job_repository.py - Database Queries for Jobs
# =============================================
# This file performs all CRUD operations for the 'jobs' table:
#   - C = Create (add a new job)
#   - R = Read (get all jobs or get one job by ID)
#   - U = Update (edit job title, description, status, etc.)
#   - D = Delete (remove a job)
# =============================================

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.job_model import JobModel
from app.schemas.job_schema import JobCreate, JobUpdate


class JobRepository:
    """
    Handles all database operations for the 'jobs' table.
    """

    def get_all(self, db: Session, active_only: bool = False) -> List[JobModel]:
        """
        Get all jobs from the database.
        
        Parameters:
            - active_only: If True, returns only jobs where status == 'Active'
              (Useful for candidate application dropdown!)
              If False, returns all jobs (for admin dashboard).
        
        SQL Equivalent:
            SELECT * FROM jobs WHERE status = 'Active' ORDER BY created_at DESC;
        """
        query = db.query(JobModel)
        if active_only:
            query = query.filter(JobModel.status == "Active")
        return query.order_by(JobModel.created_at.desc()).all()

    def get_by_id(self, db: Session, job_id: int) -> Optional[JobModel]:
        """
        Find a specific job by its ID.
        
        SQL Equivalent:
            SELECT * FROM jobs WHERE id = :job_id LIMIT 1;
        """
        return db.query(JobModel).filter(JobModel.id == job_id).first()

    def create(self, db: Session, job_data: JobCreate) -> JobModel:
        """
        Insert a new job into the database.
        
        SQL Equivalent:
            INSERT INTO jobs (title, department, location, job_type, description, requirements, status)
            VALUES (...);
        """
        new_job = JobModel(
            title=job_data.title,
            department=job_data.department,
            location=job_data.location,
            job_type=job_data.job_type,
            description=job_data.description,
            requirements=job_data.requirements,
            status=job_data.status
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job

    def update(self, db: Session, job_id: int, job_update: JobUpdate) -> Optional[JobModel]:
        """
        Update an existing job.
        Only updates fields that were actually provided (not None).
        
        SQL Equivalent:
            UPDATE jobs SET title = :new_title, ... WHERE id = :job_id;
        """
        db_job = self.get_by_id(db, job_id)
        if not db_job:
            return None

        # Convert the Pydantic schema to a dictionary, excluding fields that weren't set
        update_dict = job_update.model_dump(exclude_unset=True)

        for field_name, new_value in update_dict.items():
            setattr(db_job, field_name, new_value)

        db.commit()
        db.refresh(db_job)
        return db_job

    def delete(self, db: Session, job_id: int) -> bool:
        """
        Delete a job by its ID.
        Returns True if deleted, False if job was not found.
        
        SQL Equivalent:
            DELETE FROM jobs WHERE id = :job_id;
        """
        db_job = self.get_by_id(db, job_id)
        if not db_job:
            return False

        db.delete(db_job)
        db.commit()
        return True

    def count(self, db: Session) -> int:
        """
        Get the total count of jobs in the database.
        Used by the auto-seeder to check if initial jobs need to be inserted.
        """
        return db.query(JobModel).count()


# Create a reusable instance of JobRepository
job_repository = JobRepository()
