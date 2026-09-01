# =============================================
# auth_routes.py - API Endpoints for Authentication
# =============================================
# WHAT IS A ROUTE FILE?
#   Routes define the URL endpoints that the frontend calls.
#   They receive the request, hand it over to the Controller,
#   and return the response back to the client.
# =============================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.controllers.auth_controller import auth_controller
from app.utils.security import get_current_admin
from app.models.user_model import UserModel

# APIRouter lets us group related routes under a common prefix and tag
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication (Login & Register)"]
)


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    **Admin Login Endpoint (Public)**
    
    Accepts email and password, verifies credentials,
    and returns a JWT bearer access token.
    
    - Default Email: `admin@enter.in`
    - Default Password: `admin123`
    """
    return auth_controller.login(db=db, login_data=login_data)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    **Register / Sign Up Endpoint (Public)**
    
    Creates a new admin user account.
    Requires: email, password, confirm_password.
    
    Validations:
    - Passwords must match
    - Password must be at least 6 characters
    - Email must not already be registered
    """
    return auth_controller.register(db=db, register_data=register_data)


@router.get("/me", response_model=UserResponse)
def get_current_user(current_admin: UserModel = Depends(get_current_admin)):
    """
    **Get Current Admin Profile (Protected)**
    
    Requires Bearer Token in Authorization header.
    Returns the logged-in admin's profile information.
    """
    return auth_controller.get_current_user_profile(current_user=current_admin)
