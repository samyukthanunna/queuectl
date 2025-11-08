# 🛠️ Backend Job Queue System

A robust asynchronous job queue system implemented in Python, designed to support command-line job enqueueing, background workers, retry with exponential backoff, dead letter queue handling, and persistent JSON storage.

***

## ✨ Key Features

- ✅ **Asynchronous job processing:** Worker threads process jobs independently from CLI commands.  
- ✅ **Command-line interface:** Clean CLI commands for enqueue, list, and detailed job info.  
- ✅ **Retry with exponential backoff:** Intelligent retry intervals increasing exponentially to prevent overload.  
- ✅ **Dead letter queue:** Isolates repeatedly failing jobs for manual review.  
- ✅ **Persistent storage:** Jobs and queue state are saved in JSON files for durability.  
- ✅ **Modular, extensible code base:** Separation of CLI, worker, and storage logic for maintainability.  
- ✅ **Cross-platform:** Works seamlessly on any system with Python 3.  

***

## 🎯 Objective

Create a reliable backend job queue system that can enqueue, process, retry, and safely handle failures through a user-accessible command line interface and background processing.

***

## 📋 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Git (for cloning)

### Steps

```bash
git clone https://github.com/samyukthanunna/queuectl.git
cd queuectl_project    # or wherever you prefer
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt   # if you have dependencies, else skip
```

***

## 🚀 Usage

### Start Background Worker

```bash
python -m queuectl.workers
```

Runs worker process that polls the job queue and executes jobs asynchronously.

### Add Jobs to Queue (Enqueue CLI)

```bash
python -m queuectl.cli enqueue job1 "echo Hello World"
python -m queuectl.cli enqueue job2 "sleep 3 && echo Done"
python -m queuectl.cli enqueue job3 "invalidcommand"
```

Example commands — first two succeed, last simulates failure to demonstrate retries.

### List Jobs

```bash
python -m queuectl.cli list
```

Shows jobs with status: pending, running, completed, failed, retry count, and timestamps.

### Show Detailed Job Info

```bash
python -m queuectl.cli info job3
```

Shows retry attempts, error logs, and status for a specific job.

***

## 🎥 Demo Video

Watch a walkthrough of the backend job queue system in action:

[Demo Video on Google Drive](https://drive.google.com/file/d/1FK2N0RUgDlwU2_jGSJ2Ucs1RCpIZhVv_/view?usp=drivesdk)

The video demonstrates job enqueueing, worker execution, retry logic, and dead letter queue behavior.

***

## 📁 Project Structure

```
queuectl_project/
│
├── queuectl/
│   ├── cli.py            # Command line interface for queue operations
│   ├── workers.py        # Worker thread for job processing
│   ├── storage.py        # Persistent JSON storage & retry logic
│
├── config.json           # Configuration parameters
├── README.md             # Project documentation (this file)
└── requirements.txt      # Python dependencies (if any)
```

***

## 🤝 Contribution & License

Open-source MIT licensed project. Contributions and feedback welcome.

***

## 👤 Author

**Samyuktha Nunna**  
- Backend Developer at QAI Technologies  
- GitHub: [samyukthanunna](https://github.com/samyukthanunna)  
- LinkedIn: [linkedin.com/in/samyukthanunna](https://linkedin.com/in/samyukthanunna)  

***

_Built with ❤️ for Flam Internship Program_  
_Last Updated: November 2025_  
_Status: Production Ready_
