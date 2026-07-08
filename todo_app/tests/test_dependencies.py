"""Tests for Task Dependencies System"""

import pytest
from datetime import datetime

from todo_app.app.models import Task, TaskStatus, TaskPriority
from todo_app.app.dependencies import DependencyManager


class TestDependencyManager:
    """Test dependency manager"""

    @pytest.fixture
    def dependency_manager(self):
        """Dependency manager instance"""
        return DependencyManager()

    @pytest.fixture
    def sample_tasks(self):
        """Sample tasks"""
        return {
            'task1': Task(id='task1', title='Task 1'),
            'task2': Task(id='task2', title='Task 2'),
            'task3': Task(id='task3', title='Task 3'),
            'task4': Task(id='task4', title='Task 4'),
        }

    def test_add_dependency(self, dependency_manager):
        """Test adding a dependency"""
        success = dependency_manager.add_dependency('task2', 'task1')
        assert success
        assert 'task1' in dependency_manager.get_dependencies('task2')
        assert 'task2' in dependency_manager.get_blocking_tasks('task1')

    def test_self_dependency_rejected(self, dependency_manager):
        """Test that self-dependencies are rejected"""
        success = dependency_manager.add_dependency('task1', 'task1')
        assert not success

    def test_circular_dependency_detection(self, dependency_manager):
        """Test that circular dependencies are detected"""
        dependency_manager.add_dependency('task2', 'task1')
        dependency_manager.add_dependency('task3', 'task2')
        
        # Try to create cycle
        success = dependency_manager.add_dependency('task1', 'task3')
        assert not success  # Should be rejected

    def test_remove_dependency(self, dependency_manager):
        """Test removing a dependency"""
        dependency_manager.add_dependency('task2', 'task1')
        success = dependency_manager.remove_dependency('task2', 'task1')
        assert success
        assert 'task1' not in dependency_manager.get_dependencies('task2')

    def test_can_start_task_no_dependencies(self, dependency_manager, sample_tasks):
        """Test task can start when it has no dependencies"""
        can_start = dependency_manager.can_start_task('task1', sample_tasks)
        assert can_start

    def test_can_start_task_dependencies_met(self, dependency_manager, sample_tasks):
        """Test task can start when dependencies are completed"""
        dependency_manager.add_dependency('task2', 'task1')
        sample_tasks['task1'].status = TaskStatus.COMPLETED
        
        can_start = dependency_manager.can_start_task('task2', sample_tasks)
        assert can_start

    def test_cannot_start_task_dependencies_unmet(self, dependency_manager, sample_tasks):
        """Test task cannot start when dependencies are not completed"""
        dependency_manager.add_dependency('task2', 'task1')
        sample_tasks['task1'].status = TaskStatus.PENDING
        
        can_start = dependency_manager.can_start_task('task2', sample_tasks)
        assert not can_start

    def test_get_blocking_tasks(self, dependency_manager):
        """Test getting tasks blocked by a task"""
        dependency_manager.add_dependency('task2', 'task1')
        dependency_manager.add_dependency('task3', 'task1')
        
        blocking = dependency_manager.get_blocking_tasks('task1')
        assert 'task2' in blocking
        assert 'task3' in blocking

    def test_get_task_chain(self, dependency_manager):
        """Test getting dependency chain"""
        dependency_manager.add_dependency('task2', 'task1')
        dependency_manager.add_dependency('task3', 'task2')
        dependency_manager.add_dependency('task4', 'task3')
        
        chain = dependency_manager.get_task_chain('task4')
        assert 'task3' in chain
        assert 'task2' in chain
        assert 'task1' in chain

    def test_get_dependent_chain(self, dependency_manager):
        """Test getting dependent chain"""
        dependency_manager.add_dependency('task2', 'task1')
        dependency_manager.add_dependency('task3', 'task2')
        dependency_manager.add_dependency('task4', 'task3')
        
        chain = dependency_manager.get_dependent_chain('task1')
        assert 'task2' in chain
        assert 'task3' in chain
        assert 'task4' in chain

    def test_get_blocked_tasks(self, dependency_manager, sample_tasks):
        """Test getting tasks that are blocked"""
        dependency_manager.add_dependency('task2', 'task1')
        sample_tasks['task1'].status = TaskStatus.PENDING
        
        blocked = dependency_manager.get_blocked_tasks(sample_tasks)
        assert 'task2' in blocked

    def test_get_ready_tasks(self, dependency_manager, sample_tasks):
        """Test getting tasks that are ready to start"""
        dependency_manager.add_dependency('task2', 'task1')
        sample_tasks['task1'].status = TaskStatus.COMPLETED
        sample_tasks['task2'].status = TaskStatus.PENDING
        
        ready = dependency_manager.get_ready_tasks(sample_tasks)
        assert 'task2' in ready

    def test_get_critical_path(self, dependency_manager, sample_tasks):
        """Test getting critical path"""
        dependency_manager.add_dependency('task2', 'task1')
        dependency_manager.add_dependency('task3', 'task2')
        dependency_manager.add_dependency('task4', 'task3')
        
        critical_path = dependency_manager.get_critical_path(sample_tasks)
        # Should be at least: task1 -> task2 -> task3 -> task4
        assert len(critical_path) > 0

    def test_get_dependency_graph(self, dependency_manager, sample_tasks):
        """Test getting full dependency graph"""
        dependency_manager.add_dependency('task2', 'task1')
        dependency_manager.add_dependency('task3', 'task1')
        
        graph = dependency_manager.get_dependency_graph(sample_tasks)
        assert 'task1' in graph
        assert 'task2' in graph
        assert len(graph['task1']['blocking']) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
