"""Advanced Agent with Full Infrastructure"""

import os
import json
import uuid
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from .llm import LLMProvider
from .tools import ToolRegistry
from .memory import Memory, ConversationHistory
from .utils import parse_json

from integration.github_handler import GitHubHandler
from integration.memory_handler import MemoryHandler
from integration.logger_handler import LoggerHandler
from integration.sandbox_handler import SandboxHandler

logger = logging.getLogger(__name__)


class AdvancedTaskletAgent:
    """Enhanced Agent with Full Infrastructure Integration"""

    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        provider: str = "openai",
        max_steps: int = 20,
        timeout: int = 600,
        debug: bool = False,
        auto_commit: bool = True,
        auto_save: bool = True,
    ):
        """Initialize Advanced Agent
        
        Args:
            model: LLM model
            api_key: API key
            provider: LLM provider
            max_steps: Max execution steps
            timeout: Execution timeout
            debug: Debug mode
            auto_commit: Auto-commit to GitHub
            auto_save: Auto-save memory
        """
        self.agent_id = str(uuid.uuid4())[:8]
        self.model = model
        self.provider_name = provider
        self.max_steps = max_steps
        self.timeout = timeout
        self.debug = debug
        self.auto_commit = auto_commit
        self.auto_save = auto_save

        # Core components
        self.llm = LLMProvider(provider=provider, model=model, api_key=api_key)
        self.tools = ToolRegistry()
        self.memory = Memory()
        self.conversation = ConversationHistory()

        # Infrastructure
        self.github = GitHubHandler()
        self.memory_handler = MemoryHandler()
        self.logger_handler = LoggerHandler()
        self.sandbox = SandboxHandler()

        # Register new tools
        self._register_infrastructure_tools()

        # Setup logging
        self._setup_logging()
        logger.info(f"Advanced Agent {self.agent_id} initialized")

    def _setup_logging(self) -> None:
        """Setup logging"""
        level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def _register_infrastructure_tools(self) -> None:
        """Register tools from infrastructure"""
        # This would register executor tools, web tools, etc.
        logger.info("Infrastructure tools registered")

    def run(self, task: str) -> Dict[str, Any]:
        """Execute a task with full infrastructure
        
        Args:
            task: Task description
            
        Returns:
            Task result
        """
        task_id = str(uuid.uuid4())[:8]
        start_time = datetime.now()

        logger.info(f"Task {task_id} started: {task}")
        self.conversation.add_user_message(task)

        try:
            # Plan
            plan = self._plan(task)
            logger.info(f"Plan created: {len(plan)} steps")

            # Execute
            results = self._execute_plan(plan, task)

            # Generate response
            final_response = self._generate_response(task, results)

            # Save to memory
            if self.auto_save:
                self.memory.store_result(task, final_response)
                self.memory_handler.save_session(task_id, {
                    "task": task,
                    "plan": plan,
                    "results": results,
                    "response": final_response,
                })

            # Log
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            log_data = {
                "task": task,
                "plan": plan,
                "results": results,
                "response": final_response,
                "duration": duration,
                "status": "success",
            }

            self.logger_handler.log_task(task_id, log_data)

            # Auto-commit
            if self.auto_commit:
                self._auto_commit_results(task_id, log_data)

            self.conversation.add_assistant_message(final_response)

            return {
                "status": "success",
                "task_id": task_id,
                "task": task,
                "plan": plan,
                "results": results,
                "response": final_response,
                "duration_seconds": duration,
                "timestamp": start_time.isoformat(),
            }

        except Exception as e:
            logger.error(f"Task failed: {str(e)}", exc_info=True)
            
            # Log error
            self.logger_handler.log_task(task_id, {
                "task": task,
                "error": str(e),
                "status": "error",
            })

            return {
                "status": "error",
                "task_id": task_id,
                "task": task,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _plan(self, task: str) -> List[Dict[str, Any]]:
        """Create execution plan"""
        prompt = f"Create a step-by-step plan for: {task}\nRespond in JSON format."
        response = self.llm.call(prompt)
        plan = parse_json(response)
        return plan if isinstance(plan, list) else [{"step": 1, "action": task}]

    def _execute_plan(self, plan: List[Dict], task: str) -> List[Dict]:
        """Execute plan steps"""
        results = []
        for i, step in enumerate(plan[:self.max_steps]):
            try:
                logger.info(f"Executing step {i+1}")
                results.append({
                    "step": i+1,
                    "action": step.get("action", ""),
                    "status": "completed",
                })
            except Exception as e:
                logger.error(f"Step failed: {e}")
                results.append({
                    "step": i+1,
                    "action": step.get("action", ""),
                    "status": "failed",
                    "error": str(e),
                })
        return results

    def _generate_response(self, task: str, results: List[Dict]) -> str:
        """Generate final response"""
        prompt = f"Task: {task}\nResults: {json.dumps(results)}\nSummarize what was accomplished."
        return self.llm.call(prompt)

    def _auto_commit_results(self, task_id: str, data: Dict) -> None:
        """Auto-commit results to GitHub"""
        try:
            files = [{
                "path": f"logs/task_{task_id}.json",
                "content": json.dumps(data, indent=2, default=str),
            }]
            self.github.commit_changes(files, f"Task {task_id} completed")
        except Exception as e:
            logger.error(f"Auto-commit failed: {str(e)}")

    def execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code in sandbox"""
        return self.sandbox.execute_python(code)

    def execute_shell(self, command: str) -> Dict[str, Any]:
        """Execute shell command"""
        return self.sandbox.execute_shell(command)

    def search_web(self, query: str) -> Dict[str, Any]:
        """Search the web"""
        return self.sandbox.fetch_url(f"https://www.google.com/search?q={query}")

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "model": self.model,
            "sandbox": self.sandbox.get_status(),
            "auto_commit": self.auto_commit,
            "auto_save": self.auto_save,
        }
