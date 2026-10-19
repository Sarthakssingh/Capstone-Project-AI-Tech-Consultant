import subprocess
import time
import sys
import os

def run_service(name, command, cwd):
    print(f"Starting {name}...")
    return subprocess.Popen(command, shell=True, cwd=cwd)

if __name__ == "__main__":
    services = [
        ("Task 1: Knowledge Brain", "python -m Task1_Knowledge_Brain.main", "."),
        ("Task 2: Inbox Agent", "npm start", "./Task2_Inbox_Agent"),
        ("Task 3: Meeting SOW", "python Task3_Meeting_to_SOW/main.py", ".")
    ]

    processes = []
    try:
        for name, cmd, cwd in services:
            p = run_service(name, cmd, cwd)
            processes.append(p)
            time.sleep(2) # Give it some time to start

        print("\nAll services started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        for p in processes:
            p.terminate()
        sys.exit(0)
