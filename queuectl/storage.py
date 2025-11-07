import json
import os
from datetime import datetime

DB_FILE = "jobs.json"

def load_jobs():
    """Load jobs from file"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_jobs(jobs):
    """Save jobs to file"""
    with open(DB_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

def add_job(job_id, command):
    """Add new job"""
    jobs = load_jobs()
    job = {
        "id": job_id,
        "command": command,
        "state": "pending",
        "created_at": datetime.now().isoformat()
    }
    jobs.append(job)
    save_jobs(jobs)
    return job

def get_jobs():
    """Get all jobs"""
    return load_jobs()

def get_job_stats():
    """Count jobs by state"""
    jobs = load_jobs()
    stats = {
        "pending": 0,
        "completed": 0,
        "failed": 0
    }
    for job in jobs:
        state = job.get("state", "pending")
        if state in stats:
            stats[state] += 1
    return stats

def move_to_dlq(job_id):
    """Move job to Dead Letter Queue"""
    jobs = load_jobs()
    for job in jobs:
        if job["id"] == job_id:
            job["state"] = "dead"
            break
    save_jobs(jobs)

def get_dlq_jobs():
    """Get all dead letter queue jobs"""
    jobs = load_jobs()
    return [j for j in jobs if j.get("state") == "dead"]

def retry_dlq_job(job_id):
    """Retry a job from DLQ"""
    jobs = load_jobs()
    for job in jobs:
        if job["id"] == job_id and job.get("state") == "dead":
            job["state"] = "pending"
            job["attempts"] = 0
            break
    save_jobs(jobs)

def move_to_dlq(job_id):
    """Move job to Dead Letter Queue"""
    jobs = load_jobs()
    for job in jobs:
        if job["id"] == job_id:
            job["state"] = "dead"
            break
    save_jobs(jobs)

def get_dlq_jobs():
    """Get all dead letter queue jobs"""
    jobs = load_jobs()
    return [j for j in jobs if j.get("state") == "dead"]

def retry_dlq_job(job_id):
    """Retry a job from DLQ"""
    jobs = load_jobs()
    for job in jobs:
        if job["id"] == job_id and job.get("state") == "dead":
            job["state"] = "pending"
            job["attempts"] = 0
            break
    save_jobs(jobs)
