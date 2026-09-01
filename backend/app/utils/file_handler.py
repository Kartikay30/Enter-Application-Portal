# =============================================
# file_handler.py - Resume File Upload Utilities
# =============================================
# This file manages saving candidate resumes uploaded from the form:
#   - Validates file extensions (PDF, DOC, DOCX)
#   - Generates unique file names using UUID to prevent overwriting
#   - Saves the file safely into the app/uploads/ directory
# =============================================

import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException, status
from app.config import settings

# Allowed file extensions for resumes
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
# Max file size: 10 MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024


def validate_file_extension(filename: str) -> str:
    """
    Validates that the uploaded file has an allowed extension (.pdf, .doc, .docx).
    Returns the lowercase extension if valid, else raises HTTP 400.
    """
    _, ext = os.path.splitext(filename)
    ext_lower = ext.lower()

    if ext_lower not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format '{ext}'. Only PDF, DOC, and DOCX files are allowed."
        )
    return ext_lower


async def save_uploaded_resume(file: UploadFile) -> tuple[str, str]:
    """
    Saves the uploaded file to disk asynchronously.
    
    Returns:
        tuple (original_filename, stored_relative_path)
        Example: ("my_resume.pdf", "app/uploads/123e4567-e89b_my_resume.pdf")
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename."
        )

    # 1. Validate file extension
    ext = validate_file_extension(file.filename)

    # 2. Ensure the upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # 3. Create a unique filename so two files with the same name don't overwrite each other
    # e.g., "7f9a1b2c_resume.pdf"
    unique_prefix = uuid.uuid4().hex[:8]
    safe_basename = "".join(c for c in file.filename if c.isalnum() or c in "._- ")
    stored_filename = f"{unique_prefix}_{safe_basename}"
    destination_path = os.path.join(settings.UPLOAD_DIR, stored_filename)

    # 4. Read content and verify size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 10MB."
        )

    # 5. Write file to disk asynchronously
    async with aiofiles.open(destination_path, "wb") as out_file:
        await out_file.write(contents)

    # Reset file pointer if needed
    await file.seek(0)

    # Normalizing path separators to forward slash for cross-platform compatibility
    normalized_path = destination_path.replace("\\", "/")

    return file.filename, normalized_path
