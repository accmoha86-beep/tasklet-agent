"""Todo App Configuration"""

import os
from pathlib import Path

# Storage
STORAGE_DIR = os.getenv("TODO_STORAGE_DIR", "./data/todos")
STORAGE_FILE = "todos.json"
BACKUP_DIR = os.path.join(STORAGE_DIR, "backups")

# Web UI
WEB_HOST = os.getenv("TODO_WEB_HOST", "localhost")
WEB_PORT = int(os.getenv("TODO_WEB_PORT", "5000"))
WEB_DEBUG = os.getenv("TODO_WEB_DEBUG", "True").lower() == "true"

# Features
AUTO_BACKUP = os.getenv("TODO_AUTO_BACKUP", "true").lower() == "true"
BACKUP_INTERVAL = int(os.getenv("TODO_BACKUP_INTERVAL", "3600"))  # 1 hour

# Logging
LOG_LEVEL = os.getenv("TODO_LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("TODO_LOG_FILE", "todo_app.log")

# Create directories
Path(STORAGE_DIR).mkdir(parents=True, exist_ok=True)
Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
