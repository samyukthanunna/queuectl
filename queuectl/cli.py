import sys
import json
from datetime import datetime
from queuectl.storage import add_job, get_jobs, get_job_stats, get_dlq_jobs, retry_dlq_job

CONFIG = {
    "max_retries": 3,
    "backoff_base": 2
}

def load_config():
    """Load config from file"""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return CONFIG

def save_config(config):
    """Save config to file"""
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

def enqueue_command(args):
    """enqueue <id> <command>"""
    if len(args) < 2:
        print("❌ Usage: queuectl enqueue <id> '<command>'")
        return
    
    job_id = args[0]
    command = args[1]
    config = load_config()
    
    job = add_job(job_id, command)
    job["max_retries"] = config["max_retries"]
    
    print(f"✅ Job enqueued: {job_id}")
    print(f"   Command: {command}")

def list_command(args):
    """list [--state pending|completed|dead]"""
    jobs = get_jobs()
    state_filter = None
    
    if "--state" in args:
        idx = args.index("--state")
        if idx + 1 < len(args):
            state_filter = args[idx + 1]
    
    if state_filter:
        jobs = [j for j in jobs if j.get("state") == state_filter]
    
    if not jobs:
        print("📋 No jobs")
        return
    
    print("📋 Jobs:")
    print("─" * 70)
    for job in jobs:
        print(f"  {job['id']:15} | {job['state']:10} | Attempts: {job.get('attempts', 0)}")
    print("─" * 70)

def status_command(args):
    """status"""
    stats = get_job_stats()
    config = load_config()
    
    print("📊 Queue Status:")
    print("─" * 40)
    print(f"  Pending:     {stats['pending']}")
    print(f"  Running:     0")
    print(f"  Completed:   {stats['completed']}")
    print(f"  Failed:      {stats['failed']}")
    print(f"  Dead (DLQ):  {len(get_dlq_jobs())}")
    print("─" * 40)
    print(f"  Max Retries: {config['max_retries']}")
    print(f"  Backoff Base: {config['backoff_base']}")

def dlq_command(args):
    """dlq list | dlq retry <id>"""
    if not args:
        print("❌ Usage: queuectl dlq list | queuectl dlq retry <id>")
        return
    
    action = args[0]
    
    if action == "list":
        dlq_jobs = get_dlq_jobs()
        if not dlq_jobs:
            print("☠️ DLQ is empty")
            return
        
        print("☠️ Dead Letter Queue:")
        print("─" * 70)
        for job in dlq_jobs:
            print(f"  {job['id']:15} | Command: {job['command'][:40]}")
        print("─" * 70)
    
    elif action == "retry":
        if len(args) < 2:
            print("❌ Usage: queuectl dlq retry <job_id>")
            return
        
        job_id = args[1]
        retry_dlq_job(job_id)
        print(f"🔄 Job {job_id} moved back to pending")
    
    else:
        print("❌ Unknown action. Use: list or retry")

def config_command(args):
    """config set <key> <value> | config get <key>"""
    if not args:
        print("❌ Usage: queuectl config set|get <key> [value]")
        return
    
    action = args[0]
    config = load_config()
    
    if action == "set":
        if len(args) < 3:
            print("❌ Usage: queuectl config set <key> <value>")
            return
        
        key = args[1]
        value = args[2]
        
        try:
            config[key] = int(value)
            save_config(config)
            print(f"✅ Config updated: {key} = {value}")
        except:
            print("❌ Value must be a number")
    
    elif action == "get":
        if len(args) < 2:
            print("❌ Usage: queuectl config get <key>")
            return
        
        key = args[1]
        value = config.get(key, "Not found")
        print(f"⚙️ {key} = {value}")
    
    else:
        print("❌ Unknown action. Use: set or get")

def help_command(args):
    """help"""
    print("""
🚀 QueueCTL - Job Queue System

Commands:
  enqueue <id> '<cmd>'     Enqueue a new job
  list [--state STATE]     List jobs (pending|completed|dead)
  status                   Show queue status
  dlq list                 View dead letter queue
  dlq retry <id>          Retry a dead job
  config set <key> <val>  Set configuration
  config get <key>        Get configuration
  help                    Show this help

Examples:
  queuectl enqueue job1 "echo hello"
  queuectl list --state pending
  queuectl status
  queuectl dlq list
  queuectl dlq retry job1
  queuectl config set max-retries 5

Start worker:
  python -m queuectl.workers
    """)

def main():
    if len(sys.argv) < 2:
        help_command([])
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "enqueue":
        enqueue_command(args)
    elif command == "list":
        list_command(args)
    elif command == "status":
        status_command(args)
    elif command == "dlq":
        dlq_command(args)
    elif command == "config":
        config_command(args)
    elif command == "help" or command == "--help":
        help_command(args)
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'queuectl help' for available commands")

if __name__ == "__main__":
    main()
