"""Agent Settings and Configuration"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
GITHUB_ORG = os.getenv("GITHUB_ORG", "")

# Agent Configuration
AGENT_MAX_STEPS = int(os.getenv("AGENT_MAX_STEPS", "10"))
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "300"))
AGENT_MEMORY_SIZE = int(os.getenv("AGENT_MEMORY_SIZE", "50"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
