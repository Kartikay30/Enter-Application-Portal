# Enter - Candidate Application & Hiring Management System (ATS)

A full-stack Recruitment & Applicant Tracking System built with **React (Frontend)** and **FastAPI (Backend)** adhering to a clean, beginner-friendly **Layered Repository Architecture**.

---

## 🌟 Key Features

### 1. Public Candidate Application Portal (`/`)
- Open portal for any job candidate to apply for active positions.
- **Job Dropdown**: Pre-seeded with 10 realistic jobs across AI, engineering, and design.
- **Application Form**: Captures Name, Phone, Email, Brief Note / Cover Letter, and Resume Upload (PDF/DOCX).
- **Validation & Feedback**: Instant file size/type validation and confirmation screen upon submission.

### 2. Admin Authentication (`/admin/login`)
- Protected authentication for the hiring team.
- **Pre-seeded Admin Account**:
  - **Email**: `admin@enter.in`
  - **Password**: `admin123`
- JWT-based authentication with auto-redirect on session expiry.

### 3. Admin ATS Dashboard (`/admin/dashboard`)
- **Job Management (CRUD)**: Create, edit, toggle active status, and delete jobs.
- **Applicant Review**: View all candidate details, timestamps, notes, and direct resume downloads.
- **Multi-Filter System**:
  - Filter candidates by specific Job
  - Filter candidates by Hiring Stage
  - Search candidates by Name or Email
- **Hiring Pipeline Stage Mover**: Move applicants between pipeline stages with a single click:
  - `Applied (Initial)`
  - `R1` / `R1 Reject`
  - `R2` / `R2 Reject`
  - `R3` / `R3 Reject`
  - `Reject`
  - `Approved (Hired)`

---

## 🏗️ Architecture & Folder Structure

```text
enter-assignment/
├── backend/                       # FastAPI Python Backend
│   ├── app/
│   │   ├── main.py                # App entry point, CORS & startup seeders
│   │   ├── config.py              # Centralized environment settings
│   │   ├── db/
│   │   │   ├── database.py        # SQLAlchemy SQLite engine & get_db dependency
│   │   │   └── seed.py            # Auto-seed script for admin@enter.in & 10 jobs
│   │   ├── models/                # SQLAlchemy Database Tables
│   │   │   ├── user_model.py      # Admin table
│   │   │   ├── job_model.py       # Job openings table
│   │   │   └── application_model.py # Candidate applications table
│   │   ├── schemas/               # Pydantic validation schemas
│   │   │   ├── auth_schema.py
│   │   │   ├── job_schema.py
│   │   │   └── application_schema.py
│   │   ├── repositories/          # 100% Database Queries (CRUD)
│   │   │   ├── user_repository.py
│   │   │   ├── job_repository.py
│   │   │   └── application_repository.py
│   │   ├── controllers/           # Business Logic
│   │   │   ├── auth_controller.py
│   │   │   ├── job_controller.py
│   │   │   └── application_controller.py
│   │   ├── routes/                # API Endpoints
│   │   │   ├── auth_routes.py
│   │   │   ├── job_routes.py
│   │   │   └── application_routes.py
│   │   ├── utils/
│   │   │   ├── security.py        # Bcrypt hashing & JWT token generator
│   │   │   └── file_handler.py    # Resume upload & validation utils
│   │   └── uploads/               # Saved candidate resume documents
│   ├── requirements.txt           # Python dependencies
│   ├── run.py                     # Backend startup script (python run.py)
│   └── test_api.py                # Automated integration test suite
│
├── frontend/                      # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/            # Navbar, StageBadge, JobModal, CandidateModal, ProtectedRoute, Toast
│   │   ├── context/               # AuthContext (global user state)
│   │   ├── pages/                 # ApplyPage, AdminLogin, AdminDashboard, NotFound
│   │   ├── services/              # Axios API client (authService, jobService, applicationService)
│   │   ├── utils/                 # Stage color constants
│   │   ├── App.jsx                # Router configuration
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js             # Vite config with Tailwind & API proxy
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Start the Backend (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server (auto-creates database and seeds admin@enter.in + 10 jobs)
python run.py
```
- API Server: `http://localhost:8000`
- Interactive Swagger API Docs: `http://localhost:8000/docs`

### 2. Start the Frontend (React + Vite)

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install packages
npm install

# Start the development server
npm run dev
```
- Candidate Application Page: `http://localhost:5173/`
- Admin Login: `http://localhost:5173/admin/login` (or click "Admin Portal" in navbar)

---

## 🧪 Running Automated Tests

To run the backend integration test suite:

```bash
cd backend
python test_api.py
```

---

## 🌐 Online Deployment Guide

### Deploy Backend to Render / Railway
1. Push your repository to GitHub.
2. In [Render](https://render.com), create a **New Web Service**.
3. Set **Root Directory** to `backend`.
4. Set **Build Command** to: `pip install -r requirements.txt`
5. Set **Start Command** to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Deploy Frontend to Vercel
1. In [Vercel](https://vercel.com), import your repository.
2. Set **Root Directory** to `frontend`.
3. Set **Framework Preset** to `Vite`.
4. Add environment variable `VITE_API_BASE_URL` pointing to your deployed backend URL.
5. Click **Deploy**.
