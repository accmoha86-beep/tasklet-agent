"""Data Models for Todo App"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from uuid import uuid4


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecurrencePattern(str, Enum):
    """Recurrence pattern enumeration"""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class ReminderType(str, Enum):
    """Reminder type enumeration"""
    AT_TIME = "at_time"
    BEFORE_DUE = "before_due"  # 1 hour before
    OVERDUE = "overdue"
    DAILY_CHECK = "daily_check"


@dataclass
class Reminder:
    """Reminder for a task"""
    id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    reminder_type: ReminderType = ReminderType.BEFORE_DUE
    scheduled_time: datetime = field(default_factory=datetime.now)
    is_sent: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'reminder_type': self.reminder_type.value,
            'scheduled_time': self.scheduled_time.isoformat(),
            'is_sent': self.is_sent,
            'created_at': self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Reminder':
        """Create from dictionary"""
        return cls(
            id=data.get('id', str(uuid4())),
            task_id=data.get('task_id', ''),
            reminder_type=ReminderType(data.get('reminder_type', 'before_due')),
            scheduled_time=datetime.fromisoformat(data.get('scheduled_time', datetime.now().isoformat())),
            is_sent=data.get('is_sent', False),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
        )


@dataclass
class RecurrenceConfig:
    """Configuration for recurring tasks"""
    pattern: RecurrencePattern = RecurrencePattern.NONE
    interval: int = 1  # Every N days/weeks/months
    end_date: Optional[datetime] = None
    max_occurrences: Optional[int] = None
    skip_weekends: bool = False
    custom_days: List[int] = field(default_factory=list)  # For weekly (0-6)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'pattern': self.pattern.value,
            'interval': self.interval,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'max_occurrences': self.max_occurrences,
            'skip_weekends': self.skip_weekends,
            'custom_days': self.custom_days,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecurrenceConfig':
        """Create from dictionary"""
        return cls(
            pattern=RecurrencePattern(data.get('pattern', 'none')),
            interval=data.get('interval', 1),
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            max_occurrences=data.get('max_occurrences'),
            skip_weekends=data.get('skip_weekends', False),
            custom_days=data.get('custom_days', []),
        )


@dataclass
class Task:
    """Task data model"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    category: str = "general"
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Recurrence
    recurrence: RecurrenceConfig = field(default_factory=RecurrenceConfig)
    is_recurring_instance: bool = False
    parent_task_id: Optional[str] = None
    occurrence_number: int = 0

    # Dependencies
    depends_on: List[str] = field(default_factory=list)  # List of task IDs
    blocking_tasks: List[str] = field(default_factory=list)  # Tasks blocked by this one

    # Reminders
    reminders: List[Reminder] = field(default_factory=list)
    has_active_reminder: bool = False

    # Tags
    tags: List[str] = field(default_factory=list)
    is_archived: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'recurrence': self.recurrence.to_dict(),
            'is_recurring_instance': self.is_recurring_instance,
            'parent_task_id': self.parent_task_id,
            'occurrence_number': self.occurrence_number,
            'depends_on': self.depends_on,
            'blocking_tasks': self.blocking_tasks,
            'reminders': [r.to_dict() for r in self.reminders],
            'has_active_reminder': self.has_active_reminder,
            'tags': self.tags,
            'is_archived': self.is_archived,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create from dictionary"""
        reminders = [Reminder.from_dict(r) for r in data.get('reminders', [])]
        recurrence_data = data.get('recurrence', {})
        recurrence = RecurrenceConfig.from_dict(recurrence_data) if recurrence_data else RecurrenceConfig()

        return cls(
            id=data.get('id', str(uuid4())),
            title=data.get('title', ''),
            description=data.get('description', ''),
            category=data.get('category', 'general'),
            priority=TaskPriority(data.get('priority', 'medium')),
            status=TaskStatus(data.get('status', 'pending')),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat())),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            recurrence=recurrence,
            is_recurring_instance=data.get('is_recurring_instance', False),
            parent_task_id=data.get('parent_task_id'),
            occurrence_number=data.get('occurrence_number', 0),
            depends_on=data.get('depends_on', []),
            blocking_tasks=data.get('blocking_tasks', []),
            reminders=reminders,
            has_active_reminder=data.get('has_active_reminder', False),
            tags=data.get('tags', []),
            is_archived=data.get('is_archived', False),
        )

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.status == TaskStatus.COMPLETED:
            return False
        return datetime.now() > self.due_date

    def is_due_soon(self, hours: int = 1) -> bool:
        """Check if task is due soon"""
        if not self.due_date or self.status == TaskStatus.COMPLETED:
            return False
        time_until_due = self.due_date - datetime.now()
        return timedelta(0) < time_until_due <= timedelta(hours=hours)

    def can_start(self, tasks_by_id: dict) -> bool:
        """Check if all dependencies are met"""
        for dep_id in self.depends_on:
            dep_task = tasks_by_id.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    def get_blocking_status(self, tasks_by_id: dict) -> dict:
        """Get blocking information"""
        blocked_count = 0
        blocking_details = []

        for task_id in self.blocking_tasks:
            blocked_task = tasks_by_id.get(task_id)
            if blocked_task:
                blocked_count += 1
                blocking_details.append({
                    'id': task_id,
                    'title': blocked_task.title,
                    'status': blocked_task.status.value,
                })

        return {
            'is_blocking': blocked_count > 0,
            'blocked_count': blocked_count,
            'blocked_tasks': blocking_details,
        }
