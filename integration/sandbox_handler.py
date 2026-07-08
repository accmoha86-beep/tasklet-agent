"""Sandbox Handler - Manage sandbox execution"""

import os
import logging
from typing import Dict, Any
from agent.executors.python_executor import PythonExecutor, ShellExecutor, WebExecutor

logger = logging.getLogger(__name__)


class SandboxHandler:
    """Handle sandbox execution environment"""

    def __init__(self):
        self.enabled = os.getenv("SANDBOX_ENABLED", "true").lower() == "true"
        self.timeout = int(os.getenv("SANDBOX_TIMEOUT", "300"))
        self.python_executor = PythonExecutor(timeout=self.timeout)
        self.shell_executor = ShellExecutor(timeout=self.timeout)
        self.web_executor = WebExecutor()

    def execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code
        
        Args:
            code: Python code
            
        Returns:
            Execution result
        """
        if not self.enabled:
            return {"status": "disabled"}

        logger.info("Executing Python code")
        return self.python_executor.execute(code)

    def execute_shell(self, command: str) -> Dict[str, Any]:
        """Execute shell command
        
        Args:
            command: Shell command
            
        Returns:
            Execution result
        """
        if not self.enabled:
            return {"status": "disabled"}

        logger.info(f"Executing shell: {command}")
        return self.shell_executor.execute(command)

    def fetch_url(self, url: str, method: str = "GET") -> Dict[str, Any]:
        """Fetch from URL
        
        Args:
            url: URL to fetch
            method: HTTP method
            
        Returns:
            Response data
        """
        if not self.enabled:
            return {"status": "disabled"}

        logger.info(f"Fetching: {url}")
        return self.web_executor.fetch(url, method=method)

    def get_status(self) -> Dict[str, Any]:
        """Get sandbox status
        
        Returns:
            Sandbox status
        """
        return {
            "status": "enabled" if self.enabled else "disabled",
            "timeout": self.timeout,
            "python_path": os.getenv("SANDBOX_PYTHON_PATH", "/usr/bin/python3"),
            "shell_path": os.getenv("SANDBOX_SHELL_PATH", "/bin/bash"),
        }
