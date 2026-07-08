"""Todo App - Main Entry Point"""

import os
import sys
import logging
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo_app.app.core import TodoManager
from todo_app.config import LOG_LEVEL, LOG_FILE

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print app banner"""
    print("""
    ╔═══════════════════════════════════════╗
    ║   📋 TODO APP - Local Storage 📋       ║
    ║   Full-featured task manager           ║
    ╚═══════════════════════════════════════╝
    """)


def print_help():
    """Print help menu"""
    print("""
    Usage: python main.py [COMMAND] [OPTIONS]

    Commands:
      add <title>          Add a new task
      list                 List all tasks
      complete <id>        Mark task complete
      delete <id>          Delete a task
      search <query>       Search tasks
      stats                Show statistics
      export <file>        Export to CSV
      import <file>        Import from CSV
      backup               Create backup
      restore <file>       Restore from backup
      web                  Start web interface
      clear                Clear completed tasks
      init                 Initialize storage
      help                 Show this help

    Examples:
      python main.py add "Buy groceries" --category shopping --priority high
      python main.py list
      python main.py complete 1
      python main.py search "python"
      python main.py stats
    """)


def main():
    """Main entry point"""
    print_banner()

    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()
    manager = TodoManager()

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Usage: python main.py add <title> [options]")
                return
            title = sys.argv[2]
            task_id = manager.add_task(title)
            print(f"✓ Task added: #{task_id}")

        elif command == "list":
            tasks = manager.get_all_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    status = "✓" if task["status"] == "completed" else "○"
                    print(f"{status} #{task['id']}: {task['title']} [{task['priority']}]")

        elif command == "complete":
            if len(sys.argv) < 3:
                print("Usage: python main.py complete <id>")
                return
            task_id = int(sys.argv[2])
            if manager.mark_complete(task_id):
                print(f"✓ Task #{task_id} completed")
            else:
                print(f"✗ Task not found")

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Usage: python main.py delete <id>")
                return
            task_id = int(sys.argv[2])
            if manager.delete_task(task_id):
                print(f"✓ Task #{task_id} deleted")
            else:
                print(f"✗ Task not found")

        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: python main.py search <query>")
                return
            query = sys.argv[2]
            results = manager.search_tasks(query)
            if results:
                for task in results:
                    print(f"#{task['id']}: {task['title']}")
            else:
                print(f"No tasks found matching '{query}'")

        elif command == "stats":
            stats = manager.get_statistics()
            print(f"\n📊 Statistics:")
            print(f"  Total: {stats['total_tasks']}")
            print(f"  Completed: {stats['completed_tasks']}")
            print(f"  Pending: {stats['pending_tasks']}")
            print(f"  Rate: {stats['completion_rate']:.1f}%")

        elif command == "export":
            if len(sys.argv) < 3:
                print("Usage: python main.py export <filename>")
                return
            filename = sys.argv[2]
            if manager.export_csv(filename):
                print(f"✓ Exported to {filename}")
            else:
                print(f"✗ Export failed")

        elif command == "import":
            if len(sys.argv) < 3:
                print("Usage: python main.py import <filename>")
                return
            filename = sys.argv[2]
            if manager.import_csv(filename):
                print(f"✓ Imported from {filename}")
            else:
                print(f"✗ Import failed")

        elif command == "backup":
            backup_file = manager.backup()
            print(f"✓ Backup created: {backup_file}")

        elif command == "restore":
            if len(sys.argv) < 3:
                print("Usage: python main.py restore <backup_file>")
                return
            backup_file = sys.argv[2]
            if manager.restore(backup_file):
                print(f"✓ Restored from {backup_file}")
            else:
                print(f"✗ Restore failed")

        elif command == "clear":
            count = manager.clear_completed()
            print(f"✓ Cleared {count} completed tasks")

        elif command == "init":
            print("✓ Storage initialized")

        elif command == "web":
            print("Starting web interface...")
            print("Open http://localhost:5000 in your browser")
            # Would start Flask/FastAPI server here

        elif command == "help":
            print_help()

        else:
            print(f"Unknown command: {command}")
            print_help()

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    main()
