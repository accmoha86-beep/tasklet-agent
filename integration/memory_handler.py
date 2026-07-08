"""Memory Handler - File-based persistent memory"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MemoryHandler:
    """Handle persistent file-based memory"""

    def __init__(self):
        self.memory_path = Path(os.getenv("STORAGE_MEMORY_PATH", "./storage/memory"))
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.enabled = os.getenv("MEMORY_ENABLED", "true").lower() == "true"
        self.auto_save = os.getenv("MEMORY_AUTO_SAVE", "true").lower() == "true"

    def save_session(self, session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save session data
        
        Args:
            session_id: Session ID
            data: Session data
            
        Returns:
            Save result
        """
        if not self.enabled:
            logger.debug("Memory disabled")
            return {"status": "disabled"}

        try:
            session_file = self.memory_path / f"{session_id}.json"
            
            # Add timestamp
            data["_saved_at"] = datetime.now().isoformat()
            data["_session_id"] = session_id

            with open(session_file, "w") as f:
                json.dump(data, f, indent=2, default=str)

            logger.info(f"Session saved: {session_id}")
            return {"status": "success", "file": str(session_file)}
        except Exception as e:
            logger.error(f"Session save failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def load_session(self, session_id: str) -> Dict[str, Any]:
        """Load session data
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data
        """
        try:
            session_file = self.memory_path / f"{session_id}.json"
            
            if not session_file.exists():
                return {"status": "not_found"}

            with open(session_file, "r") as f:
                data = json.load(f)

            logger.info(f"Session loaded: {session_id}")
            return {"status": "success", "data": data}
        except Exception as e:
            logger.error(f"Session load failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def save_fact(self, key: str, value: Any) -> Dict[str, Any]:
        """Save a fact to memory
        
        Args:
            key: Fact key
            value: Fact value
            
        Returns:
            Save result
        """
        try:
            facts_file = self.memory_path / "facts.json"
            
            facts = {}
            if facts_file.exists():
                with open(facts_file, "r") as f:
                    facts = json.load(f)

            facts[key] = {
                "value": value,
                "saved_at": datetime.now().isoformat()
            }

            with open(facts_file, "w") as f:
                json.dump(facts, f, indent=2, default=str)

            logger.info(f"Fact saved: {key}")
            return {"status": "success", "key": key}
        except Exception as e:
            logger.error(f"Fact save failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def load_facts(self) -> Dict[str, Any]:
        """Load all facts
        
        Returns:
            All facts
        """
        try:
            facts_file = self.memory_path / "facts.json"
            
            if not facts_file.exists():
                return {"status": "success", "facts": {}}

            with open(facts_file, "r") as f:
                facts = json.load(f)

            logger.info(f"Loaded {len(facts)} facts")
            return {"status": "success", "facts": facts}
        except Exception as e:
            logger.error(f"Facts load failed: {str(e)}")
            return {"status": "error", "error": str(e)}
