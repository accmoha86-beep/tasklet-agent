"""Recurring Tasks System for Todo App"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional
from copy import deepcopy

from .models import Task, RecurrenceConfig, RecurrencePattern, TaskStatus

logger = logging.getLogger(__name__)


class RecurringTaskManager:
    """Manages recurring tasks"""

    def __init__(self):
        """Initialize recurring task manager"""
        pass

    def create_recurring_task(self, task: Task, recurrence: RecurrenceConfig) -> Task:
        """Create a recurring task"""
        task.recurrence = recurrence
        logger.info(f"Created recurring task {task.id} with pattern {recurrence.pattern.value}")
        return task

    def generate_next_occurrence(self, task: Task, completed_at: Optional[datetime] = None) -> Optional[Task]:
        """Generate the next occurrence of a recurring task"""
        if task.recurrence.pattern == RecurrencePattern.NONE:
            return None

        # Check if we've reached max occurrences
        if task.recurrence.max_occurrences:
            if task.occurrence_number >= task.recurrence.max_occurrences:
                logger.info(f"Task {task.id} reached max occurrences")
                return None

        # Check if we've passed end date
        if task.recurrence.end_date:
            if datetime.now() >= task.recurrence.end_date:
                logger.info(f"Task {task.id} reached end date")
                return None

        # Create new task instance
        next_task = deepcopy(task)
        next_task.id = f"{task.id}_occ_{task.occurrence_number + 1}"
        next_task.parent_task_id = task.id
        next_task.occurrence_number = task.occurrence_number + 1
        next_task.status = TaskStatus.PENDING
        next_task.completed_at = None
        next_task.is_recurring_instance = True
        next_task.created_at = datetime.now()
        next_task.updated_at = datetime.now()

        # Calculate next due date
        base_date = completed_at or datetime.now()
        next_task.due_date = self._calculate_next_due_date(
            base_date,
            task.due_date,
            task.recurrence
        )

        logger.info(f"Generated next occurrence for task {task.id}: {next_task.id}")
        return next_task

    def get_next_occurrences(self, task: Task, count: int = 5) -> List[datetime]:
        """Get the next N occurrence dates for a recurring task"""
        if task.recurrence.pattern == RecurrencePattern.NONE:
            return []

        occurrences = []
        current_date = task.due_date or datetime.now()
        occurrence_num = task.occurrence_number

        for _ in range(count):
            # Check constraints
            if task.recurrence.max_occurrences:
                if occurrence_num >= task.recurrence.max_occurrences:
                    break

            if task.recurrence.end_date:
                if current_date >= task.recurrence.end_date:
                    break

            occurrences.append(current_date)
            current_date = self._calculate_next_due_date(
                current_date,
                current_date,
                task.recurrence
            )
            occurrence_num += 1

        return occurrences

    def _calculate_next_due_date(self, base_date: datetime, current_due: Optional[datetime],
                                   recurrence: RecurrenceConfig) -> datetime:
        """Calculate the next due date based on recurrence pattern"""
        if current_due:
            base_date = current_due

        interval = recurrence.interval or 1

        if recurrence.pattern == RecurrencePattern.DAILY:
            next_date = base_date + timedelta(days=interval)
            if recurrence.skip_weekends:
                # Skip weekends (5=Saturday, 6=Sunday)
                while next_date.weekday() in [5, 6]:
                    next_date += timedelta(days=1)
            return next_date

        elif recurrence.pattern == RecurrencePattern.WEEKLY:
            if recurrence.custom_days:
                # Find next occurrence on specified weekdays
                next_date = base_date + timedelta(days=1)
                while next_date.weekday() not in recurrence.custom_days:
                    next_date += timedelta(days=1)
                return next_date
            else:
                return base_date + timedelta(weeks=interval)

        elif recurrence.pattern == RecurrencePattern.BIWEEKLY:
            return base_date + timedelta(weeks=2 * interval)

        elif recurrence.pattern == RecurrencePattern.MONTHLY:
            # Add months carefully to handle month-end edge cases
            year = base_date.year
            month = base_date.month + interval
            day = base_date.day

            while month > 12:
                year += 1
                month -= 12

            # Handle day overflow (e.g., Jan 31 + 1 month)
            while True:
                try:
                    return base_date.replace(year=year, month=month, day=day)
                except ValueError:
                    day -= 1

        elif recurrence.pattern == RecurrencePattern.QUARTERLY:
            year = base_date.year
            month = base_date.month + (3 * interval)
            day = base_date.day

            while month > 12:
                year += 1
                month -= 12

            while True:
                try:
                    return base_date.replace(year=year, month=month, day=day)
                except ValueError:
                    day -= 1

        elif recurrence.pattern == RecurrencePattern.YEARLY:
            return base_date.replace(year=base_date.year + interval)

        return base_date

    def get_overdue_recurring_tasks(self, tasks: List[Task]) -> List[Task]:
        """Get recurring tasks that are overdue"""
        overdue = []
        for task in tasks:
            if task.recurrence.pattern != RecurrencePattern.NONE and task.is_overdue():
                overdue.append(task)
        return overdue

    def auto_complete_and_reschedule(self, task: Task) -> Optional[Task]:
        """Mark task complete and generate next occurrence"""
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        logger.info(f"Completed task {task.id}")

        next_occurrence = self.generate_next_occurrence(task, datetime.now())
        if next_occurrence:
            logger.info(f"Auto-scheduled next occurrence: {next_occurrence.id}")

        return next_occurrence
