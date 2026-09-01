# =============================================
# test_api.py - Verification Test Script
# =============================================
# This script tests all key backend features:
#   1. Admin Login (JWT generation)
#   2. Listing Jobs (public dropdown)
#   3. Creating a Job (Admin only)
#   4. Submitting a Candidate Application (with resume file)
#   5. Filtering Applications (by job, by stage, by search)
#   6. Updating Candidate Stage (Applied -> R1 -> Approved)
# =============================================

import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("--------------------------------------------------")
    print("[TEST] RUNNING BACKEND INTEGRATION TESTS")
    print("--------------------------------------------------")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200
    print("[PASS] 1. Health check passed:", res.json())

    # 2. Admin Login
    login_res = client.post(
        "/api/auth/login",
        json={"email": "admin@enter.in", "password": "admin123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[PASS] 2. Admin login successful. JWT token received.")

    # 3. Check /api/auth/me
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    print("[PASS] 3. Admin profile verified:", me_res.json())

    # 4. Get Jobs
    jobs_res = client.get("/api/jobs")
    assert jobs_res.status_code == 200
    jobs = jobs_res.json()
    assert len(jobs) >= 10
    print(f"[PASS] 4. Retrieved {len(jobs)} jobs from database.")

    # 5. Create a new Job (Admin)
    new_job_data = {
        "title": "Cloud Architect",
        "department": "Infrastructure",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Design high scalability cloud architectures.",
        "requirements": "AWS / GCP certifications, Kubernetes mastery.",
        "status": "Active"
    }
    create_job_res = client.post("/api/jobs", json=new_job_data, headers=headers)
    assert create_job_res.status_code == 201
    created_job = create_job_res.json()
    print(f"[PASS] 5. Created new job: ID {created_job['id']} - {created_job['title']}")

    # 6. Candidate Submit Application (with simulated resume PDF file)
    sample_pdf_bytes = io.BytesIO(b"%PDF-1.4 sample resume content for testing")
    app_data = {
        "job_id": str(created_job["id"]),
        "full_name": "Kavya Nair",
        "email": "kavya.nair@example.com",
        "phone": "+91 99887 76655",
        "brief_note": "Cloud engineer with 5 years AWS experience."
    }
    files = {
        "resume": ("kavya_resume.pdf", sample_pdf_bytes, "application/pdf")
    }
    submit_res = client.post("/api/applications", data=app_data, files=files)
    assert submit_res.status_code == 201
    created_app = submit_res.json()
    print(f"[PASS] 6. Candidate application submitted: ID {created_app['id']} for '{created_app['job_title']}'")

    # 7. List Applications with Filter
    filter_res = client.get(
        f"/api/applications?job_id={created_job['id']}&stage=Applied",
        headers=headers
    )
    assert filter_res.status_code == 200
    filtered_apps = filter_res.json()
    assert len(filtered_apps) >= 1
    print(f"[PASS] 7. Filtered applications by job & stage: {len(filtered_apps)} found.")

    # 8. Update Stage (Applied -> R1 -> Approved)
    stage_res = client.patch(
        f"/api/applications/{created_app['id']}/stage",
        json={"stage": "R1"},
        headers=headers
    )
    assert stage_res.status_code == 200
    assert stage_res.json()["stage"] == "R1"
    print(f"[PASS] 8. Candidate moved to R1 successfully.")

    stage_res2 = client.patch(
        f"/api/applications/{created_app['id']}/stage",
        json={"stage": "Approved"},
        headers=headers
    )
    assert stage_res2.status_code == 200
    assert stage_res2.json()["stage"] == "Approved"
    print(f"[PASS] 9. Candidate moved to Approved successfully.")

    # 10. Dashboard stats
    stats_res = client.get("/api/applications/stats", headers=headers)
    assert stats_res.status_code == 200
    print("[PASS] 10. Dashboard stats verified:", stats_res.json())

    print("\n[SUCCESS] ALL BACKEND TESTS PASSED SUCCESSFULLY!\n")


if __name__ == "__main__":
    run_tests()
