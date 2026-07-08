"""Sandbox Executor - Execute Python code safely"""

import subprocess
import json
import logging
import tempfile
import os
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class PythonExecutor:
    """Execute Python code in sandbox"""

    def __init__(self, timeout: int = 300, memory_limit: int = 2048):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.python_path = os.getenv("SANDBOX_PYTHON_PATH", "/usr/bin/python3")

    def execute(self, code: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute Python code
        
        Args:
            code: Python code to execute
            variables: Variables to pass to code
            
        Returns:
            Execution result
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                temp_file = f.name

            # Execute
            result = subprocess.run(
                [self.python_path, temp_file],
                capture_output=True,
                timeout=self.timeout,
                text=True,
            )

            # Cleanup
            os.unlink(temp_file)

            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            logger.error("Python execution timeout")
            return {"status": "timeout", "error": "Execution exceeded timeout"}
        except Exception as e:
            logger.error(f"Python execution error: {str(e)}")
            return {"status": "error", "error": str(e)}


class ShellExecutor:
    """Execute shell commands"""

    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.shell_path = os.getenv("SANDBOX_SHELL_PATH", "/bin/bash")

    def execute(self, command: str) -> Dict[str, Any]:
        """Execute shell command
        
        Args:
            command: Shell command to execute
            
        Returns:
            Execution result
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=self.timeout,
                text=True,
            )

            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            logger.error("Shell execution timeout")
            return {"status": "timeout", "error": "Command exceeded timeout"}
        except Exception as e:
            logger.error(f"Shell execution error: {str(e)}")
            return {"status": "error", "error": str(e)}


class WebExecutor:
    """Execute web requests"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        try:
            import requests
            self.requests = requests
        except ImportError:
            logger.warning("requests library not installed")
            self.requests = None

    def fetch(self, url: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Fetch from URL
        
        Args:
            url: URL to fetch
            method: HTTP method
            **kwargs: Additional arguments
            
        Returns:
            Response data
        """
        if not self.requests:
            return {"status": "error", "error": "requests library not available"}

        try:
            response = self.requests.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
            return {
                "status": "success",
                "status_code": response.status_code,
                "content": response.text[:5000],  # Limit to 5KB
                "headers": dict(response.headers),
            }
        except Exception as e:
            logger.error(f"Web fetch error: {str(e)}")
            return {"status": "error", "error": str(e)}
