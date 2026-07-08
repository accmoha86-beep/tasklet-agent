"""Executor Tools - Run code in sandbox"""

import logging
from typing import Dict, Any
from agent.tools import BaseTool
from agent.executors.python_executor import PythonExecutor, ShellExecutor

logger = logging.getLogger(__name__)


class RunPythonTool(BaseTool):
    """Execute Python code"""

    name = "run_python"
    description = "Execute Python code in the sandbox"

    def __init__(self):
        self.executor = PythonExecutor()

    def execute(self, code: str, **kwargs) -> Dict[str, Any]:
        """Execute Python code
        
        Args:
            code: Python code to execute
            
        Returns:
            Execution result
        """
        logger.info("Executing Python code")
        return self.executor.execute(code)


class RunShellTool(BaseTool):
    """Execute shell commands"""

    name = "run_shell"
    description = "Execute shell commands"

    def __init__(self):
        self.executor = ShellExecutor()

    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute shell command
        
        Args:
            command: Shell command to execute
            
        Returns:
            Execution result
        """
        logger.info(f"Executing shell: {command}")
        return self.executor.execute(command)


class RunAnalysisTool(BaseTool):
    """Analyze data with Python"""

    name = "run_analysis"
    description = "Analyze data files with Python"

    def __init__(self):
        self.executor = PythonExecutor()

    def execute(self, script: str, input_file: str = None, **kwargs) -> Dict[str, Any]:
        """Run analysis script
        
        Args:
            script: Python script
            input_file: Input data file
            
        Returns:
            Analysis results
        """
        logger.info(f"Running analysis on {input_file}")
        return self.executor.execute(script)
