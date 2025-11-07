import subprocess
import time
from queuectl.storage import load_jobs, save_jobs


def calculate_backoff(attempts, base=2):
    """Calculate exponential backoff: base^attempts"""
    return base ** attempts


def run_worker():
    """Worker that processes jobs with exponential backoff"""
    print("Worker started...")
    
    while True:
        jobs = load_jobs()
        
        # Find pending job
        pending_job = None
        for job in jobs:
            if job["state"] == "pending":
                pending_job = job
                break
        
        if not pending_job:
            print("No jobs, waiting...")
            time.sleep(2)
            continue
        
        # Process the job
        job_id = pending_job["id"]
        command = pending_job["command"]
        
        # Check if we need to wait for backoff
        attempts = pending_job.get("attempts", 0)
        max_retries = pending_job.get("max_retries", 3)
        
        if attempts > 0:
            backoff_time = calculate_backoff(attempts - 1, base=2)
            print(f"⏳ Job {job_id}: waiting {backoff_time}s (backoff)")
            time.sleep(backoff_time)
        
        print(f"Processing: {job_id}")
        print(f"Running: {command}")
        
        try:
            # Run the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            
            # Check if successful
            if result.returncode == 0:
                pending_job["state"] = "completed"
                print(f"✓ {job_id} completed")
            else:
                # Command failed
                if attempts < max_retries:
                    pending_job["state"] = "pending"
                    pending_job["attempts"] = attempts + 1
                    backoff = calculate_backoff(attempts, base=2)
                    print(f"⚠️ {job_id} failed, retrying in {backoff}s ({attempts + 1}/{max_retries})")
                else:
                    pending_job["state"] = "dead"
                    print(f"☠️ {job_id} moved to DLQ (max retries exceeded)")
        
        except subprocess.TimeoutExpired:
            if attempts < max_retries:
                pending_job["state"] = "pending"
                pending_job["attempts"] = attempts + 1
                print(f"⚠️ {job_id} timeout, retrying ({attempts + 1}/{max_retries})")
            else:
                pending_job["state"] = "dead"
                print(f"☠️ {job_id} timeout, moved to DLQ")
        
        except Exception as e:
            if attempts < max_retries:
                pending_job["state"] = "pending"
                pending_job["attempts"] = attempts + 1
                print(f"⚠️ {job_id} error, retrying ({attempts + 1}/{max_retries})")
            else:
                pending_job["state"] = "dead"
                print(f"☠️ {job_id} error, moved to DLQ: {e}")
        
        # Update jobs file
        for i, job in enumerate(jobs):
            if job["id"] == job_id:
                jobs[i] = pending_job
                break
        
        save_jobs(jobs)


if __name__ == "__main__":
    run_worker()
