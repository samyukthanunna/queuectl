# QueueCTL - Job Queue

A program that runs jobs one by one.

## How to use

1. Start worker:
   python -m queuectl.workers

2. Add a job:
   python -m queuectl.cli enqueue job1 "echo hello"

3. See status:
   python -m queuectl.cli status

4. List jobs:
   python -m queuectl.cli list

## What it does

- You add jobs
- Worker runs them
- Shows if they worked or failed

## Files

- cli.py - Takes commands
- storage.py - Saves jobs
- workers.py - Runs jobs
