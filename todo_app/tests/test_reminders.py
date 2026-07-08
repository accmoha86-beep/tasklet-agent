"""Tests for Reminder System"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path

from todo_app.app.models import Task, Reminder, ReminderType, TaskStatus, TaskPriority
from todo_app.app.reminders import ReminderManager


class TestReminderManager:
    """Test reminder manager"""

    @pytest.fixture
    def temp_storage(self, tmp_path):
        """Temporary storage directory"""
        return str(tmp_path)

    @pytest.fixture
    def reminder_manager(self, temp_storage):
        """Reminder manager instance"""
        return ReminderManager(temp_storage)

    @pytest.fixture
    def task(self):
        """Sample task"""
        task = Task(
            id="task1",
            title="Buy groceries",
            due_date=datetime.now() + timedelta(hours=2),
        )
        return task

    def test_create_reminder(self, reminder_manager, task):
        """Test creating a reminder"""
        reminder = reminder_manager.create_reminder(task, ReminderType.BEFORE_DUE)
        assert reminder.task_id == task.id
        assert reminder.reminder_type == ReminderType.BEFORE_DUE
        assert not reminder.is_sent

    def test_get_pending_reminders(self, reminder_manager, task):
        """Test getting pending reminders"""
        # Create reminder with past scheduled time
        reminder = Reminder(
            task_id=task.id,
            reminder_type=ReminderType.BEFORE_DUE,
            scheduled_time=datetime.now() - timedelta(minutes=1),
            is_sent=False,
        )
        reminder_manager.reminders[task.id] = [reminder]

        pending = reminder_manager.get_pending_reminders()
        assert len(pending) > 0
        assert reminder in pending

    def test_mark_reminder_sent(self, reminder_manager, task):
        """Test marking reminder as sent"""
        reminder = reminder_manager.create_reminder(task, ReminderType.BEFORE_DUE)
        reminder_id = reminder.id

        success = reminder_manager.mark_reminder_sent(reminder_id)
        assert success
        assert reminder.is_sent

    def test_get_reminders_for_task(self, reminder_manager, task):
        """Test getting reminders for specific task"""
        reminder1 = reminder_manager.create_reminder(task, ReminderType.BEFORE_DUE)
        reminder2 = reminder_manager.create_reminder(task, ReminderType.AT_TIME)

        reminders = reminder_manager.get_reminders_for_task(task.id)
        assert len(reminders) == 2

    def test_delete_reminders_for_task(self, reminder_manager, task):
        """Test deleting all reminders for a task"""
        reminder_manager.create_reminder(task, ReminderType.BEFORE_DUE)
        reminder_manager.create_reminder(task, ReminderType.AT_TIME)

        success = reminder_manager.delete_reminders_for_task(task.id)
        assert success
        assert len(reminder_manager.get_reminders_for_task(task.id)) == 0

    def test_get_overdue_tasks_reminders(self, reminder_manager):
        """Test getting reminders for overdue tasks"""
        overdue_task = Task(
            id="overdue1",
            title="Late task",
            due_date=datetime.now() - timedelta(hours=1),
            status=TaskStatus.PENDING,
        )
        completed_task = Task(
            id="completed1",
            title="Completed task",
            due_date=datetime.now() - timedelta(hours=1),
            status=TaskStatus.COMPLETED,
        )

        reminders = reminder_manager.get_overdue_tasks_reminders([overdue_task, completed_task])
        # Should only have overdue_task
        assert len(reminders) == 1
        assert reminders[0]['task_id'] == 'overdue1'

    def test_get_upcoming_reminders(self, reminder_manager, task):
        """Test getting upcoming reminders"""
        reminder = Reminder(
            task_id=task.id,
            reminder_type=ReminderType.BEFORE_DUE,
            scheduled_time=datetime.now() + timedelta(hours=2),
            is_sent=False,
        )
        reminder_manager.reminders[task.id] = [reminder]

        upcoming = reminder_manager.get_upcoming_reminders(hours=3)
        assert len(upcoming) > 0
        assert upcoming[0]['task_id'] == task.id

    def test_reminder_persistence(self, temp_storage, task):
        """Test saving and loading reminders"""
        manager1 = ReminderManager(temp_storage)
        manager1.create_reminder(task, ReminderType.BEFORE_DUE)

        # Create new manager instance
        manager2 = ReminderManager(temp_storage)
        reminders = manager2.get_reminders_for_task(task.id)
        assert len(reminders) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
