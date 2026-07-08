"""File System Tools"""

import os
import logging
from agent.tools import BaseTool

logger = logging.getLogger(__name__)


class CreateFileTool(BaseTool):
    """Create a new file"""

    name = "create_file"
    description = "Create a new file with given content"

    def execute(self, path: str, content: str = "", **kwargs) -> dict:
        """Create a file"""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            logger.info(f"File created: {path}")
            return {"status": "success", "path": path, "size": len(content)}
        except Exception as e:
            logger.error(f"Failed to create file: {str(e)}")
            return {"status": "error", "error": str(e)}


class ReadFileTool(BaseTool):
    """Read a file"""

    name = "read_file"
    description = "Read content from a file"

    def execute(self, path: str, **kwargs) -> dict:
        """Read a file"""
        try:
            with open(path, "r") as f:
                content = f.read()
            logger.info(f"File read: {path}")
            return {"status": "success", "content": content, "size": len(content)}
        except Exception as e:
            logger.error(f"Failed to read file: {str(e)}")
            return {"status": "error", "error": str(e)}


class DeleteFileTool(BaseTool):
    """Delete a file"""

    name = "delete_file"
    description = "Delete a file"

    def execute(self, path: str, **kwargs) -> dict:
        """Delete a file"""
        try:
            os.remove(path)
            logger.info(f"File deleted: {path}")
            return {"status": "success", "path": path}
        except Exception as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return {"status": "error", "error": str(e)}


class ListDirectoryTool(BaseTool):
    """List files in a directory"""

    name = "list_directory"
    description = "List files in a directory"

    def execute(self, path: str = ".", **kwargs) -> dict:
        """List directory contents"""
        try:
            items = os.listdir(path)
            logger.info(f"Directory listed: {path}")
            return {"status": "success", "path": path, "items": items}
        except Exception as e:
            logger.error(f"Failed to list directory: {str(e)}")
            return {"status": "error", "error": str(e)}
