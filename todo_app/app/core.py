"""Todo App - Core Logic"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from todo_app.app.models import Task, TaskStatus, TaskPriority, TodoStats
from todo_app.app.storage import StorageHandler

logger = logging.getLogger(__name__)


class TodoManager:
    """Main todo manager"""

    def __init__(self, storage_dir: str = "./data"):
        """Initialize todo manager
        
        Args:
            storage_dir: Storage directory
        """
        self.storage = StorageHandler(storage_dir)
        logger.info("TodoManager initialized")

    def add_task(
        self,
        title: str,
        description: str = "",
        category: str = "general",
        priority: str = "medium",
        due_date: Optional[str] = None,
        tags: List[str] = None,
    ) -> int:
        """Add a new task
        
        Args:
            title: Task title
            description: Task description
            category: Task category
            priority: Task priority
            due_date: Due date
            tags: Task tags
            
        Returns:
            Task ID
        """
        task = Task(
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
            tags=tags or [],
        )
        
        task_id = self.storage.save_task(task.to_dict())
        logger.info(f"Task added: {task_id}")
        return task_id

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get task by ID
        
        Args:
            task_id: Task ID
            
        Returns:
            Task data or None
        """
        return self.storage.get_task(task_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks
        
        Returns:
            List of tasks
        """
        return self.storage.get_all_tasks()

    def update_task(self, task_id: int, **updates) -> bool:
        """Update task
        
        Args:
            task_id: Task ID
            **updates: Fields to update
            
        Returns:
            Success status
        """
        task = self.storage.get_task(task_id)
        if not task:
            logger.warning(f"Task not found: {task_id}")
            return False
        
        task.update(updates)
        return self.storage.update_task(task_id, task)

    def delete_task(self, task_id: int) -> bool:
        """Delete task
        
        Args:
            task_id: Task ID
            
        Returns:
            Success status
        """
        return self.storage.delete_task(task_id)

    def mark_complete(self, task_id: int) -> bool:
        """Mark task as complete
        
        Args:
            task_id: Task ID
            
        Returns:
            Success status
        """
        return self.update_task(
            task_id,
            status=TaskStatus.COMPLETED.value,
            completed_at=datetime.now().isoformat(),
        )

    def mark_pending(self, task_id: int) -> bool:
        """Mark task as pending
        
        Args:
            task_id: Task ID
            
        Returns:
            Success status
        """
        return self.update_task(
            task_id,
            status=TaskStatus.PENDING.value,
            completed_at=None,
        )

    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Search tasks
        
        Args:
            query: Search query
            
        Returns:
            Matching tasks
        """
        return self.storage.search_tasks(query)

    def filter_tasks(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Filter tasks
        
        Args:
            status: Task status
            category: Task category
            priority: Task priority
            
        Returns:
            Filtered tasks
        """
        filters = {}
        if status:
            filters["status"] = status
        if category:
            filters["category"] = category
        if priority:
            filters["priority"] = priority
        
        return self.storage.filter_tasks(**filters) if filters else self.get_all_tasks()

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get overdue tasks
        
        Returns:
            List of overdue tasks
        """
        tasks = self.get_all_tasks()
        today = datetime.now().date()
        
        overdue = []
        for task in tasks:
            if task.get("due_date") and task.get("status") != "completed":
                due_date = datetime.fromisoformat(task["due_date"]).date()
                if due_date < today:
                    overdue.append(task)
        
        return overdue

    def get_due_today(self) -> List[Dict[str, Any]]:
        """Get tasks due today
        
        Returns:
            List of tasks due today
        """
        tasks = self.get_all_tasks()
        today = datetime.now().date()
        
        due_today = []
        for task in tasks:
            if task.get("due_date") and task.get("status") != "completed":
                due_date = datetime.fromisoformat(task["due_date"]).date()
                if due_date == today:
                    due_today.append(task)
        
        return due_today

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics
        
        Returns:
            Statistics data
        """
        return self.storage.get_statistics()

    def clear_completed(self) -> int:
        """Clear completed tasks
        
        Returns:
            Number of deleted tasks
        """
        tasks = self.get_all_tasks()
        completed = [t for t in tasks if t.get("status") == "completed"]
        
        count = 0
        for task in completed:
            if self.delete_task(task["id"]):
                count += 1
        
        return count

    def backup(self) -> str:
        """Create backup
        
        Returns:
            Backup file path
        """
        return self.storage.backup()

    def restore(self, backup_file: str) -> bool:
        """Restore from backup
        
        Args:
            backup_file: Backup file path
            
        Returns:
            Success status
        """
        return self.storage.restore(backup_file)

    def export_csv(self, filename: str) -> bool:
        """Export to CSV
        
        Args:
            filename: Output filename
            
        Returns:
            Success status
        """
        return self.storage.export_csv(filename)

    def import_csv(self, filename: str) -> bool:
        """Import from CSV
        
        Args:
            filename: Input filename
            
        Returns:
            Success status
        """
        return self.storage.import_csv(filename)
