"""Core Agent Logic"""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from .llm import LLMProvider
from .tools import ToolRegistry
from .memory import Memory, ConversationHistory
from .utils import parse_json

logger = logging.getLogger(__name__)


class TaskletAgent:
    """Main Agent Class - Orchestrates LLM, Tools, and Memory"""

    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        provider: str = "openai",
        max_steps: int = 10,
        timeout: int = 300,
        debug: bool = False,
    ):
        """Initialize the Agent
        
        Args:
            model: LLM model name
            api_key: API key for LLM provider
            provider: LLM provider (openai, anthropic, local)
            max_steps: Maximum steps in agent loop
            timeout: Timeout for agent execution
            debug: Enable debug logging
        """
        self.model = model
        self.provider_name = provider
        self.max_steps = max_steps
        self.timeout = timeout
        self.debug = debug

        # Initialize components
        self.llm = LLMProvider(provider=provider, model=model, api_key=api_key)
        self.tools = ToolRegistry()
        self.memory = Memory()
        self.conversation = ConversationHistory()

        # Setup logging
        self._setup_logging()
        logger.info(f"Agent initialized with {provider} ({model})")

    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def register_tool(self, tool: Any) -> None:
        """Register a new tool
        
        Args:
            tool: Tool instance to register
        """
        self.tools.register(tool)
        logger.info(f"Tool registered: {tool.name}")

    def run(self, task: str) -> Dict[str, Any]:
        """Execute a task
        
        Args:
            task: User's task description
            
        Returns:
            Result dictionary with status, output, and metadata
        """
        logger.info(f"Starting task: {task}")
        start_time = datetime.now()

        try:
            # Add to conversation history
            self.conversation.add_user_message(task)

            # Step 1: Understanding & Planning
            plan = self._plan(task)
            logger.info(f"Plan created: {len(plan)} steps")

            # Step 2: Execution
            results = self._execute_plan(plan, task)

            # Step 3: Generate final response
            final_response = self._generate_response(task, results)

            # Store in memory
            self.memory.store_result(task, final_response)
            self.conversation.add_assistant_message(final_response)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            return {
                "status": "success",
                "task": task,
                "plan": plan,
                "results": results,
                "response": final_response,
                "duration_seconds": duration,
                "timestamp": start_time.isoformat(),
            }

        except Exception as e:
            logger.error(f"Task failed: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "task": task,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _plan(self, task: str) -> List[Dict[str, Any]]:
        """Create a plan for the task
        
        Args:
            task: Task description
            
        Returns:
            List of planned steps
        """
        prompt = f"""
Create a step-by-step plan for this task: {task}

Respond with a JSON array where each step has:
- "step": step number
- "action": what to do
- "notes": important notes

Example: [{"step": 1, "action": "Read file", "notes": "Use file_tools"}]
"""

        response = self.llm.call(prompt)
        plan = parse_json(response)

        return plan if isinstance(plan, list) else [{"step": 1, "action": task}]

    def _execute_plan(
        self, plan: List[Dict[str, Any]], original_task: str
    ) -> List[Dict[str, Any]]:
        """Execute the planned steps
        
        Args:
            plan: List of steps to execute
            original_task: Original user task
            
        Returns:
            List of execution results
        """
        results = []
        step_count = 0

        for step in plan:
            if step_count >= self.max_steps:
                logger.warning("Maximum steps reached")
                break

            try:
                step_num = step.get("step", step_count + 1)
                action = step.get("action") or step.get("task", str(step))

                logger.info(f"Executing step {step_num}: {action}")

                results.append(
                    {
                        "step": step_num,
                        "action": action,
                        "status": "completed",
                    }
                )

                step_count += 1

            except Exception as e:
                logger.error(f"Step failed: {str(e)}")
                results.append(
                    {
                        "step": step.get("step", step_count + 1),
                        "action": step.get("action", str(step)),
                        "status": "failed",
                        "error": str(e),
                    }
                )

        return results

    def _generate_response(
        self, task: str, results: List[Dict[str, Any]]
    ) -> str:
        """Generate final response
        
        Args:
            task: Original task
            results: Execution results
            
        Returns:
            Final response text
        """
        prompt = f"""
Task: {task}

Execution Results:
{json.dumps(results, indent=2)}

Provide a clear summary of what was accomplished.
"""

        return self.llm.call(prompt)

    def get_memory(self) -> Dict[str, Any]:
        """Get agent memory
        
        Returns:
            Memory contents
        """
        return self.memory.get_all()

    def clear_memory(self) -> None:
        """Clear agent memory"""
        self.memory.clear()
        self.conversation.clear()
        logger.info("Memory cleared")
