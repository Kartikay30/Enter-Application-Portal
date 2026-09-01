# =============================================
# user_repository.py - Database Queries for Admin Users
# =============================================
# WHAT IS A REPOSITORY?
#   A repository is the ONLY place in the codebase that talks directly
#   to the database using SQLAlchemy.
#
#   Why do we do this?
#   - Keeps database queries organized in one place.
#   - If database logic changes, we only modify this file!
#   - Controllers and routes stay clean and simple.
# =============================================

from sqlalchemy.orm import Session
from typing import Optional
from app.models.user_model import UserModel


class UserRepository:
    """
    Handles all database operations related to the 'users' table.
    """

    def get_by_email(self, db: Session, email: str) -> Optional[UserModel]:
        """
        Find a user by their email address.
        Used during admin login to check if the account exists.
        
        SQL Equivalent:
            SELECT * FROM users WHERE email = :email LIMIT 1;
        """
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> Optional[UserModel]:
        """
        Find a user by their unique ID.
        Used to verify that the admin token belongs to an existing user.
        
        SQL Equivalent:
            SELECT * FROM users WHERE id = :user_id LIMIT 1;
        """
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    def create(self, db: Session, email: str, hashed_password: str, role: str = "admin") -> UserModel:
        """
        Create and save a new user to the database.
        Used by our auto-seed script on startup.
        
        SQL Equivalent:
            INSERT INTO users (email, hashed_password, role) VALUES (...);
        """
        new_user = UserModel(
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        db.add(new_user)       # Stage the new user object
        db.commit()            # Save changes permanently to database
        db.refresh(new_user)   # Refresh to get auto-generated fields (like id, created_at)
        return new_user


# Create a reusable instance of UserRepository
user_repository = UserRepository()
