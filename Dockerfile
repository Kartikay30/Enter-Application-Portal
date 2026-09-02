# =============================================
# Dockerfile - Railway Deployment (Multi-Stage Build)
# =============================================
# Stage 1: Build the React frontend with Node.js
# Stage 2: Run the FastAPI backend with Python + serve React build
# =============================================

# ---- Stage 1: Build React Frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /frontend

# Copy package files first (for better Docker caching)
COPY frontend/package.json frontend/package-lock.json ./

# Install Node.js dependencies
RUN npm ci

# Copy all frontend source code
COPY frontend/ ./

# Build the React app (output goes to /frontend/dist/)
RUN npm run build


# ---- Stage 2: Python Backend + Serve React ----
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies first (for better Docker caching)
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY backend/ ./

# Copy the React build from Stage 1 into backend/static/
COPY --from=frontend-build /frontend/dist ./static/

# Create uploads directory
RUN mkdir -p app/uploads

# Railway sets PORT environment variable automatically
ENV PORT=8000

# Expose the port
EXPOSE ${PORT}

# Start the FastAPI server
CMD ["python", "run.py"]
