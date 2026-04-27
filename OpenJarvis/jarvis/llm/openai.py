"""OpenAI API integration."""

import os
from typing import List, Dict, Any, Optional
from jarvis.llm.base import BaseLLM
from jarvis.utils.logger import log


class OpenAILLM(BaseLLM):
    """OpenAI API LLM provider."""
    
    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None):
        super().__init__(model)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            log("⚠️", "OPENAI_API_KEY not found in environment")
        
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            log("✅", f"OpenAI client initialized with model: {self.model}")
        except ImportError:
            log("❌", "OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            log("❌", f"Error initializing OpenAI client: {e}")
    
    def generate(self, messages: List[Dict[str, str]], tools: Dict[str, Any] = None) -> Any:
        """Generate response using OpenAI API."""
        if not self.client:
            return {"content": "OpenAI client not initialized. Please check your API key."}
        
        try:
            # Prepare tool definitions if provided
            tool_definitions = None
            if tools:
                tool_definitions = self._format_tools(tools)
            
            # Make API call
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
            }
            
            if tool_definitions:
                kwargs["tools"] = tool_definitions
            
            response = self.client.chat.completions.create(**kwargs)
            
            # Extract response
            choice = response.choices[0]
            message = choice.message
            
            # Check for tool calls
            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_call = message.tool_calls[0]
                return {
                    "tool_call": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
            
            return {"content": message.content}
            
        except Exception as e:
            log("❌", f"OpenAI API error: {e}")
            return {"content": f"Error: {str(e)}"}
    
    def _format_tools(self, tools: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format tools for OpenAI API."""
        tool_definitions = []
        
        for name, info in tools.items():
            if isinstance(info, dict) and "description" in info:
                tool_def = {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": info["description"],
                        "parameters": {
                            "type": "object",
                            "properties": info.get("parameters", {}),
                            "required": []
                        }
                    }
                }
                tool_definitions.append(tool_def)
        
        return tool_definitions
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available."""
        return self.client is not None and self.api_key is not None
