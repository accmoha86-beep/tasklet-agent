"""Task Dependencies System for Todo App"""

import logging
from typing import List, Dict, Optional, Set
from collections import defaultdict, deque

from .models import Task, TaskStatus

logger = logging.getLogger(__name__)


class DependencyManager:
    """Manages task dependencies and blocking relationships"""

    def __init__(self):
        """Initialize dependency manager"""
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)  # task_id -> set of dependencies
        self.dependents: Dict[str, Set[str]] = defaultdict(set)    # task_id -> set of dependents

    def add_dependency(self, task_id: str, depends_on_id: str) -> bool:
        """Add a dependency: task_id depends on depends_on_id"""
        if task_id == depends_on_id:
            logger.warning(f"Cannot add self-dependency for task {task_id}")
            return False

        # Check for circular dependency
        if self._would_create_cycle(task_id, depends_on_id):
            logger.warning(f"Would create circular dependency: {task_id} -> {depends_on_id}")
            return False

        self.dependencies[task_id].add(depends_on_id)
        self.dependents[depends_on_id].add(task_id)
        logger.info(f"Added dependency: {task_id} depends on {depends_on_id}")
        return True

    def remove_dependency(self, task_id: str, depends_on_id: str) -> bool:
        """Remove a dependency"""
        if depends_on_id in self.dependencies[task_id]:
            self.dependencies[task_id].remove(depends_on_id)
            self.dependents[depends_on_id].discard(task_id)
            logger.info(f"Removed dependency: {task_id} no longer depends on {depends_on_id}")
            return True
        return False

    def can_start_task(self, task_id: str, tasks_by_id: Dict[str, Task]) -> bool:
        """Check if all dependencies for a task are completed"""
        for dep_id in self.dependencies[task_id]:
            dep_task = tasks_by_id.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    def get_blocking_tasks(self, task_id: str) -> Set[str]:
        """Get tasks blocked by this task"""
        return self.dependents.get(task_id, set()).copy()

    def get_dependencies(self, task_id: str) -> Set[str]:
        """Get tasks this task depends on"""
        return self.dependencies.get(task_id, set()).copy()

    def get_task_chain(self, task_id: str) -> List[str]:
        """Get the dependency chain for a task (BFS)"""
        chain = []
        visited = set()
        queue = deque([task_id])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue

            visited.add(current)
            chain.append(current)

            for dep_id in self.dependencies[current]:
                if dep_id not in visited:
                    queue.append(dep_id)

        return chain[1:] if chain else []  # Exclude the original task

    def get_dependent_chain(self, task_id: str) -> List[str]:
        """Get all tasks that depend on this task (BFS)"""
        chain = []
        visited = set()
        queue = deque([task_id])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue

            visited.add(current)
            chain.append(current)

            for dependent_id in self.dependents[current]:
                if dependent_id not in visited:
                    queue.append(dependent_id)

        return chain[1:] if chain else []  # Exclude the original task

    def get_critical_path(self, tasks_by_id: Dict[str, Task]) -> List[str]:
        """Get critical path (longest dependency chain)"""
        if not tasks_by_id:
            return []

        # Find all root tasks (no dependencies)
        root_tasks = [tid for tid in tasks_by_id.keys() if not self.dependencies[tid]]

        longest_path = []
        for root in root_tasks:
            path = self._dfs_longest_path(root, tasks_by_id)
            if len(path) > len(longest_path):
                longest_path = path

        return longest_path

    def get_dependency_graph(self, tasks_by_id: Dict[str, Task]) -> Dict[str, Dict]:
        """Get complete dependency graph"""
        graph = {}
        for task_id, task in tasks_by_id.items():
            deps = self.dependencies[task_id]
            dependents = self.dependents[task_id]
            graph[task_id] = {
                'task': {
                    'title': task.title,
                    'status': task.status.value,
                },
                'depends_on': list(deps),
                'blocking': list(dependents),
            }
        return graph

    def get_blocked_tasks(self, tasks_by_id: Dict[str, Task]) -> List[str]:
        """Get all tasks that cannot start due to unmet dependencies"""
        blocked = []
        for task_id in tasks_by_id:
            if not self.can_start_task(task_id, tasks_by_id):
                blocked.append(task_id)
        return blocked

    def get_ready_tasks(self, tasks_by_id: Dict[str, Task]) -> List[str]:
        """Get all tasks that can start (dependencies met)"""
        ready = []
        for task_id, task in tasks_by_id.items():
            if task.status == TaskStatus.PENDING and self.can_start_task(task_id, tasks_by_id):
                ready.append(task_id)
        return ready

    def _would_create_cycle(self, task_id: str, depends_on_id: str) -> bool:
        """Check if adding a dependency would create a cycle"""
        # BFS to check if depends_on_id can reach task_id
        visited = set()
        queue = deque([depends_on_id])

        while queue:
            current = queue.popleft()
            if current == task_id:
                return True

            if current in visited:
                continue

            visited.add(current)
            queue.extend(self.dependencies[current])

        return False

    def _dfs_longest_path(self, task_id: str, tasks_by_id: Dict[str, Task], visited: Optional[Set[str]] = None) -> List[str]:
        """DFS to find longest path from a task"""
        if visited is None:
            visited = set()

        if task_id in visited:
            return []

        visited.add(task_id)
        path = [task_id]

        dependents = self.dependents[task_id]
        if not dependents:
            return path

        longest = []
        for dep_id in dependents:
            sub_path = self._dfs_longest_path(dep_id, tasks_by_id, visited.copy())
            if len(sub_path) > len(longest):
                longest = sub_path

        return path + longest
