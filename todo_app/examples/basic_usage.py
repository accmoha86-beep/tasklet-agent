"""Todo App - Example Usage"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from todo_app.app.core import TodoManager


def main():
    """Run example usage"""

    print("🎯 Todo App - Example Usage")
    print("=" * 60)

    # Initialize manager
    manager = TodoManager(storage_dir="./data/todos")

    # Add tasks
    print("\n📝 Adding tasks...")
    print("-" * 60)
    
    task1 = manager.add_task(
        "Learn Python",
        description="Complete Python fundamentals course",
        category="learning",
        priority="high",
        due_date="2024-01-20",
    )
    print(f"✓ Task #{task1}: Learn Python")

    task2 = manager.add_task(
        "Buy groceries",
        description="Milk, eggs, bread, vegetables",
        category="shopping",
        priority="medium",
        due_date="2024-01-15",
    )
    print(f"✓ Task #{task2}: Buy groceries")

    task3 = manager.add_task(
        "Finish project",
        description="Complete the todo app implementation",
        category="work",
        priority="urgent",
        due_date="2024-01-16",
    )
    print(f"✓ Task #{task3}: Finish project")

    task4 = manager.add_task(
        "Exercise",
        description="30 min running",
        category="health",
        priority="medium",
    )
    print(f"✓ Task #{task4}: Exercise")

    # List all tasks
    print("\n📋 All Tasks:")
    print("-" * 60)
    all_tasks = manager.get_all_tasks()
    for task in all_tasks:
        status_icon = "✓" if task["status"] == "completed" else "○"
        print(
            f"{status_icon} #{task['id']}: {task['title']} "
            f"[{task['priority']}] ({task['category']})"
        )

    # Mark complete
    print("\n✅ Marking tasks complete...")
    print("-" * 60)
    manager.mark_complete(task2)
    print(f"✓ Task #{task2} marked complete")

    # Search
    print("\n🔍 Searching for 'project'...")
    print("-" * 60)
    results = manager.search_tasks("project")
    for task in results:
        print(f"Found: #{task['id']} - {task['title']}")

    # Filter
    print("\n🏷️ Tasks with HIGH priority:")
    print("-" * 60)
    high_priority = manager.filter_tasks(priority="high")
    for task in high_priority:
        print(f"#{task['id']}: {task['title']}")

    # Statistics
    print("\n📊 Statistics:")
    print("-" * 60)
    stats = manager.get_statistics()
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Completed: {stats['completed_tasks']}")
    print(f"Pending: {stats['pending_tasks']}")
    print(f"Completion Rate: {stats['completion_rate']:.1f}%")
    print(f"\nCategories:")
    for cat, count in stats["categories"].items():
        print(f"  {cat}: {count}")
    print(f"\nPriorities:")
    for pri, count in stats["priorities"].items():
        print(f"  {pri}: {count}")

    # Overdue tasks
    print("\n⚠️ Overdue Tasks:")
    print("-" * 60)
    overdue = manager.get_overdue_tasks()
    if overdue:
        for task in overdue:
            print(f"#{task['id']}: {task['title']} (Due: {task['due_date']})")
    else:
        print("No overdue tasks!")

    # Backup
    print("\n💾 Creating backup...")
    print("-" * 60)
    backup_file = manager.backup()
    print(f"✓ Backup created: {backup_file}")

    # Export
    print("\n📤 Exporting to CSV...")
    print("-" * 60)
    if manager.export_csv("todos_export.csv"):
        print("✓ Exported to todos_export.csv")

    print("\n✅ Example complete!")


if __name__ == "__main__":
    main()
