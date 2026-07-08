"""Logger Handler - Comprehensive audit logging"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class LoggerHandler:
    """Handle comprehensive logging to files and markdown"""

    def __init__(self):
        self.logs_path = Path(os.getenv("STORAGE_LOGS_PATH", "./storage/logs"))
        self.logs_path.mkdir(parents=True, exist_ok=True)
        self.level = os.getenv("LOGGING_LEVEL", "DEBUG")
        self.auto_commit = os.getenv("LOGGING_AUTO_COMMIT", "true").lower() == "true"
        self.to_markdown = os.getenv("LOGGING_TO_MARKDOWN", "true").lower() == "true"

    def log_task(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log a task execution
        
        Args:
            task_id: Task ID
            task_data: Task data
            
        Returns:
            Log result
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # JSON log
            json_file = self.logs_path / f"task_{task_id}.json"
            with open(json_file, "w") as f:
                json.dump({
                    "task_id": task_id,
                    "timestamp": timestamp,
                    **task_data
                }, f, indent=2, default=str)

            # Markdown log
            if self.to_markdown:
                md_file = self.logs_path / f"task_{task_id}.md"
                self._write_markdown_log(md_file, task_id, task_data, timestamp)

            logger.info(f"Task logged: {task_id}")
            return {
                "status": "success",
                "json_file": str(json_file),
                "markdown_file": str(md_file) if self.to_markdown else None,
            }
        except Exception as e:
            logger.error(f"Task log failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _write_markdown_log(self, file_path: Path, task_id: str, task_data: Dict, timestamp: str):
        """Write markdown log"""
        content = f"""# Task: {task_id}

**Timestamp:** {timestamp}

## Status

{task_data.get('status', 'Unknown')}

## Details

"""
        
        if "plan" in task_data:
            content += f"### Plan\n\n```json\n{json.dumps(task_data['plan'], indent=2)}\n```\n\n"
        
        if "results" in task_data:
            content += f"### Results\n\n```json\n{json.dumps(task_data['results'], indent=2)}\n```\n\n"
        
        if "error" in task_data:
            content += f"### Error\n\n{task_data['error']}\n\n"

        with open(file_path, "w") as f:
            f.write(content)

    def log_execution(self, execution_id: str, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log code execution
        
        Args:
            execution_id: Execution ID
            execution_data: Execution data
            
        Returns:
            Log result
        """
        try:
            exec_file = self.logs_path / f"execution_{execution_id}.json"
            
            with open(exec_file, "w") as f:
                json.dump({
                    "execution_id": execution_id,
                    "timestamp": datetime.now().isoformat(),
                    **execution_data
                }, f, indent=2, default=str)

            logger.info(f"Execution logged: {execution_id}")
            return {"status": "success", "file": str(exec_file)}
        except Exception as e:
            logger.error(f"Execution log failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def get_recent_logs(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent logs
        
        Args:
            limit: Number of logs to retrieve
            
        Returns:
            Recent logs
        """
        try:
            files = sorted(
                self.logs_path.glob("*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:limit]

            logs = []
            for f in files:
                with open(f, "r") as file:
                    logs.append(json.load(file))

            return {"status": "success", "count": len(logs), "logs": logs}
        except Exception as e:
            logger.error(f"Get logs failed: {str(e)}")
            return {"status": "error", "error": str(e)}
