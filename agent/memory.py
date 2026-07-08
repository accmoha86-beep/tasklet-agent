"""Memory and Context Management"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import deque


class ConversationHistory:
    """Manages conversation history"""

    def __init__(self, max_messages: int = 50):
        """Initialize conversation history
        
        Args:
            max_messages: Maximum messages to keep
        """
        self.messages = deque(maxlen=max_messages)

    def add_user_message(self, content: str) -> None:
        """Add user message
        
        Args:
            content: Message content
        """
        self.messages.append(
            {"role": "user", "content": content, "timestamp": datetime.now()}
        )

    def add_assistant_message(self, content: str) -> None:
        """Add assistant message
        
        Args:
            content: Message content
        """
        self.messages.append(
            {"role": "assistant", "content": content, "timestamp": datetime.now()}
        )

    def get_context(self, last_n: int = 10) -> str:
        """Get conversation context
        
        Args:
            last_n: Number of recent messages to include
            
        Returns:
            Formatted conversation context
        """
        recent = list(self.messages)[-last_n:]
        context = ""
        for msg in recent:
            role = msg["role"].upper()
            content = msg["content"]
            context += f"{role}: {content}\n"
        return context

    def clear(self) -> None:
        """Clear conversation history"""
        self.messages.clear()

    def to_dict(self) -> List[Dict[str, Any]]:
        """Export as dictionary
        
        Returns:
            List of messages
        """
        return [
            {
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["timestamp"].isoformat(),
            }
            for msg in self.messages
        ]


class Memory:
    """Long-term memory for agent"""

    def __init__(self):
        """Initialize memory"""
        self.tasks = {}  # Completed tasks
        self.tool_results = deque(maxlen=100)  # Recent tool results
        self.facts = {}  # Learned facts

    def store_result(self, task: str, result: Any) -> None:
        """Store task result
        
        Args:
            task: Task description
            result: Task result
        """
        self.tasks[task] = {
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }

    def store_tool_result(self, tool_name: str, result: Any) -> None:
        """Store tool execution result
        
        Args:
            tool_name: Tool name
            result: Tool result
        """
        self.tool_results.append(
            {
                "tool": tool_name,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def store_fact(self, key: str, value: Any) -> None:
        """Store a learned fact
        
        Args:
            key: Fact key
            value: Fact value
        """
        self.facts[key] = {"value": value, "timestamp": datetime.now().isoformat()}

    def recall_task(self, task: str) -> Optional[Any]:
        """Recall a task result
        
        Args:
            task: Task description
            
        Returns:
            Task result or None
        """
        return self.tasks.get(task)

    def recall_fact(self, key: str) -> Optional[Any]:
        """Recall a fact
        
        Args:
            key: Fact key
            
        Returns:
            Fact value or None
        """
        if key in self.facts:
            return self.facts[key]["value"]
        return None

    def get_all(self) -> Dict[str, Any]:
        """Get all memory contents
        
        Returns:
            Memory contents
        """
        return {
            "tasks": self.tasks,
            "tool_results": list(self.tool_results),
            "facts": self.facts,
        }

    def clear(self) -> None:
        """Clear all memory"""
        self.tasks.clear()
        self.tool_results.clear()
        self.facts.clear()
