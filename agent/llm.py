"""LLM Provider Integration"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMProvider:
    """Handles LLM API calls"""

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        api_key: Optional[str] = None,
    ):
        """Initialize LLM Provider
        
        Args:
            provider: LLM provider (openai, anthropic, local)
            model: Model name
            api_key: API key (uses env if not provided)
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY", "")

        if provider == "openai":
            try:
                import openai
                openai.api_key = self.api_key
            except ImportError:
                raise ImportError("openai package not installed")
        elif provider == "anthropic":
            try:
                import anthropic
            except ImportError:
                raise ImportError("anthropic package not installed")

    def call(self, prompt: str, temperature: float = 0.7) -> str:
        """Call the LLM
        
        Args:
            prompt: Prompt to send
            temperature: Response temperature (0-1)
            
        Returns:
            LLM response
        """
        try:
            if self.provider == "openai":
                return self._call_openai(prompt, temperature)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, temperature)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise

    def _call_openai(self, prompt: str, temperature: float) -> str:
        """Call OpenAI API"""
        import openai
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str, temperature: float) -> str:
        """Call Anthropic Claude API"""
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        message = client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return message.content[0].text
