"""Base LLM interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLLM(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, model: str = "default"):
        self.model = model
    
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], tools: Dict[str, Any] = None) -> Any:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional dict of available tools
        
        Returns:
            LLM response (format depends on implementation)
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        pass
