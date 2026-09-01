# =============================================
# auth_controller.py - Business Logic for Authentication
# =============================================
# WHAT IS A CONTROLLER?
#   A controller sits between the route (HTTP endpoint) and repository (Database).
#   It handles the core business logic:
#   - Validates that user credentials are correct
#   - Throws error if wrong password
#   - Creates and returns JWT token
# =============================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.repositories.user_repository import user_repository
from app.utils.security import verify_password, hash_password, create_access_token
from app.models.user_model import UserModel


class AuthController:
    """
    Handles authentication business logic (Login + Register).
    """

    def login(self, db: Session, login_data: LoginRequest) -> TokenResponse:
        """
        Step-by-step login flow:
          1. Find the user by email in the database via UserRepository
          2. If user doesn't exist -> raise HTTP 401 Unauthorized
          3. Check if plain password matches stored hashed password
          4. If password doesn't match -> raise HTTP 401 Unauthorized
          5. If valid -> generate and return a signed JWT token
        """
        # 1. Look up user by email
        user = user_repository.get_by_email(db, email=login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please check your credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 2. Check password
        is_password_valid = verify_password(login_data.password, user.hashed_password)
        if not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please check your credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Create access token with user_id inside payload
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(data=token_data)

        # 4. Return token response
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )

    def register(self, db: Session, register_data: RegisterRequest) -> UserResponse:
        """
        Step-by-step registration (Sign Up) flow:
          1. Check if passwords match
          2. Check password length (min 6 characters)
          3. Check if email is already taken
          4. Hash the password
          5. Create the new user in the database
          6. Return the created user profile
        """
        # 1. Verify passwords match
        if register_data.password != register_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match. Please re-enter."
            )

        # 2. Validate password strength
        if len(register_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long."
            )

        # 3. Check if email already exists
        existing_user = user_repository.get_by_email(db, email=register_data.email.strip().lower())
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An account with email '{register_data.email}' already exists. Please log in instead."
            )

        # 4. Hash the password securely
        hashed_pwd = hash_password(register_data.password)

        # 5. Create new user via repository
        new_user = user_repository.create(
            db=db,
            email=register_data.email.strip().lower(),
            hashed_password=hashed_pwd,
            role="admin"
        )

        # 6. Return created user info
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            role=new_user.role
        )

    def get_current_user_profile(self, current_user: UserModel) -> UserResponse:
        """
        Returns profile info of the currently authenticated admin.
        """
        return UserResponse(
            id=current_user.id,
            email=current_user.email,
            role=current_user.role
        )


# Reusable singleton instance
auth_controller = AuthController()
