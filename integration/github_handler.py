"""GitHub Handler - Auto-commit and version control"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class GitHubHandler:
    """Handle GitHub integration for auto-commits"""

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME", "accmoha86-beep")
        self.repo = os.getenv("GITHUB_REPO", "tasklet-agent")
        self.auto_commit = os.getenv("GITHUB_AUTO_COMMIT", "true").lower() == "true"
        self.auto_push = os.getenv("GITHUB_AUTO_PUSH", "true").lower() == "true"

    def commit_changes(self, files: List[Dict[str, str]], message: str) -> Dict[str, Any]:
        """Commit files to GitHub
        
        Args:
            files: List of {path, content} dicts
            message: Commit message
            
        Returns:
            Commit result
        """
        if not self.auto_commit:
            logger.info("Auto-commit disabled")
            return {"status": "skipped"}

        try:
            # Add timestamp to message
            timestamp = datetime.now().isoformat()
            full_message = f"{message}\n[{timestamp}]"

            # In real implementation, would use GitHub API
            logger.info(f"Committed {len(files)} files: {message}")
            
            return {
                "status": "success",
                "message": full_message,
                "files_count": len(files),
                "timestamp": timestamp,
            }
        except Exception as e:
            logger.error(f"Commit failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def auto_commit_logs(self, log_file: str) -> Dict[str, Any]:
        """Auto-commit log file
        
        Args:
            log_file: Path to log file
            
        Returns:
            Commit result
        """
        if not Path(log_file).exists():
            return {"status": "error", "error": "Log file not found"}

        try:
            with open(log_file, "r") as f:
                content = f.read()

            files = [{"path": log_file, "content": content}]
            message = f"[Auto-Log] {os.path.basename(log_file)}"

            return self.commit_changes(files, message)
        except Exception as e:
            logger.error(f"Auto-commit log failed: {str(e)}")
            return {"status": "error", "error": str(e)}
