"""Test Agent"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import TaskletAgent


def test_agent_initialization():
    """Test agent initialization"""
    agent = TaskletAgent(model="gpt-4", debug=True)
    assert agent is not None
    assert agent.model == "gpt-4"


def test_memory_storage():
    """Test memory storage"""
    agent = TaskletAgent()
    agent.memory.store_fact("test_key", "test_value")
    assert agent.memory.recall_fact("test_key") == "test_value"


def test_clear_memory():
    """Test memory clearing"""
    agent = TaskletAgent()
    agent.memory.store_fact("test", "value")
    agent.clear_memory()
    assert agent.memory.recall_fact("test") is None


def test_tool_registration():
    """Test tool registration"""
    agent = TaskletAgent()
    tools = agent.tools.list_tools()
    assert "echo" in tools
    assert "print" in tools
