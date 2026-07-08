"""Tests for Recurring Tasks System"""

import pytest
from datetime import datetime, timedelta

from todo_app.app.models import Task, RecurrenceConfig, RecurrencePattern, TaskStatus, TaskPriority
from todo_app.app.recurring import RecurringTaskManager


class TestRecurringTaskManager:
    """Test recurring task manager"""

    @pytest.fixture
    def recurring_manager(self):
        """Recurring task manager instance"""
        return RecurringTaskManager()

    @pytest.fixture
    def daily_task(self):
        """Sample daily recurring task"""
        task = Task(
            id="daily1",
            title="Daily standup",
            due_date=datetime.now() + timedelta(days=1),
            recurrence=RecurrenceConfig(
                pattern=RecurrencePattern.DAILY,
                interval=1,
            ),
        )
        return task

    def test_create_recurring_task(self, recurring_manager, daily_task):
        """Test creating a recurring task"""
        assert daily_task.recurrence.pattern == RecurrencePattern.DAILY
        assert daily_task.recurrence.interval == 1

    def test_generate_next_occurrence_daily(self, recurring_manager, daily_task):
        """Test generating next occurrence for daily task"""
        next_task = recurring_manager.generate_next_occurrence(daily_task)
        assert next_task is not None
        assert next_task.parent_task_id == daily_task.id
        assert next_task.occurrence_number == 1
        assert next_task.status == TaskStatus.PENDING

    def test_generate_next_occurrence_weekly(self, recurring_manager):
        """Test generating next occurrence for weekly task"""
        weekly_task = Task(
            id="weekly1",
            title="Weekly review",
            due_date=datetime.now() + timedelta(weeks=1),
            recurrence=RecurrenceConfig(
                pattern=RecurrencePattern.WEEKLY,
                interval=1,
            ),
        )
        next_task = recurring_manager.generate_next_occurrence(weekly_task)
        assert next_task is not None

    def test_get_next_occurrences(self, recurring_manager, daily_task):
        """Test getting next N occurrences"""
        occurrences = recurring_manager.get_next_occurrences(daily_task, count=5)
        assert len(occurrences) == 5
        # Each should be 1 day apart
        for i in range(1, len(occurrences)):
            delta = occurrences[i] - occurrences[i-1]
            assert delta.days == 1

    def test_max_occurrences_limit(self, recurring_manager):
        """Test that max occurrences limit is respected"""
        limited_task = Task(
            id="limited1",
            title="Limited task",
            due_date=datetime.now() + timedelta(days=1),
            occurrence_number=9,
            recurrence=RecurrenceConfig(
                pattern=RecurrencePattern.DAILY,
                interval=1,
                max_occurrences=10,
            ),
        )
        next_task = recurring_manager.generate_next_occurrence(limited_task)
        assert next_task is not None
        assert next_task.occurrence_number == 10

        # 11th should be None
        next_next = recurring_manager.generate_next_occurrence(next_task)
        assert next_next is None

    def test_end_date_limit(self, recurring_manager):
        """Test that end date limit is respected"""
        end_date = datetime.now() + timedelta(days=5)
        limited_task = Task(
            id="limited2",
            title="Limited task",
            due_date=datetime.now() + timedelta(days=1),
            recurrence=RecurrenceConfig(
                pattern=RecurrencePattern.DAILY,
                interval=1,
                end_date=end_date,
            ),
        )
        next_task = recurring_manager.generate_next_occurrence(limited_task)
        # Due date should be before end date
        assert next_task.due_date < end_date

    def test_skip_weekends(self, recurring_manager):
        """Test daily task that skips weekends"""
        # Start on Friday
        friday = datetime.now()
        while friday.weekday() != 4:  # 4 = Friday
            friday += timedelta(days=1)

        task = Task(
            id="weekend_skip",
            title="Weekday task",
            due_date=friday,
            recurrence=RecurrenceConfig(
                pattern=RecurrencePattern.DAILY,
                interval=1,
                skip_weekends=True,
            ),
        )
        next_task = recurring_manager.generate_next_occurrence(task)
        # Next should be Monday, not Saturday
        assert next_task.due_date.weekday() != 5  # 5 = Saturday

    def test_auto_complete_and_reschedule(self, recurring_manager, daily_task):
        """Test auto-completing and rescheduling task"""
        next_task = recurring_manager.auto_complete_and_reschedule(daily_task)
        assert daily_task.status == TaskStatus.COMPLETED
        assert daily_task.completed_at is not None
        assert next_task is not None

    def test_calculate_monthly_date(self, recurring_manager):
        """Test monthly recurrence date calculation"""
        monthly_task = Task(
            id="monthly1",
            title="Monthly task",
            due_date=datetime(2024, 1, 31),
            recurrence=RecurrenceConfig(
                pattern=RecurrencePattern.MONTHLY,
                interval=1,
            ),
        )
        # Next occurrence should handle month-end properly
        next_date = recurring_manager._calculate_next_due_date(
            monthly_task.due_date,
            monthly_task.due_date,
            monthly_task.recurrence
        )
        # Should go to Feb 29 (2024 is leap year) or Feb 28
        assert next_date.month == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
