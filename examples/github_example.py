"""GitHub Integration Example"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import TaskletAgent


def main():
    """Run GitHub integration example"""

    print("🤖 Tasklet Agent - GitHub Integration Example")
    print("=" * 50)

    # Initialize agent
    agent = TaskletAgent(
        model="gpt-4",
        api_key=os.getenv("LLM_API_KEY"),
        provider="openai",
        debug=True,
    )

    # GitHub-related task
    task = "Explain how to create a pull request on GitHub"

    print(f"\n📋 Task: {task}")
    print("-" * 50)

    # Run agent
    result = agent.run(task)

    # Display results
    print(f"\n✅ Status: {result['status']}")
    if result['status'] == 'success':
        print(f"\n📝 Response:\n{result['response']}")
    else:
        print(f"\n❌ Error: {result.get('error')}")


if __name__ == "__main__":
    main()
