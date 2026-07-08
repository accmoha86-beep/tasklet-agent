"""Reminder System for Todo App"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from .models import Task, Reminder, ReminderType, TaskStatus

logger = logging.getLogger(__name__)


class ReminderManager:
    """Manages task reminders"""

    def __init__(self, storage_dir: str = "./data/todos"):
        """Initialize reminder manager"""
        self.storage_dir = Path(storage_dir)
        self.reminders_file = self.storage_dir / "reminders.json"
        self.reminders: Dict[str, List[Reminder]] = {}
        self._load_reminders()

    def create_reminder(self, task: Task, reminder_type: ReminderType = ReminderType.BEFORE_DUE) -> Reminder:
        """Create a reminder for a task"""
        reminder = Reminder(
            task_id=task.id,
            reminder_type=reminder_type,
        )

        # Calculate scheduled time based on reminder type
        if reminder_type == ReminderType.AT_TIME and task.due_date:
            reminder.scheduled_time = task.due_date
        elif reminder_type == ReminderType.BEFORE_DUE and task.due_date:
            reminder.scheduled_time = task.due_date - timedelta(hours=1)
        elif reminder_type == ReminderType.OVERDUE:
            reminder.scheduled_time = task.due_date + timedelta(hours=1) if task.due_date else datetime.now()
        else:
            reminder.scheduled_time = datetime.now()

        if task.id not in self.reminders:
            self.reminders[task.id] = []

        self.reminders[task.id].append(reminder)
        self._save_reminders()
        logger.info(f"Created {reminder_type.value} reminder for task {task.id}")
        return reminder

    def get_pending_reminders(self) -> List[Reminder]:
        """Get all pending reminders due now"""
        pending = []
        now = datetime.now()

        for task_reminders in self.reminders.values():
            for reminder in task_reminders:
                if not reminder.is_sent and reminder.scheduled_time <= now:
                    pending.append(reminder)

        return pending

    def mark_reminder_sent(self, reminder_id: str) -> bool:
        """Mark a reminder as sent"""
        for task_reminders in self.reminders.values():
            for reminder in task_reminders:
                if reminder.id == reminder_id:
                    reminder.is_sent = True
                    self._save_reminders()
                    logger.info(f"Marked reminder {reminder_id} as sent")
                    return True
        return False

    def get_reminders_for_task(self, task_id: str) -> List[Reminder]:
        """Get all reminders for a task"""
        return self.reminders.get(task_id, [])

    def delete_reminders_for_task(self, task_id: str) -> bool:
        """Delete all reminders for a task"""
        if task_id in self.reminders:
            del self.reminders[task_id]
            self._save_reminders()
            logger.info(f"Deleted all reminders for task {task_id}")
            return True
        return False

    def update_task_reminders(self, task: Task) -> None:
        """Update reminders when task changes (e.g., due date changed)"""
        # Delete old reminders
        self.delete_reminders_for_task(task.id)

        # Create new reminders if task has due date and not completed
        if task.due_date and task.status != TaskStatus.COMPLETED:
            self.create_reminder(task, ReminderType.BEFORE_DUE)

    def get_overdue_tasks_reminders(self, tasks: List[Task]) -> List[Dict]:
        """Get reminders for overdue tasks"""
        overdue_reminders = []

        for task in tasks:
            if task.is_overdue() and task.status != TaskStatus.COMPLETED:
                overdue_reminders.append({
                    'task_id': task.id,
                    'title': task.title,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'days_overdue': (datetime.now() - task.due_date).days,
                })

        return overdue_reminders

    def get_upcoming_reminders(self, hours: int = 24) -> List[Dict]:
        """Get reminders scheduled in the next N hours"""
        upcoming = []
        now = datetime.now()
        future = now + timedelta(hours=hours)

        for task_id, task_reminders in self.reminders.items():
            for reminder in task_reminders:
                if not reminder.is_sent and now <= reminder.scheduled_time <= future:
                    upcoming.append({
                        'task_id': task_id,
                        'reminder_id': reminder.id,
                        'type': reminder.reminder_type.value,
                        'scheduled_time': reminder.scheduled_time.isoformat(),
                    })

        return sorted(upcoming, key=lambda x: x['scheduled_time'])

    def _load_reminders(self) -> None:
        """Load reminders from storage"""
        try:
            if self.reminders_file.exists():
                with open(self.reminders_file, 'r') as f:
                    data = json.load(f)
                    for task_id, reminders_data in data.items():
                        self.reminders[task_id] = [
                            Reminder.from_dict(r) for r in reminders_data
                        ]
                logger.info(f"Loaded {sum(len(r) for r in self.reminders.values())} reminders")
        except Exception as e:
            logger.error(f"Error loading reminders: {str(e)}")
            self.reminders = {}

    def _save_reminders(self) -> None:
        """Save reminders to storage"""
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            data = {
                task_id: [r.to_dict() for r in reminders]
                for task_id, reminders in self.reminders.items()
            }
            with open(self.reminders_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved {sum(len(r) for r in self.reminders.values())} reminders")
        except Exception as e:
            logger.error(f"Error saving reminders: {str(e)}")
