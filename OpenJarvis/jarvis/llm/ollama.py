"""Ollama local LLM integration."""

import os
import requests
import json
from typing import List, Dict, Any, Optional
from jarvis.llm.base import BaseLLM
from jarvis.utils.logger import log


class OllamaLLM(BaseLLM):
    """Ollama local LLM provider."""
    
    def __init__(self, model: str = "deepseek-coder", host: Optional[str] = None):
        super().__init__(model)
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.base_url = f"{self.host}/api"
        log("✅", f"Ollama initialized with model: {self.model} at {self.host}")
    
    def generate(self, messages: List[Dict[str, str]], tools: Dict[str, Any] = None) -> Any:
        """Generate response using Ollama API."""
        try:
            # Format messages for Ollama
            formatted_messages = self._format_messages(messages)
            
            # Prepare request
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "stream": False,
                "options": {
                    "temperature": 0.7
                }
            }
            
            # Add tool definitions if provided
            if tools:
                payload["tools"] = self._format_tools(tools)
            
            # Make API call
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                log("❌", error_msg)
                return {"content": error_msg}
            
            result = response.json()
            
            # Extract response
            message = result.get("message", {})
            content = message.get("content", "")
            
            # Check for tool calls
            if "tool_calls" in message:
                tool_call = message["tool_calls"][0]
                return {
                    "tool_call": {
                        "name": tool_call.get("function", {}).get("name"),
                        "arguments": json.dumps(tool_call.get("function", {}).get("arguments", {}))
                    }
                }
            
            return {"content": content}
            
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to Ollama. Is it running? (ollama serve)"
            log("❌", error_msg)
            return {"content": error_msg}
        except requests.exceptions.Timeout:
            error_msg = "Ollama request timed out"
            log("❌", error_msg)
            return {"content": error_msg}
        except Exception as e:
            error_msg = f"Ollama error: {str(e)}"
            log("❌", error_msg)
            return {"content": error_msg}
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Format messages for Ollama API."""
        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        return formatted
    
    def _format_tools(self, tools: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format tools for Ollama API."""
        tool_definitions = []
        
        for name, info in tools.items():
            if isinstance(info, dict) and "description" in info:
                tool_def = {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": info["description"],
                        "parameters": info.get("parameters", {})
                    }
                }
                tool_definitions.append(tool_def)
        
        return tool_definitions
    
    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List available Ollama models."""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except:
            pass
        return []
    
    def pull_model(self, model_name: str):
        """Pull a model from Ollama library."""
        log("📥", f"Pulling model: {model_name}")
        
        try:
            response = requests.post(
                f"{self.base_url}/pull",
                json={"name": model_name, "stream": False},
                timeout=300
            )
            
            if response.status_code == 200:
                log("✅", f"Model pulled: {model_name}")
                return True
            else:
                log("❌", f"Failed to pull model: {response.text}")
                return False
                
        except Exception as e:
            log("❌", f"Error pulling model: {e}")
            return False
