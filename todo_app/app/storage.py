"""Todo App - Local Storage Handler"""

import json
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class StorageHandler:
    """Handle local storage for todos"""

    def __init__(self, storage_dir: str = "./data", filename: str = "todos.json"):
        """Initialize storage
        
        Args:
            storage_dir: Directory for storage
            filename: Filename for todos
        """
        self.storage_dir = Path(storage_dir)
        self.storage_file = self.storage_dir / filename
        self.backup_dir = self.storage_dir / "backups"
        
        # Create directories
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize file if not exists
        if not self.storage_file.exists():
            self._initialize_storage()

    def _initialize_storage(self) -> None:
        """Initialize empty storage"""
        data = {"tasks": [], "metadata": {"version": "1.0", "created_at": datetime.now().isoformat()}}
        self._write_file(data)
        logger.info(f"Storage initialized: {self.storage_file}")

    def _read_file(self) -> Dict[str, Any]:
        """Read storage file
        
        Returns:
            Storage data
        """
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Read error: {str(e)}")
            return {"tasks": []}

    def _write_file(self, data: Dict[str, Any]) -> None:
        """Write to storage file
        
        Args:
            data: Data to write
        """
        try:
            with open(self.storage_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Storage updated: {len(data.get('tasks', []))} tasks")
        except Exception as e:
            logger.error(f"Write error: {str(e)}")

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks
        
        Returns:
            List of tasks
        """
        data = self._read_file()
        return data.get("tasks", [])

    def save_task(self, task: Dict[str, Any]) -> int:
        """Save a task
        
        Args:
            task: Task data
            
        Returns:
            Task ID
        """
        data = self._read_file()
        tasks = data.get("tasks", [])
        
        # Generate ID
        task_id = max([t.get("id", 0) for t in tasks], default=0) + 1
        task["id"] = task_id
        task["created_at"] = task.get("created_at", datetime.now().isoformat())
        
        tasks.append(task)
        data["tasks"] = tasks
        self._write_file(data)
        
        logger.info(f"Task saved: {task_id}")
        return task_id

    def update_task(self, task_id: int, task: Dict[str, Any]) -> bool:
        """Update a task
        
        Args:
            task_id: Task ID
            task: Updated task data
            
        Returns:
            Success status
        """
        data = self._read_file()
        tasks = data.get("tasks", [])
        
        for i, t in enumerate(tasks):
            if t.get("id") == task_id:
                task["id"] = task_id
                task["created_at"] = t.get("created_at", datetime.now().isoformat())
                tasks[i] = task
                data["tasks"] = tasks
                self._write_file(data)
                logger.info(f"Task updated: {task_id}")
                return True
        
        logger.warning(f"Task not found: {task_id}")
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task
        
        Args:
            task_id: Task ID
            
        Returns:
            Success status
        """
        data = self._read_file()
        tasks = data.get("tasks", [])
        
        original_count = len(tasks)
        tasks = [t for t in tasks if t.get("id") != task_id]
        
        if len(tasks) < original_count:
            data["tasks"] = tasks
            self._write_file(data)
            logger.info(f"Task deleted: {task_id}")
            return True
        
        logger.warning(f"Task not found: {task_id}")
        return False

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get specific task
        
        Args:
            task_id: Task ID
            
        Returns:
            Task data or None
        """
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                return task
        return None

    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Search tasks by title or description
        
        Args:
            query: Search query
            
        Returns:
            Matching tasks
        """
        tasks = self.get_all_tasks()
        query_lower = query.lower()
        
        return [
            t for t in tasks
            if query_lower in t.get("title", "").lower()
            or query_lower in t.get("description", "").lower()
        ]

    def filter_tasks(self, **filters) -> List[Dict[str, Any]]:
        """Filter tasks by criteria
        
        Args:
            **filters: Filter criteria (status, category, priority)
            
        Returns:
            Filtered tasks
        """
        tasks = self.get_all_tasks()
        
        for key, value in filters.items():
            tasks = [t for t in tasks if t.get(key) == value]
        
        return tasks

    def backup(self) -> str:
        """Create backup
        
        Returns:
            Backup file path
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"todos_backup_{timestamp}.json"
            shutil.copy(self.storage_file, backup_file)
            logger.info(f"Backup created: {backup_file}")
            return str(backup_file)
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            return ""

    def restore(self, backup_file: str) -> bool:
        """Restore from backup
        
        Args:
            backup_file: Backup file path
            
        Returns:
            Success status
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                logger.error(f"Backup not found: {backup_file}")
                return False
            
            shutil.copy(backup_path, self.storage_file)
            logger.info(f"Restored from: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Restore failed: {str(e)}")
            return False

    def export_csv(self, filename: str) -> bool:
        """Export to CSV
        
        Args:
            filename: Output CSV file
            
        Returns:
            Success status
        """
        try:
            import csv
            tasks = self.get_all_tasks()
            
            if not tasks:
                logger.warning("No tasks to export")
                return False
            
            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
                writer.writeheader()
                writer.writerows(tasks)
            
            logger.info(f"Exported to CSV: {filename}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            return False

    def import_csv(self, filename: str) -> bool:
        """Import from CSV
        
        Args:
            filename: Input CSV file
            
        Returns:
            Success status
        """
        try:
            import csv
            backup = self.backup()
            
            tasks = []
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tasks.append(dict(row))
            
            data = {"tasks": tasks, "metadata": {"version": "1.0", "imported_from": filename}}
            self._write_file(data)
            
            logger.info(f"Imported {len(tasks)} tasks from: {filename}")
            return True
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics
        
        Returns:
            Statistics
        """
        tasks = self.get_all_tasks()
        
        completed = [t for t in tasks if t.get("status") == "completed"]
        pending = [t for t in tasks if t.get("status") == "pending"]
        
        # Category stats
        categories = {}
        for task in tasks:
            cat = task.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
        
        # Priority stats
        priorities = {}
        for task in tasks:
            pri = task.get("priority", "medium")
            priorities[pri] = priorities.get(pri, 0) + 1
        
        total = len(tasks)
        completed_count = len(completed)
        
        return {
            "total_tasks": total,
            "completed_tasks": completed_count,
            "pending_tasks": len(pending),
            "completion_rate": (completed_count / total * 100) if total > 0 else 0,
            "categories": categories,
            "priorities": priorities,
            "storage_file": str(self.storage_file),
        }
