# QueueCTL - CLI Job Queue System

A production-grade background job queue system written in Python. Manage, execute, and retry jobs with exponential backoff, automatic dead-letter queue handling, and persistent storage.

## ✨ Features

- ✅ **CLI-based Job Management** - Enqueue, list, and monitor jobs
- ✅ **Worker Process** - Automatically executes pending jobs
- ✅ **Exponential Backoff** - Smart retry strategy (2^attempt seconds)
- ✅ **Dead Letter Queue (DLQ)** - Permanently failed jobs handled gracefully
- ✅ **Persistent Storage** - Jobs survive application restarts
- ✅ **Configuration Management** - Adjust retry count and backoff base
- ✅ **Beautiful CLI** - Clear, intuitive command interface
- ✅ **Job States** - pending → completed/dead with full tracking

## 📋 Requirements

- Python 3.7+
- No external database required (uses JSON storage)

## 🚀 Installation

