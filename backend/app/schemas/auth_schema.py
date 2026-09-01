# =============================================
# auth_schema.py - Authentication Data Validation
# =============================================
# WHAT ARE SCHEMAS (Pydantic Models)?
#   Schemas validate the data that comes IN (requests)
#   and the data that goes OUT (responses).
#
#   Think of it like a security guard at a club:
#   - "You need an email AND password to enter" (request validation)
#   - "Here's your access token" (response format)
#
#   If someone sends bad data (e.g., missing email),
#   Pydantic automatically returns a clear error message.
# =============================================

from pydantic import BaseModel, EmailStr  # BaseModel = base for all schemas


class LoginRequest(BaseModel):
    """
    What the admin must send to log in.
    
    Example request body:
    {
        "email": "admin@enter.in",
        "password": "admin123"
    }
    """
    email: str        # Admin's email address
    password: str     # Admin's password (plain text - we'll verify it against the hash)


class RegisterRequest(BaseModel):
    """
    What a new user must send to create an account (Sign Up).
    
    Example request body:
    {
        "email": "newadmin@enter.in",
        "password": "securePassword123",
        "confirm_password": "securePassword123"
    }
    """
    email: str              # New user's email address
    password: str           # Password (min 6 characters recommended)
    confirm_password: str   # Must match password exactly


class TokenResponse(BaseModel):
    """
    What the server sends back after successful login.
    
    Example response:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "token_type": "bearer"
    }
    """
    access_token: str   # The JWT token (a long encoded string)
    token_type: str     # Always "bearer" (it's a standard)


class UserResponse(BaseModel):
    """
    User info returned when checking "who am I?" (GET /api/auth/me).
    
    Example response:
    {
        "id": 1,
        "email": "admin@enter.in",
        "role": "admin"
    }
    
    NOTE: We NEVER return the password in any response!
    """
    id: int
    email: str
    role: str

    class Config:
        # This tells Pydantic to work with SQLAlchemy model objects
        # Without this, Pydantic can't read data from our database models
        from_attributes = True
