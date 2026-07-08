"""Tests for Todo App"""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from todo_app.app.core import TodoManager
from todo_app.app.storage import StorageHandler


class TestStorageHandler:
    """Test storage handler"""

    @pytest.fixture
    def storage(self):
        """Create temporary storage"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield StorageHandler(tmpdir)

    def test_save_task(self, storage):
        """Test saving task"""
        task = {
            "title": "Test Task",
            "category": "test",
            "priority": "high",
        }
        task_id = storage.save_task(task)
        assert task_id > 0

    def test_get_task(self, storage):
        """Test getting task"""
        task = {"title": "Test", "category": "test"}
        task_id = storage.save_task(task)
        retrieved = storage.get_task(task_id)
        assert retrieved is not None
        assert retrieved["title"] == "Test"

    def test_delete_task(self, storage):
        """Test deleting task"""
        task = {"title": "Test"}
        task_id = storage.save_task(task)
        assert storage.delete_task(task_id)
        assert storage.get_task(task_id) is None

    def test_search_tasks(self, storage):
        """Test searching tasks"""
        storage.save_task({"title": "Learn Python"})
        storage.save_task({"title": "Buy groceries"})
        results = storage.search_tasks("python")
        assert len(results) == 1

    def test_filter_tasks(self, storage):
        """Test filtering tasks"""
        storage.save_task({"title": "Task 1", "status": "completed"})
        storage.save_task({"title": "Task 2", "status": "pending"})
        results = storage.filter_tasks(status="completed")
        assert len(results) == 1


class TestTodoManager:
    """Test todo manager"""

    @pytest.fixture
    def manager(self):
        """Create temporary manager"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield TodoManager(tmpdir)

    def test_add_task(self, manager):
        """Test adding task"""
        task_id = manager.add_task("Test Task", category="test")
        assert task_id > 0

    def test_get_all_tasks(self, manager):
        """Test getting all tasks"""
        manager.add_task("Task 1")
        manager.add_task("Task 2")
        tasks = manager.get_all_tasks()
        assert len(tasks) == 2

    def test_mark_complete(self, manager):
        """Test marking task complete"""
        task_id = manager.add_task("Task")
        manager.mark_complete(task_id)
        task = manager.get_task(task_id)
        assert task["status"] == "completed"

    def test_search_tasks(self, manager):
        """Test searching"""
        manager.add_task("Learn Python")
        manager.add_task("Learn JavaScript")
        results = manager.search_tasks("Python")
        assert len(results) == 1

    def test_statistics(self, manager):
        """Test getting statistics"""
        manager.add_task("Task 1", category="work", priority="high")
        manager.add_task("Task 2", category="personal")
        stats = manager.get_statistics()
        assert stats["total_tasks"] == 2
        assert "work" in stats["categories"]

    def test_backup_restore(self, manager):
        """Test backup and restore"""
        manager.add_task("Important Task")
        backup_file = manager.backup()
        assert backup_file and Path(backup_file).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
