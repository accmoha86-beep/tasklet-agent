"""Todo App - Data Models"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task status enum"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskPriority(Enum):
    """Task priority enum"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Task:
    """Task data model"""
    title: str
    category: str = "general"
    priority: str = TaskPriority.MEDIUM.value
    status: str = TaskStatus.PENDING.value
    description: str = ""
    due_date: Optional[str] = None
    id: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        """Create from dictionary"""
        return Task(**data)

    def is_completed(self) -> bool:
        """Check if completed"""
        return self.status == TaskStatus.COMPLETED.value

    def mark_complete(self) -> None:
        """Mark as completed"""
        self.status = TaskStatus.COMPLETED.value
        self.completed_at = datetime.now().isoformat()

    def mark_pending(self) -> None:
        """Mark as pending"""
        self.status = TaskStatus.PENDING.value
        self.completed_at = None


@dataclass
class TodoStats:
    """Statistics for todos"""
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    high_priority: int = 0
    overdue_tasks: int = 0
    completion_rate: float = 0.0
    categories: dict = field(default_factory=dict)
    tasks_by_priority: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)
