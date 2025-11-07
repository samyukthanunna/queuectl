import sys
from queuectl.storage import add_job, get_jobs, get_job_stats

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m queuectl.cli <command>")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        stats = get_job_stats()
        print("Status:")
        print(f"  Pending: {stats['pending']}")
        print(f"  Completed: {stats['completed']}")
        print(f"  Failed: {stats['failed']}")
    
    elif command == "enqueue":
        if len(sys.argv) < 4:
            print("Usage: python -m queuectl.cli enqueue <id> <command>")
            return
        job_id = sys.argv[2]
        job_cmd = sys.argv[3]
        job = add_job(job_id, job_cmd)
        print(f"✓ Job added: {job_id}")
    
    elif command == "list":
        jobs = get_jobs()
        if not jobs:
            print("No jobs yet")
            return
        print("Jobs:")
        for job in jobs:
            print(f"  {job['id']}: {job['state']} - {job['command']}")
    
    elif command == "--help":
        print("Commands:")
        print("  status              - Show job stats")
        print("  enqueue <id> <cmd>  - Add job")
        print("  list                - List all jobs")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
