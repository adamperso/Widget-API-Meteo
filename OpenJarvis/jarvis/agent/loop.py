"""Agent loop - the brain of Jarvis."""

import json
from typing import Any, Dict, List, Optional
from jarvis.utils.logger import log


class AgentLoop:
    """
    Main agent loop that:
    1. Sends prompt to LLM
    2. Analyzes response
    3. Detects tool calls
    4. Executes tools
    5. Returns result to LLM
    6. Loops until final answer
    """
    
    def __init__(self, llm, tools: Dict[str, callable], max_iterations: int = 10):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations
        self.conversation_history: List[Dict[str, str]] = []
    
    def run(self, user_prompt: str) -> str:
        """Execute the agent loop for a given prompt."""
        log("🚀", f"Starting agent loop with prompt: {user_prompt[:100]}...")
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_prompt
        })
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            log("🔄", f"Iteration {iteration}/{self.max_iterations}")
            
            # Get LLM response
            response = self.llm.generate(
                messages=self.conversation_history,
                tools=self.tools
            )
            
            # Check if response contains tool call
            if self._is_tool_call(response):
                tool_result = self._execute_tool_call(response)
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "assistant",
                    "content": f"Tool executed. Result: {tool_result}"
                })
                
                log("✅", f"Tool executed successfully")
            else:
                # Final response found
                log("✨", "Final response received")
                return response.get("content", str(response))
        
        log("⚠️", "Max iterations reached")
        return "I reached the maximum number of iterations. Please try a simpler task."
    
    def _is_tool_call(self, response: Any) -> bool:
        """Check if the LLM response is a tool call."""
        if isinstance(response, dict):
            return "tool_call" in response or "function_call" in response
        return False
    
    def _execute_tool_call(self, response: Any) -> str:
        """Execute a tool call from LLM response."""
        tool_name = None
        tool_args = {}
        
        if isinstance(response, dict):
            if "tool_call" in response:
                tool_name = response["tool_call"].get("name")
                tool_args = response["tool_call"].get("arguments", {})
            elif "function_call" in response:
                tool_name = response["function_call"].get("name")
                tool_args = json.loads(response["function_call"].get("arguments", "{}"))
        
        if not tool_name or tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        log("🔧", f"Executing tool: {tool_name}")
        
        # Execute the tool
        tool_func = self.tools[tool_name]
        result = tool_func(**tool_args)
        
        return str(result)
