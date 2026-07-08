# Integration Guide - Tasklet Agent Advanced Features

## Overview

This guide covers the integration of advanced features added to the tasklet-agent repository:
- Web UI (Flask backend + interactive frontend)
- CLI Tests
- Due Date Reminders System
- Recurring Tasks System
- Task Dependencies System

## Branch Structure

```
main (master branch)
├── feature/web-ui (Web UI implementation)
│   └── web_ui/
│       ├── app.py              # Flask server
│       ├── requirements.txt    # Flask dependencies
│       ├── templates/index.html
│       └── static/
│           ├── style.css
│           └── script.js
│
└── feature/advanced-features (Advanced features - based on feature/web-ui)
    ├── todo_app/
    │   ├── app/
    │   │   ├── models.py           # Data models with advanced fields
    │   │   ├── reminders.py        # Reminder system
    │   │   ├── recurring.py        # Recurring tasks system
    │   │   └── dependencies.py     # Task dependencies system
    │   │
    │   └── tests/
    │       ├── test_cli.py         # CLI command tests (20+ cases)
    │       ├── test_reminders.py   # Reminder system tests
    │       ├── test_recurring.py   # Recurring tasks tests
    │       └── test_dependencies.py # Dependencies tests
```

## Feature Details

### 1. Web UI (feature/web-ui)

**Files Added:**
- `web_ui/app.py` - Flask application with REST API
- `web_ui/templates/index.html` - Interactive HTML interface
- `web_ui/static/style.css` - Modern responsive styling
- `web_ui/static/script.js` - Frontend logic and API calls
- `web_ui/requirements.txt` - Dependencies (Flask, Flask-CORS)
- `web_ui/README.md` - Complete Web UI documentation

**API Endpoints:**
- `POST /api/execute` - Execute agent task
- `GET /api/history` - Get execution history
- `GET /api/memory` - Get agent memory
- `POST /api/clear-memory` - Clear memory
- `GET /api/status` - Get agent status

**Features:**
- Real-time task execution feedback
- Execution history tracking
- Agent memory inspection
- Responsive mobile-friendly design
- Keyboard shortcuts (Ctrl+Enter)

**To Run:**
```bash
cd web_ui
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

### 2. CLI Tests (feature/advanced-features)

**File:** `todo_app/tests/test_cli.py`

**Test Coverage (20+ tests):**
- Help and initialization commands
- Task creation with options
- Task listing and filtering
- Task completion and deletion
- Search functionality
- Statistics and reporting
- Export/Import CSV operations
- Backup and restore functionality
- Error handling and edge cases
- Full workflow integration tests

**Run Tests:**
```bash
pytest todo_app/tests/test_cli.py -v
pytest todo_app/tests/test_cli.py --cov=todo_app
```

### 3. Due Date Reminders System (feature/advanced-features)

**File:** `todo_app/app/reminders.py`

**Components:**
- `ReminderType` enum: at_time, before_due, overdue, daily_check
- `Reminder` model: Stores reminder details
- `ReminderManager` class: Manages reminder lifecycle

**Key Methods:**
```python
# Create reminder
reminder = manager.create_reminder(task, ReminderType.BEFORE_DUE)

# Get pending reminders
pending = manager.get_pending_reminders()

# Mark as sent
manager.mark_reminder_sent(reminder_id)

# Get overdue tasks
overdue = manager.get_overdue_tasks_reminders(tasks)

# Get upcoming reminders
upcoming = manager.get_upcoming_reminders(hours=24)
```

**Features:**
- Automatic reminder scheduling
- Multiple reminder types
- Persistent storage in `reminders.json`
- Overdue task detection
- Upcoming reminder querying

**Tests:** `test_reminders.py` (10 tests)

### 4. Recurring Tasks System (feature/advanced-features)

**File:** `todo_app/app/recurring.py`

**Components:**
- `RecurrencePattern` enum: none, daily, weekly, biweekly, monthly, quarterly, yearly
- `RecurrenceConfig` model: Configure recurrence behavior
- `RecurringTaskManager` class: Handle recurring task logic

**Key Methods:**
```python
# Create recurring task
task.recurrence = RecurrenceConfig(pattern=RecurrencePattern.DAILY)

# Generate next occurrence
next_task = manager.generate_next_occurrence(task)

# Get future occurrences
futures = manager.get_next_occurrences(task, count=5)

# Auto-complete and reschedule
next_occurrence = manager.auto_complete_and_reschedule(task)
```

**Features:**
- 7 recurrence patterns
- Configurable intervals
- Max occurrences limit
- End date constraint
- Skip weekends option
- Custom weekdays for weekly tasks
- Parent-child tracking

**Configuration:**
```python
RecurrenceConfig(
    pattern=RecurrencePattern.WEEKLY,
    interval=2,              # Every 2 weeks
    custom_days=[0, 2, 4],   # Mon, Wed, Fri
    skip_weekends=True,
    max_occurrences=52,
    end_date=datetime(2025, 12, 31)
)
```

**Tests:** `test_recurring.py` (12 tests)

### 5. Task Dependencies System (feature/advanced-features)

**File:** `todo_app/app/dependencies.py`

**Components:**
- `DependencyManager` class: Manage task dependencies
- Circular dependency detection
- Critical path analysis

**Key Methods:**
```python
# Add dependency
manager.add_dependency('task2', 'task1')  # task2 depends on task1

# Check if task can start
can_start = manager.can_start_task('task2', tasks_by_id)

# Get dependency chains
deps = manager.get_task_chain('task')      # All dependencies
dependents = manager.get_dependent_chain('task')  # All dependents

# Get critical path
path = manager.get_critical_path(tasks_by_id)

# Get task status
ready = manager.get_ready_tasks(tasks_by_id)     # Can start
blocked = manager.get_blocked_tasks(tasks_by_id) # Cannot start
```

**Features:**
- Dependency linking and removal
- Circular dependency prevention
- Chain traversal (BFS)
- Critical path analysis (DFS)
- Ready task identification
- Blocked task detection
- Full dependency graph generation

**Example Usage:**
```python
# Create dependency chain
manager.add_dependency('design', 'requirements')
manager.add_dependency('implementation', 'design')
manager.add_dependency('testing', 'implementation')
manager.add_dependency('deployment', 'testing')

# Get critical path
path = manager.get_critical_path(tasks)
# Output: ['requirements', 'design', 'implementation', 'testing', 'deployment']
```

**Tests:** `test_dependencies.py` (15 tests)

## Data Models Update

**File:** `todo_app/app/models.py`

Enhancements to `Task` model:
```python
@dataclass
class Task:
    # ... existing fields ...
    
    # Recurrence
    recurrence: RecurrenceConfig = field(default_factory=RecurrenceConfig)
    is_recurring_instance: bool = False
    parent_task_id: Optional[str] = None
    occurrence_number: int = 0
    
    # Dependencies
    depends_on: List[str] = field(default_factory=list)
    blocking_tasks: List[str] = field(default_factory=list)
    
    # Reminders
    reminders: List[Reminder] = field(default_factory=list)
    has_active_reminder: bool = False
    
    # Additional fields
    tags: List[str] = field(default_factory=list)
    is_archived: bool = False
    
    # Helper methods
    def is_overdue(self) -> bool
    def is_due_soon(self, hours: int = 1) -> bool
    def can_start(self, tasks_by_id: dict) -> bool
    def get_blocking_status(self, tasks_by_id: dict) -> dict
```

## Test Summary

**Total Tests: 57+**

| Feature | Tests | Coverage |
|---------|-------|----------|
| CLI Commands | 20+ | Commands, options, error handling |
| Reminders | 10 | Create, get, mark sent, persistence |
| Recurring | 12 | Patterns, dates, limits, rescheduling |
| Dependencies | 15 | Add, remove, chains, cycles, paths |

**Run All Tests:**
```bash
# Individual test files
pytest todo_app/tests/test_cli.py -v
pytest todo_app/tests/test_reminders.py -v
pytest todo_app/tests/test_recurring.py -v
pytest todo_app/tests/test_dependencies.py -v

# All tests
pytest todo_app/tests/ -v

# With coverage
pytest todo_app/tests/ --cov=todo_app --cov-report=html
```

## Integration Steps

### Step 1: Merge Web UI
```bash
git checkout main
git merge feature/web-ui
```

### Step 2: Merge Advanced Features
```bash
git merge feature/advanced-features
```

### Step 3: Update Main Requirements
```bash
# Combine all requirements
cat web_ui/requirements.txt >> requirements-full.txt
cat todo_app/requirements.txt >> requirements-full.txt
```

### Step 4: Run All Tests
```bash
pytest tests/ todo_app/tests/ -v --cov
```

### Step 5: Update README.md
Add sections for:
- Web UI usage
- Reminder system
- Recurring tasks
- Task dependencies

## Usage Examples

### Complete Workflow

```python
from todo_app.app.core import TodoManager
from todo_app.app.models import RecurrencePattern, RecurrenceConfig, TaskStatus
from todo_app.app.reminders import ReminderManager, ReminderType
from todo_app.app.recurring import RecurringTaskManager
from todo_app.app.dependencies import DependencyManager
from datetime import datetime, timedelta

# Initialize managers
todo_manager = TodoManager()
reminder_mgr = ReminderManager()
recurring_mgr = RecurringTaskManager()
dep_mgr = DependencyManager()

# Create tasks
req_task = todo_manager.add_task("Gather requirements", due_date=datetime.now() + timedelta(days=1))
design_task = todo_manager.add_task("Create design", due_date=datetime.now() + timedelta(days=3))
dev_task = todo_manager.add_task("Development", due_date=datetime.now() + timedelta(days=7))

# Set up dependencies
dep_mgr.add_dependency('design', 'requirements')
dep_mgr.add_dependency('dev', 'design')

# Create recurring standup
standup = todo_manager.add_task("Daily standup", due_date=datetime.now() + timedelta(days=1))
standup.recurrence = RecurrenceConfig(
    pattern=RecurrencePattern.DAILY,
    skip_weekends=True
)

# Set up reminders
reminder_mgr.create_reminder(req_task, ReminderType.BEFORE_DUE)
reminder_mgr.create_reminder(design_task, ReminderType.BEFORE_DUE)

# Check ready tasks
ready = dep_mgr.get_ready_tasks({t.id: t for t in [req_task, design_task, dev_task]})
# Output: ['requirements']

# Get critical path
path = dep_mgr.get_critical_path({t.id: t for t in [req_task, design_task, dev_task]})
# Output: ['requirements', 'design', 'dev']

# Complete first task and reschedule
next_standup = recurring_mgr.auto_complete_and_reschedule(standup)

# Check for upcoming reminders
upcoming = reminder_mgr.get_upcoming_reminders(hours=24)
```

## CLI Examples

```bash
# Add recurring task
python todo_app/main.py add "Daily standup" --category "standup" --priority "high" --recurring daily

# List all tasks
python todo_app/main.py list

# Mark complete (auto-reschedules if recurring)
python todo_app/main.py complete 1

# Add task with dependency
python todo_app/main.py add "Design" --depends-on 1

# Show statistics
python todo_app/main.py stats

# Export for backup
python todo_app/main.py export tasks_backup.csv
```

## Performance Considerations

1. **Reminders**: O(N) to find pending, O(1) to mark sent
2. **Recurring**: O(1) to generate next occurrence
3. **Dependencies**: O(N+E) for BFS/DFS operations
4. **Storage**: JSON serialization/deserialization

## Future Enhancements

- [ ] Database backend instead of JSON
- [ ] WebSocket support for real-time updates
- [ ] Advanced filtering and sorting
- [ ] Task templates and cloning
- [ ] Multi-user support
- [ ] Notifications integration (email, SMS, Slack)
- [ ] Calendar view integration
- [ ] Mobile app

## Troubleshooting

### Tests Failing
```bash
# Check Python version
python --version  # Should be 3.8+

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run with verbose output
pytest todo_app/tests/ -vv --tb=short
```

### Circular Dependency Error
```python
# This will fail
dep_mgr.add_dependency('task1', 'task2')
dep_mgr.add_dependency('task2', 'task3')
dep_mgr.add_dependency('task3', 'task1')  # Error!
```

### Reminder Not Triggering
```python
# Ensure task has due date
task.due_date = datetime.now() + timedelta(hours=1)

# Create reminder
reminder = reminder_mgr.create_reminder(task, ReminderType.BEFORE_DUE)

# Check pending
pending = reminder_mgr.get_pending_reminders()
```

## Contributing

When adding features:
1. Create feature branch from `feature/advanced-features`
2. Add tests in `todo_app/tests/`
3. Update documentation
4. Ensure all tests pass
5. Create pull request

## License

MIT License - See LICENSE file in root directory
