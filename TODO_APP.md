# Todo App - Local Storage Task Manager

A modern, full-featured todo list application with local storage, built with the Tasklet Agent infrastructure.

## Features

✅ **Create Tasks** - Add new tasks with descriptions
✅ **Edit Tasks** - Modify task details
✅ **Delete Tasks** - Remove tasks
✅ **Mark Complete** - Toggle task completion status
✅ **Local Storage** - Persist data between sessions
✅ **Categories** - Organize tasks by category
✅ **Priorities** - Set task priority levels
✅ **Due Dates** - Add deadlines to tasks
✅ **Search & Filter** - Find tasks quickly
✅ **Export/Import** - Backup and restore data
✅ **Statistics** - Track productivity
✅ **CLI & Web UI** - Use via command line or web interface

## Project Structure

```
todo-app/
├── app/
│   ├── __init__.py
│   ├── core.py                 # Main todo logic
│   ├── storage.py              # Local storage handler
│   ├── models.py               # Data models
│   └── utils.py                # Utilities
├── cli/
│   ├── __init__.py
│   ├── commands.py             # CLI commands
│   └── main.py                 # CLI entry point
├── web/
│   ├── __init__.py
│   ├── app.py                  # Flask/FastAPI app
│   ├── routes.py               # API routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       └── index.html
├── tests/
│   ├── test_core.py
│   ├── test_storage.py
│   └── test_cli.py
├── data/                       # Local storage directory
│   └── todos.json
├── requirements.txt
├── config.py                   # Configuration
├── main.py                     # Main entry point
└── README.md
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize data directory
python main.py init
```

## Usage

### CLI Usage

```bash
# Add a task
python main.py add "Buy groceries" --category shopping --priority high

# List all tasks
python main.py list

# List completed tasks
python main.py list --status completed

# Mark task complete
python main.py complete 1

# Delete task
python main.py delete 1

# Search tasks
python main.py search "grocery"

# Show statistics
python main.py stats

# Export data
python main.py export todos.csv

# Import data
python main.py import todos.csv
```

### Web UI Usage

```bash
# Start web server
python main.py web

# Open http://localhost:5000 in browser
```

### Python API

```python
from app.core import TodoManager

# Initialize
todo_manager = TodoManager()

# Add task
todo_manager.add_task("Learn Python", category="learning", priority="high")

# Get all tasks
tasks = todo_manager.get_all_tasks()

# Mark complete
todo_manager.mark_complete(1)

# Delete
todo_manager.delete_task(1)

# Search
results = todo_manager.search("Python")

# Get statistics
stats = todo_manager.get_statistics()
```

## Data Storage

Tasks are stored locally in `data/todos.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "category": "shopping",
      "priority": "high",
      "status": "pending",
      "created_at": "2024-01-15T10:30:00",
      "due_date": "2024-01-16",
      "completed_at": null
    }
  ]
}
```

## API Endpoints

```
GET    /api/todos              - Get all tasks
POST   /api/todos              - Create task
GET    /api/todos/<id>         - Get specific task
PUT    /api/todos/<id>         - Update task
DELETE /api/todos/<id>         - Delete task
PATCH  /api/todos/<id>/complete - Mark complete
GET    /api/stats              - Get statistics
GET    /api/search?q=<query>   - Search tasks
```

## Configuration

Edit `config.py` to customize:

```python
# Storage
STORAGE_DIR = "./data"
STORAGE_FILE = "todos.json"

# Web UI
WEB_HOST = "localhost"
WEB_PORT = 5000
WEB_DEBUG = True

# Auto-backup
AUTO_BACKUP = True
BACKUP_DIR = "./backups"
```

## Development

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Format code
black .

# Lint
pylint app/ cli/ web/
```

---

**Version:** 1.0.0  
**Status:** ✅ Production Ready
