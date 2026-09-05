# =============================================
# seed.py - Database Initializer & Seeder
# =============================================
# This file automatically populates our database with:
#   1. The default Admin account: admin@enter.in (Password: admin123)
#   2. 10 realistic Job listings across tech domains
#   3. A few initial sample candidate applications in various pipeline stages
#
# This ensures that when someone starts the app for the first time,
# everything is already ready to test without manual data entry!
# =============================================

from sqlalchemy.orm import Session
from app.config import settings
from app.utils.security import hash_password
from app.repositories.user_repository import user_repository
from app.repositories.job_repository import job_repository
from app.schemas.job_schema import JobCreate
from app.models.application_model import ApplicationModel


# 10 Seed Jobs across engineering, AI, design, and product
SEED_JOBS = [
    {
        "title": "Full Stack Developer",
        "department": "Engineering",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Develop and maintain robust web applications using React, Python FastAPI, and PostgreSQL. You will build end-to-end features, optimize database queries, and contribute to architectural decisions.",
        "requirements": "Proficiency in JavaScript/React, Python (FastAPI/Django), REST APIs, SQL, and Git. Experience with Docker and cloud deployments is a plus.",
        "status": "Active"
    },
    {
        "title": "AI / ML Engineer",
        "department": "Artificial Intelligence",
        "location": "Bangalore, India",
        "job_type": "Full-time",
        "description": "Design, build, and deploy generative AI agents, LLM pipelines, and custom machine learning models to solve complex enterprise problems.",
        "requirements": "Strong Python skills, experience with PyTorch/TensorFlow, LangChain/LlamaIndex, OpenAI/Anthropic APIs, vector databases, and prompt engineering.",
        "status": "Active"
    },
    {
        "title": "Frontend Engineer (React)",
        "department": "Frontend Engineering",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Craft intuitive, performant, and visually stunning user interfaces. Collaborate closely with UI/UX designers to translate Figma mockups into reusable component systems.",
        "requirements": "3+ years with React, TypeScript, Tailwind CSS, State Management (Zustand/Redux), responsive web design, and web performance optimization.",
        "status": "Active"
    },
    {
        "title": "Backend Engineer (Python / FastAPI)",
        "department": "Backend Engineering",
        "location": "Hyderabad, India",
        "job_type": "Full-time",
        "description": "Architect high-throughput REST and WebSocket APIs, design scalable database schemas, and ensure bank-grade security and reliability across services.",
        "requirements": "Strong Python fundamentals, FastAPI/asyncio, SQLAlchemy, PostgreSQL, Redis caching, microservices architecture, and automated testing.",
        "status": "Active"
    },
    {
        "title": "UI / UX Product Designer",
        "department": "Product Design",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Own the end-to-end design lifecycle for our web and mobile applications. Create wireframes, interactive prototypes, and comprehensive design systems.",
        "requirements": "Mastery of Figma, strong visual hierarchy sense, deep user empathy, usability testing experience, and ability to build scalable design component libraries.",
        "status": "Active"
    },
    {
        "title": "DevOps & Cloud Engineer",
        "department": "Infrastructure",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Manage our multi-region AWS infrastructure, establish CI/CD pipelines with GitHub Actions, monitor system uptime, and automate deployment workflows.",
        "requirements": "Experience with AWS, Docker, Kubernetes, Terraform, Linux systems administration, Prometheus/Grafana monitoring, and CI/CD pipelines.",
        "status": "Active"
    },
    {
        "title": "AI Fullstack Intern",
        "department": "Engineering",
        "location": "Remote",
        "job_type": "Internship",
        "description": "Exciting 6-month internship building cutting-edge full-stack AI features with React, FastAPI, and generative AI models. High potential for full-time conversion.",
        "requirements": "Passion for web development and AI, foundational knowledge of Python, React, JavaScript, Git, and eagerness to learn quickly.",
        "status": "Active"
    },
    {
        "title": "Mobile App Developer (React Native)",
        "department": "Mobile Engineering",
        "location": "Bangalore, India",
        "job_type": "Full-time",
        "description": "Build and release cross-platform iOS and Android applications. Ensure fluid 60fps animations, offline-first data sync, and seamless native module integrations.",
        "requirements": "Proven experience building React Native applications, Expo, Redux/Zustand, native bridge debugging, App Store & Google Play publishing.",
        "status": "Active"
    },
    {
        "title": "Data Analyst / BI Specialist",
        "department": "Data & Analytics",
        "location": "Mumbai, India",
        "job_type": "Full-time",
        "description": "Transform complex user behavior and hiring metrics into actionable business intelligence dashboards and executive insights.",
        "requirements": "Advanced SQL, Python for data manipulation (Pandas, NumPy), Tableau / PowerBI / Metabase, and statistical modeling fundamentals.",
        "status": "Active"
    },
    {
        "title": "QA Automation Engineer",
        "department": "Quality Assurance",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Develop comprehensive automated test suites (E2E, integration, unit) to maintain top-tier software reliability and catch regressions early.",
        "requirements": "Experience with Playwright / Cypress / Selenium, pytest for API test automation, Postman, CI/CD test integration, and performance load testing.",
        "status": "Active"
    }
]


def seed_database(db: Session) -> None:
    """
    Main seed function executed on server startup.
    """
    print("[SEED] Checking database initialization...")

    # 1. Seed Default Admin User
    admin_email = settings.ADMIN_EMAIL
    admin_user = user_repository.get_by_email(db, email=admin_email)
    if not admin_user:
        print(f"[SEED] Creating default admin account: {admin_email}")
        hashed_pwd = hash_password(settings.ADMIN_PASSWORD)
        user_repository.create(
            db=db,
            email=admin_email,
            hashed_password=hashed_pwd,
            role="admin"
        )
        print(f"[SEED] Admin created successfully (Password: {settings.ADMIN_PASSWORD})")
    else:
        print(f"[SEED] Admin account '{admin_email}' already exists.")

    # 2. Seed 10 Jobs
    job_count = job_repository.count(db)
    if job_count == 0:
        print(f"[SEED] Seeding {len(SEED_JOBS)} initial jobs...")
        created_jobs = []
        for job_data in SEED_JOBS:
            job_obj = job_repository.create(db, job_data=JobCreate(**job_data))
            created_jobs.append(job_obj)
        print(f"[SEED] Successfully seeded {len(created_jobs)} jobs.")

        # 3. Seed Sample Applications (demonstrates pipeline stages)
        print("[SEED] Seeding sample candidate applications...")
        sample_applications = [
            {
                "job_id": created_jobs[0].id,
                "full_name": "Aarav Sharma",
                "email": "aarav.sharma@example.com",
                "phone": "+91 98765 43210",
                "brief_note": "Experienced Full Stack Developer with 4 years in React and FastAPI. Excited to contribute to Enter's rapid growth.",
                "resume_filename": "aarav_sharma_resume.pdf",
                "resume_path": None,
                "stage": "Applied",
                "stage_reason": "Application received and under preliminary review."
            },
            {
                "job_id": created_jobs[1].id,
                "full_name": "Priya Patel",
                "email": "priya.patel@example.com",
                "phone": "+91 98123 45678",
                "brief_note": "AI researcher specializing in LLM agents and retrieval augmented generation. Published 2 research papers.",
                "resume_filename": "priya_patel_cv.pdf",
                "resume_path": None,
                "stage": "R1",
                "stage_reason": "Strong profile in LLMs and AI agent architectures. Shortlisted for Round 1 technical interview."
            },
            {
                "job_id": created_jobs[2].id,
                "full_name": "Rohan Verma",
                "email": "rohan.verma@example.com",
                "phone": "+91 97234 56789",
                "brief_note": "Frontend developer obsessed with web performance, 60fps animations, and accessible design systems.",
                "resume_filename": "rohan_verma_portfolio.pdf",
                "resume_path": None,
                "stage": "R2",
                "stage_reason": "Cleared Round 1 with distinction in React and state management. Advanced to Round 2 architecture interview."
            },
            {
                "job_id": created_jobs[6].id,
                "full_name": "Ananya Sen",
                "email": "ananya.sen@example.com",
                "phone": "+91 99345 67890",
                "brief_note": "Final year Computer Science student. Built 3 fullstack web apps and passionate about AI development.",
                "resume_filename": "ananya_sen_resume.pdf",
                "resume_path": None,
                "stage": "Approved",
                "stage_reason": "Outstanding project portfolio and problem-solving skills throughout all interview rounds. Selected for hire!"
            },
            {
                "job_id": created_jobs[3].id,
                "full_name": "Vikram Singh",
                "email": "vikram.singh@example.com",
                "phone": "+91 96456 78901",
                "brief_note": "Backend developer with strong SQL and microservices background. Looking for high scale challenges.",
                "resume_filename": "vikram_singh_resume.pdf",
                "resume_path": None,
                "stage": "R1 Reject",
                "stage_reason": "Lacks required depth in asynchronous Python concurrency and FastAPI framework."
            }
        ]

        for app_data in sample_applications:
            app = ApplicationModel(**app_data)
            db.add(app)
        db.commit()
        print("[SEED] Sample applications seeded successfully.")
    else:
        print(f"[SEED] Database already contains {job_count} jobs.")

    print("[SEED] Initialization complete!\n")
