"""Tool call parser utility."""

import json
import re
from typing import Dict, Any, Optional, Tuple


class ToolCallParser:
    """Parse tool calls from LLM responses."""
    
    @staticmethod
    def parse_tool_call(text: str) -> Optional[Dict[str, Any]]:
        """
        Parse a tool call from text.
        
        Expected formats:
        - JSON: {"tool": "name", "args": {...}}
        - XML: <tool name="...">args</tool>
        - Markdown: ```tool:name\n{args}\n```
        """
        # Try JSON format first
        try:
            # Look for JSON object in the text
            json_match = re.search(r'\{[^{}]*"tool"[^{}]*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "name": data.get("tool") or data.get("name"),
                    "arguments": data.get("args") or data.get("arguments", {})
                }
        except json.JSONDecodeError:
            pass
        
        # Try XML format
        xml_match = re.search(r'<tool\s+name=["\']([^"\']+)["\']>(.*?)</tool>', text, re.DOTALL)
        if xml_match:
            try:
                args = json.loads(xml_match.group(2).strip())
                return {"name": xml_match.group(1), "arguments": args}
            except json.JSONDecodeError:
                return {"name": xml_match.group(1), "arguments": xml_match.group(2).strip()}
        
        # Try Markdown code block format
        md_match = re.search(r'```tool:(\w+)\n(.*?)\n```', text, re.DOTALL)
        if md_match:
            try:
                args = json.loads(md_match.group(2).strip())
                return {"name": md_match.group(1), "arguments": args}
            except json.JSONDecodeError:
                return {"name": md_match.group(1), "arguments": md_match.group(2).strip()}
        
        return None
    
    @staticmethod
    def extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON object from text."""
        try:
            # Find JSON between braces
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        return None
    
    @staticmethod
    def is_tool_response(text: str) -> bool:
        """Check if text contains a tool call."""
        indicators = [
            '"tool"',
            '"function_call"',
            '<tool',
            '```tool:',
            'TOOL_CALL',
            '[TOOL]'
        ]
        
        return any(indicator in text for indicator in indicators)
    
    @staticmethod
    def format_tool_result(tool_name: str, result: Any) -> str:
        """Format a tool result for the LLM."""
        return f"Tool '{tool_name}' executed successfully.\nResult: {result}"
    
    @staticmethod
    def format_tool_error(tool_name: str, error: str) -> str:
        """Format a tool error for the LLM."""
        return f"Tool '{tool_name}' failed.\nError: {error}"
