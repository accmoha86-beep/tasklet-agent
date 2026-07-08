"""Example: Full Workflow with All Infrastructure"""

import os
import sys
from dotenv import load_dotenv

load_dotenv(".env.infrastructure")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core_advanced import AdvancedTaskletAgent


def main():
    """Run full workflow with infrastructure"""

    print("🔥 Tasklet Agent - Full Infrastructure Workflow")
    print("=" * 60)

    # Initialize advanced agent
    agent = AdvancedTaskletAgent(
        model="gpt-4",
        api_key=os.getenv("LLM_API_KEY"),
        provider="openai",
        debug=True,
        auto_commit=True,
        auto_save=True,
    )

    print(f"\n🤖 Agent Status:")
    status = agent.get_status()
    print(f"  ID: {status['agent_id']}")
    print(f"  Model: {status['model']}")
    print(f"  Sandbox: {status['sandbox']['status']}")
    print(f"  Auto-commit: {status['auto_commit']}")
    print(f"  Auto-save: {status['auto_save']}")

    # Task 1: Analyze data
    print(f"\n📋 Task 1: Data Analysis")
    print("-" * 60)
    task1 = "Analyze sales data and generate insights"
    result1 = agent.run(task1)
    print(f"Status: {result1['status']}")
    print(f"Task ID: {result1.get('task_id')}")
    print(f"Duration: {result1.get('duration_seconds', 'N/A'):.2f}s")

    # Task 2: Execute Python
    print(f"\n📋 Task 2: Python Execution")
    print("-" * 60)
    python_code = """
import json
data = {'status': 'success', 'message': 'Python execution works!'}
print(json.dumps(data, indent=2))
"""
    py_result = agent.execute_python(python_code)
    print(f"Python Result: {py_result}")

    # Task 3: Shell command
    print(f"\n📋 Task 3: Shell Execution")
    print("-" * 60)
    shell_result = agent.execute_shell("echo 'Sandbox working!' && date")
    print(f"Shell Result: {shell_result['stdout']}")

    # Task 4: Web search
    print(f"\n📋 Task 4: Web Search")
    print("-" * 60)
    task4 = "Search for information about AI agents"
    result4 = agent.run(task4)
    print(f"Status: {result4['status']}")

    print(f"\n✅ Workflow Complete!")
    print(f"Memory saved: storage/memory/")
    print(f"Logs saved: storage/logs/")
    print(f"All changes auto-committed to GitHub")


if __name__ == "__main__":
    main()
