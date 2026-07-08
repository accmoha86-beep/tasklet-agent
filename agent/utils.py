"""Utility Functions"""

import json
import re
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def parse_json(text: str) -> Optional[Union[Dict, List]]:
    """Parse JSON from text
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Parsed JSON or None
    """
    try:
        # Try direct parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from text
    json_pattern = r'\{.*\}|\[.*\]'
    matches = re.findall(json_pattern, text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    logger.warning(f"Could not parse JSON from: {text}")
    return None


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to max length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) > max_length:
        return text[: max_length - 3] + "..."
    return text
