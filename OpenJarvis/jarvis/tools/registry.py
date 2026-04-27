"""Tool registry - manages all available tools for the agent."""

from typing import Dict, Callable, List, Any
from jarvis.tools.file_tools import FileTools
from jarvis.tools.shell_tools import ShellTools
from jarvis.tools.search_tools import SearchTools
from jarvis.utils.logger import log


class ToolRegistry:
    """
    Central registry for all tools.
    Makes tools available to the LLM with descriptions.
    """
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all default tools."""
        
        # File tools
        self.register_tool(
            name="read_file",
            func=FileTools.read_file,
            description="Read the contents of a file",
            parameters={
                "file_path": {"type": "string", "description": "Path to the file to read"}
            }
        )
        
        self.register_tool(
            name="write_file",
            func=FileTools.write_file,
            description="Write content to a file (creates or overwrites)",
            parameters={
                "file_path": {"type": "string", "description": "Path to the file"},
                "content": {"type": "string", "description": "Content to write"},
                "overwrite": {"type": "boolean", "description": "Whether to overwrite existing file", "default": False}
            }
        )
        
        self.register_tool(
            name="list_directory",
            func=FileTools.list_directory,
            description="List files in a directory",
            parameters={
                "dir_path": {"type": "string", "description": "Path to the directory"},
                "recursive": {"type": "boolean", "description": "Whether to list recursively", "default": False}
            }
        )
        
        self.register_tool(
            name="delete_file",
            func=FileTools.delete_file,
            description="Delete a file",
            parameters={
                "file_path": {"type": "string", "description": "Path to the file to delete"}
            }
        )
        
        # Shell tools
        self.register_tool(
            name="run_command",
            func=ShellTools.run_command,
            description="Execute a shell command",
            parameters={
                "command": {"type": "string", "description": "The shell command to execute"},
                "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30},
                "cwd": {"type": "string", "description": "Working directory", "default": None}
            }
        )
        
        self.register_tool(
            name="run_python",
            func=ShellTools.run_python,
            description="Execute Python code",
            parameters={
                "code": {"type": "string", "description": "Python code to execute"},
                "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30}
            }
        )
        
        # Search tools
        self.register_tool(
            name="grep",
            func=SearchTools.grep,
            description="Search for a pattern in files (like grep)",
            parameters={
                "pattern": {"type": "string", "description": "Regex pattern to search for"},
                "path": {"type": "string", "description": "Directory to search in", "default": "."},
                "recursive": {"type": "boolean", "description": "Whether to search recursively", "default": True},
                "include_pattern": {"type": "string", "description": "File pattern to include (e.g., '*.py')", "default": None}
            }
        )
        
        self.register_tool(
            name="find_files",
            func=SearchTools.find_files,
            description="Find files matching a pattern",
            parameters={
                "pattern": {"type": "string", "description": "File pattern (e.g., '*.py')"},
                "path": {"type": "string", "description": "Directory to search in", "default": "."},
                "recursive": {"type": "boolean", "description": "Whether to search recursively", "default": True}
            }
        )
        
        log("✅", f"Registered {len(self.tools)} tools")
    
    def register_tool(self, name: str, func: Callable, description: str, 
                      parameters: Dict[str, Any] = None):
        """
        Register a new tool.
        
        Args:
            name: Tool name (used by LLM to call it)
            func: The actual function to execute
            description: Description of what the tool does
            parameters: Parameter schema for the tool
        """
        self.tools[name] = {
            "func": func,
            "description": description,
            "parameters": parameters or {}
        }
        log("🔧", f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Callable:
        """Get a tool function by name."""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        return self.tools[name]["func"]
    
    def get_tools(self) -> Dict[str, Callable]:
        """Get all tools as a simple dict of name -> function."""
        return {name: info["func"] for name, info in self.tools.items()}
    
    def get_tool_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """Get tool descriptions (for LLM context)."""
        return {
            name: {
                "description": info["description"],
                "parameters": info["parameters"]
            }
            for name, info in self.tools.items()
        }
    
    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        """Get full schema for a specific tool."""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        
        info = self.tools[name]
        return {
            "name": name,
            "description": info["description"],
            "parameters": info["parameters"]
        }
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self.tools.keys())
