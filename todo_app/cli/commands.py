"""Todo App - CLI Interface"""

import click
import json
from typing import Optional
from tabulate import tabulate
from todo_app.app.core import TodoManager


class CLI:
    """Command line interface for todo app"""

    def __init__(self):
        """Initialize CLI"""
        self.manager = TodoManager()

    @click.group()
    def cli(self):
        """Todo App CLI"""
        pass

    @cli.command()
    @click.argument("title")
    @click.option("--desc", "-d", default="", help="Task description")
    @click.option("--category", "-c", default="general", help="Task category")
    @click.option("--priority", "-p", default="medium", help="Task priority")
    @click.option("--due", "-D", default=None, help="Due date (YYYY-MM-DD)")
    def add(self, title: str, desc: str, category: str, priority: str, due: Optional[str]):
        """Add a new task"""
        task_id = self.manager.add_task(
            title=title,
            description=desc,
            category=category,
            priority=priority,
            due_date=due,
        )
        click.echo(f"✓ Task added: #{task_id} {title}")

    @cli.command()
    @click.option("--status", "-s", default=None, help="Filter by status")
    @click.option("--category", "-c", default=None, help="Filter by category")
    @click.option("--priority", "-p", default=None, help="Filter by priority")
    def list(self, status: Optional[str], category: Optional[str], priority: Optional[str]):
        """List tasks"""
        tasks = self.manager.filter_tasks(
            status=status,
            category=category,
            priority=priority,
        )
        
        if not tasks:
            click.echo("No tasks found.")
            return
        
        # Format for display
        display = []
        for task in tasks:
            display.append([
                task["id"],
                task["title"],
                task["status"],
                task["priority"],
                task["category"],
                task.get("due_date", "-"),
            ])
        
        print(tabulate(
            display,
            headers=["ID", "Title", "Status", "Priority", "Category", "Due Date"],
            tablefmt="grid"
        ))

    @cli.command()
    @click.argument("task_id", type=int)
    def complete(self, task_id: int):
        """Mark task as complete"""
        if self.manager.mark_complete(task_id):
            click.echo(f"✓ Task #{task_id} completed")
        else:
            click.echo(f"✗ Task #{task_id} not found")

    @cli.command()
    @click.argument("task_id", type=int)
    def delete(self, task_id: int):
        """Delete a task"""
        if self.manager.delete_task(task_id):
            click.echo(f"✓ Task #{task_id} deleted")
        else:
            click.echo(f"✗ Task #{task_id} not found")

    @cli.command()
    @click.argument("query")
    def search(self, query: str):
        """Search tasks"""
        tasks = self.manager.search_tasks(query)
        
        if not tasks:
            click.echo(f"No tasks found matching '{query}'")
            return
        
        display = []
        for task in tasks:
            display.append([
                task["id"],
                task["title"],
                task["status"],
            ])
        
        print(tabulate(
            display,
            headers=["ID", "Title", "Status"],
            tablefmt="grid"
        ))

    @cli.command()
    def stats(self):
        """Show statistics"""
        stats = self.manager.get_statistics()
        
        click.echo("\n📊 Todo Statistics:")
        click.echo(f"  Total Tasks: {stats['total_tasks']}")
        click.echo(f"  Completed: {stats['completed_tasks']}")
        click.echo(f"  Pending: {stats['pending_tasks']}")
        click.echo(f"  Completion Rate: {stats['completion_rate']:.1f}%")
        
        if stats["categories"]:
            click.echo(f"\n  Categories:")
            for cat, count in stats["categories"].items():
                click.echo(f"    - {cat}: {count}")
        
        if stats["priorities"]:
            click.echo(f"\n  Priorities:")
            for pri, count in stats["priorities"].items():
                click.echo(f"    - {pri}: {count}")

    @cli.command()
    @click.argument("filename")
    def export(self, filename: str):
        """Export to CSV"""
        if self.manager.export_csv(filename):
            click.echo(f"✓ Exported to {filename}")
        else:
            click.echo(f"✗ Export failed")

    @cli.command()
    @click.argument("filename")
    def import_data(self, filename: str):
        """Import from CSV"""
        if self.manager.import_csv(filename):
            click.echo(f"✓ Imported from {filename}")
        else:
            click.echo(f"✗ Import failed")


if __name__ == "__main__":
    cli = CLI()
    cli.cli()
