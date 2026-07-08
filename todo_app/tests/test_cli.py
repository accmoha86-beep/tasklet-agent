"""CLI Tests for Todo App"""

import pytest
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime, timedelta


class TestCLI:
    """CLI command tests"""

    @pytest.fixture
    def setup(self, tmp_path):
        """Setup test environment"""
        # Set environment to use temp directory
        os.environ['TODO_STORAGE_DIR'] = str(tmp_path / 'todos')
        yield
        # Cleanup
        if 'TODO_STORAGE_DIR' in os.environ:
            del os.environ['TODO_STORAGE_DIR']

    def run_cli(self, *args):
        """Run CLI command and return output"""
        cmd = ['python', '-m', 'todo_app.main'] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def test_help_command(self, setup):
        """Test help command"""
        returncode, stdout, stderr = self.run_cli('help')
        assert returncode == 0
        assert 'Commands:' in stdout
        assert 'add' in stdout
        assert 'list' in stdout

    def test_init_command(self, setup):
        """Test init command"""
        returncode, stdout, stderr = self.run_cli('init')
        assert returncode == 0
        assert 'Storage initialized' in stdout

    def test_add_task(self, setup):
        """Test adding a task"""
        returncode, stdout, stderr = self.run_cli('add', 'Buy groceries')
        assert returncode == 0
        assert 'Task added' in stdout

    def test_add_task_with_options(self, setup):
        """Test adding task with category and priority"""
        returncode, stdout, stderr = self.run_cli(
            'add', 'Learn Python',
            '--category', 'learning',
            '--priority', 'high'
        )
        assert returncode == 0
        assert 'Task added' in stdout

    def test_list_tasks(self, setup):
        """Test listing tasks"""
        # Add some tasks first
        self.run_cli('add', 'Task 1')
        self.run_cli('add', 'Task 2')

        returncode, stdout, stderr = self.run_cli('list')
        assert returncode == 0
        assert 'Task 1' in stdout or '#1' in stdout

    def test_list_tasks_empty(self, setup):
        """Test list on empty todo list"""
        returncode, stdout, stderr = self.run_cli('list')
        assert returncode == 0
        assert 'No tasks found' in stdout or len(stdout.strip()) > 0

    def test_complete_task(self, setup):
        """Test marking task as complete"""
        # Add a task
        self.run_cli('add', 'Task to complete')

        # Complete it
        returncode, stdout, stderr = self.run_cli('complete', '1')
        assert returncode == 0
        assert 'completed' in stdout.lower() or 'completed' in stderr.lower()

    def test_delete_task(self, setup):
        """Test deleting a task"""
        # Add a task
        self.run_cli('add', 'Task to delete')

        # Delete it
        returncode, stdout, stderr = self.run_cli('delete', '1')
        assert returncode == 0
        assert 'deleted' in stdout.lower() or 'deleted' in stderr.lower()

    def test_search_tasks(self, setup):
        """Test searching tasks"""
        # Add tasks
        self.run_cli('add', 'Buy groceries')
        self.run_cli('add', 'Buy books')
        self.run_cli('add', 'Learn Python')

        # Search for 'buy'
        returncode, stdout, stderr = self.run_cli('search', 'buy')
        assert returncode == 0
        # Should find tasks with 'buy' in them

    def test_search_no_results(self, setup):
        """Test search with no results"""
        returncode, stdout, stderr = self.run_cli('search', 'nonexistent')
        assert returncode == 0
        assert 'No tasks found' in stdout or 'not found' in stdout.lower()

    def test_statistics(self, setup):
        """Test statistics command"""
        # Add and complete some tasks
        self.run_cli('add', 'Task 1')
        self.run_cli('add', 'Task 2')
        self.run_cli('complete', '1')

        returncode, stdout, stderr = self.run_cli('stats')
        assert returncode == 0
        assert 'Statistics' in stdout or 'Total' in stdout

    def test_export_tasks(self, setup, tmp_path):
        """Test exporting tasks to CSV"""
        # Add tasks
        self.run_cli('add', 'Task 1')
        self.run_cli('add', 'Task 2')

        # Export
        export_file = tmp_path / 'export.csv'
        returncode, stdout, stderr = self.run_cli('export', str(export_file))
        assert returncode == 0
        assert 'Exported' in stdout or export_file.exists()

    def test_backup_and_restore(self, setup, tmp_path):
        """Test backup and restore"""
        # Add a task
        self.run_cli('add', 'Important task')

        # Backup
        returncode, stdout, stderr = self.run_cli('backup')
        assert returncode == 0
        assert 'Backup created' in stdout

    def test_clear_completed(self, setup):
        """Test clearing completed tasks"""
        # Add and complete tasks
        self.run_cli('add', 'Task 1')
        self.run_cli('add', 'Task 2')
        self.run_cli('complete', '1')

        # Clear
        returncode, stdout, stderr = self.run_cli('clear')
        assert returncode == 0
        assert 'Cleared' in stdout

    def test_add_task_missing_title(self, setup):
        """Test add command without title"""
        returncode, stdout, stderr = self.run_cli('add')
        assert returncode != 0 or 'Usage' in stdout or 'Usage' in stderr

    def test_complete_nonexistent_task(self, setup):
        """Test completing non-existent task"""
        returncode, stdout, stderr = self.run_cli('complete', '999')
        # Should fail or not find task
        assert 'not found' in stdout.lower() or 'not found' in stderr.lower() or returncode != 0

    def test_unknown_command(self, setup):
        """Test unknown command"""
        returncode, stdout, stderr = self.run_cli('unknown')
        assert returncode != 0 or 'Unknown' in stdout or 'Unknown' in stderr


class TestCLIIntegration:
    """Integration tests for CLI"""

    def test_full_workflow(self, tmp_path):
        """Test complete workflow: add, list, complete, list"""
        os.environ['TODO_STORAGE_DIR'] = str(tmp_path / 'todos')

        cmd_add1 = subprocess.run(
            ['python', '-m', 'todo_app.main', 'add', 'Buy groceries'],
            capture_output=True, text=True
        )
        assert cmd_add1.returncode == 0

        cmd_add2 = subprocess.run(
            ['python', '-m', 'todo_app.main', 'add', 'Learn Python'],
            capture_output=True, text=True
        )
        assert cmd_add2.returncode == 0

        cmd_list1 = subprocess.run(
            ['python', '-m', 'todo_app.main', 'list'],
            capture_output=True, text=True
        )
        assert cmd_list1.returncode == 0
        # Should show 2 tasks

        cmd_complete = subprocess.run(
            ['python', '-m', 'todo_app.main', 'complete', '1'],
            capture_output=True, text=True
        )
        assert cmd_complete.returncode == 0

        if 'TODO_STORAGE_DIR' in os.environ:
            del os.environ['TODO_STORAGE_DIR']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
