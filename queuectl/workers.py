import subprocess
import time
from queuectl.storage import load_jobs, save_jobs


def run_worker():
    """Worker that processes jobs"""
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
        
        print(f"Processing: {job_id}")
        print(f"Running: {command}")
        
        # Track retries
        if "attempts" not in pending_job:
            pending_job["attempts"] = 0
        
        max_retries = 3
        attempts = pending_job["attempts"]
        
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
                    print(f"⚠️ {job_id} failed, retrying ({attempts + 1}/{max_retries})")
                else:
                    pending_job["state"] = "failed"
                    print(f"✗ {job_id} failed permanently (max retries)")
        
        except subprocess.TimeoutExpired:
            pending_job["state"] = "failed"
            print(f"✗ {job_id} timeout")
        
        except Exception as e:
            pending_job["state"] = "failed"
            print(f"✗ {job_id} error: {e}")
        
        # Update jobs file
        for i, job in enumerate(jobs):
            if job["id"] == job_id:
                jobs[i] = pending_job
                break
        
        save_jobs(jobs)


if __name__ == "__main__":
    run_worker()
