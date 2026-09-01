# =============================================
# security.py - Password Hashing & JWT Auth Utilities
# =============================================
# This file provides functions to:
#   1. Hash passwords so plain text passwords are never stored in DB
#   2. Verify plain password against hashed password on login
#   3. Create JSON Web Tokens (JWT) for logged-in sessions
#   4. Verify JWT tokens and protect admin endpoints
# =============================================

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.repositories.user_repository import user_repository
from app.models.user_model import UserModel

# ---- Password Hashing Setup ----
# CryptContext manages password hashing algorithms.
# We use bcrypt - the gold standard for password security.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- OAuth2 Scheme for Token Extraction ----
# This tells FastAPI to extract the Bearer token from the HTTP Authorization header:
# "Authorization: Bearer <your_jwt_token_here>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    """
    Takes a plain password (e.g. "admin123") and returns a secure hash
    (e.g. "$2b$12$e8Zbw...").
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain text password matches the hashed password stored in the DB.
    Returns True if correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a secure signed JWT token containing the user's data (e.g., user_id and email).
    The token will expire after ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode token with SECRET_KEY and HMAC-SHA256 algorithm
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """
    FASTAPI DEPENDENCY:
    Protects any route that requires admin login.
    
    How it works:
      1. Grabs the Bearer token from the request header.
      2. Decodes the token using our SECRET_KEY.
      3. Checks if the user exists in our database.
      4. If valid, returns the UserModel object.
      5. If invalid/expired, returns HTTP 401 Unauthorized immediately.
    
    Usage in routes:
        @router.post("/jobs")
        def create_job(current_admin: UserModel = Depends(get_current_admin)):
            # This code only runs if the user is a verified logged-in admin!
            ...
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or session expired. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    # Check that the user still exists in the DB
    user = user_repository.get_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception

    return user
