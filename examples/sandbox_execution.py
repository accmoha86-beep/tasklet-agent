"""Example: Sandbox Execution Demo"""

import os
import sys
from dotenv import load_dotenv

load_dotenv(".env.infrastructure")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integration.sandbox_handler import SandboxHandler
from integration.logger_handler import LoggerHandler


def main():
    """Demonstrate sandbox capabilities"""

    print("🔋 Sandbox Execution Demo")
    print("=" * 60)

    sandbox = SandboxHandler()
    logger_handler = LoggerHandler()

    # Show sandbox status
    print(f"\n🔍 Sandbox Status:")
    status = sandbox.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Python execution
    print(f"\n👀 Executing Python Code:")
    print("-" * 60)
    python_code = """
import sys
import json
from datetime import datetime

result = {
    'status': 'success',
    'message': 'Python execution works!',
    'timestamp': str(datetime.now()),
    'python_version': sys.version,
}
print(json.dumps(result, indent=2))
"""
    py_result = sandbox.execute_python(python_code)
    print(f"Return code: {py_result['returncode']}")
    print(f"Output: {py_result['stdout']}")
    if py_result['stderr']:
        print(f"Errors: {py_result['stderr']}")

    # Shell execution
    print(f"\n👀 Executing Shell Commands:")
    print("-" * 60)
    shell_result = sandbox.execute_shell(
        "echo 'System Info:' && uname -a && echo '\nMemory:' && free -h"
    )
    print(f"Output:\n{shell_result['stdout']}")

    # Web fetch
    print(f"\n👀 Fetching Web Content:")
    print("-" * 60)
    web_result = sandbox.fetch_url("https://api.github.com")
    print(f"Status code: {web_result['status_code']}")
    print(f"Content (first 500 chars): {web_result['content'][:500]}")

    # Log results
    print(f"\n📋 Logging Results:")
    print("-" * 60)
    log_result = logger_handler.log_execution("sandbox_demo", {
        "python": py_result,
        "shell": shell_result,
        "web": {"status": web_result['status']},
    })
    print(f"Logged to: {log_result['file']}")

    print(f"\n✅ Demo Complete!")


if __name__ == "__main__":
    main()
