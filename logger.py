import datetime
from pathlib import Path

log_file = Path("signals.log")

def log_signal(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

def get_logs():
    if not log_file.exists():
        return []
    with open(log_file, "r") as f:
        return f.readlines()[-30:]
