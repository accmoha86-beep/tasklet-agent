"""Tool System - Base Classes and Registry"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Base class for all tools"""

    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool
        
        Args:
            **kwargs: Tool-specific arguments
            
        Returns:
            Tool execution result
        """
        pass

    def __call__(self, **kwargs) -> Any:
        """Make tool callable"""
        return self.execute(**kwargs)


class ToolRegistry:
    """Registry for managing tools"""

    def __init__(self):
        """Initialize tool registry"""
        self._tools: Dict[str, BaseTool] = {}
        self._load_default_tools()

    def register(self, tool: BaseTool) -> None:
        """Register a tool
        
        Args:
            tool: Tool instance to register
        """
        if not hasattr(tool, "name"):
            raise ValueError("Tool must have a 'name' attribute")
        if not hasattr(tool, "description"):
            raise ValueError("Tool must have a 'description' attribute")

        self._tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")

    def execute(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool
        
        Args:
            tool_name: Name of tool to execute
            **kwargs: Tool arguments
            
        Returns:
            Tool result
        """
        if tool_name not in self._tools:
            raise ValueError(f"Tool not found: {tool_name}")

        tool = self._tools[tool_name]
        logger.info(f"Executing tool: {tool_name}")
        return tool.execute(**kwargs)

    def has_tool(self, tool_name: str) -> bool:
        """Check if tool exists
        
        Args:
            tool_name: Name of tool
            
        Returns:
            True if tool exists
        """
        return tool_name in self._tools

    def list_tools(self) -> List[str]:
        """List all available tools
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def get_tool_info(self, tool_name: str) -> Dict[str, str]:
        """Get tool information
        
        Args:
            tool_name: Name of tool
            
        Returns:
            Tool metadata
        """
        if tool_name not in self._tools:
            return {}

        tool = self._tools[tool_name]
        return {"name": tool.name, "description": tool.description}

    def _load_default_tools(self) -> None:
        """Load default built-in tools"""
        self.register(EchoTool())
        self.register(PrintTool())


class EchoTool(BaseTool):
    """Simple echo tool for testing"""

    name = "echo"
    description = "Echo back the input text"

    def execute(self, text: str = "", **kwargs) -> str:
        """Echo the input"""
        return f"Echo: {text}"


class PrintTool(BaseTool):
    """Print tool for logging"""

    name = "print"
    description = "Print a message"

    def execute(self, message: str = "", **kwargs) -> str:
        """Print a message"""
        print(message)
        return f"Printed: {message}"
