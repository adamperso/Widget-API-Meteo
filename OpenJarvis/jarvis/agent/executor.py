"""Tool executor - intermediary between LLM and tools."""

from typing import Dict, Any, Callable
from jarvis.utils.logger import log


class Executor:
    """
    Executes tools with safety checks and validation.
    Acts as intermediary between LLM and actual tool execution.
    """
    
    def __init__(self, tools: Dict[str, Callable], allowed_commands: list = None):
        self.tools = tools
        self.allowed_commands = allowed_commands or []
        self.execution_log = []
    
    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool with validation."""
        log("⚙️", f"Executor: Running tool '{tool_name}'")
        
        # Validate tool exists
        if tool_name not in self.tools:
            error_msg = f"Unknown tool: {tool_name}"
            log("❌", error_msg)
            raise ValueError(error_msg)
        
        # Security check for shell commands
        if tool_name == "run_command":
            command = arguments.get("command", "")
            if not self._is_command_allowed(command):
                error_msg = f"Command not allowed: {command}"
                log("🔒", error_msg)
                raise PermissionError(error_msg)
        
        # Execute the tool
        try:
            tool_func = self.tools[tool_name]
            result = tool_func(**arguments)
            
            # Log execution
            self.execution_log.append({
                "tool": tool_name,
                "arguments": arguments,
                "success": True,
                "result_preview": str(result)[:100]
            })
            
            log("✅", f"Tool '{tool_name}' executed successfully")
            return result
            
        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            log("❌", error_msg)
            
            # Log failure
            self.execution_log.append({
                "tool": tool_name,
                "arguments": arguments,
                "success": False,
                "error": str(e)
            })
            
            raise
    
    def _is_command_allowed(self, command: str) -> bool:
        """Check if a shell command is in the allowed list."""
        if not self.allowed_commands:
            return True  # No restrictions
        
        # Extract base command
        base_cmd = command.split()[0] if command else ""
        
        return base_cmd in self.allowed_commands
    
    def get_execution_history(self) -> list:
        """Get history of tool executions."""
        return self.execution_log
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_log = []
