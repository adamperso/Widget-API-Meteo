"""Task planner for complex task decomposition."""

from typing import List, Dict, Any
from jarvis.utils.logger import log


class Planner:
    """
    Breaks down complex tasks into executable steps.
    Example: "Create an API" → plan → code → test → fix
    """
    
    def __init__(self, llm):
        self.llm = llm
    
    def create_plan(self, task: str) -> List[Dict[str, Any]]:
        """Create a step-by-step plan for a complex task."""
        log("📋", f"Creating plan for task: {task[:100]}...")
        
        prompt = f"""You are a task planner. Break down this task into clear, executable steps.

Task: {task}

Return a JSON array of steps. Each step should have:
- "id": step number
- "description": what to do
- "expected_output": what success looks like

Example format:
[
  {{"id": 1, "description": "Analyze requirements", "expected_output": "Clear understanding"}},
  {{"id": 2, "description": "Write code", "expected_output": "Working implementation"}},
  {{"id": 3, "description": "Test the code", "expected_output": "All tests pass"}}
]

Respond with ONLY the JSON array:"""

        response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}],
            tools={}
        )
        
        # Parse the plan
        try:
            if isinstance(response, dict) and "content" in response:
                content = response["content"]
                # Extract JSON from response
                import json
                start_idx = content.find("[")
                end_idx = content.rfind("]") + 1
                if start_idx >= 0 and end_idx > start_idx:
                    plan_json = content[start_idx:end_idx]
                    plan = json.loads(plan_json)
                    log("✅", f"Plan created with {len(plan)} steps")
                    return plan
        except Exception as e:
            log("❌", f"Error parsing plan: {e}")
        
        # Fallback: single step plan
        return [{"id": 1, "description": task, "expected_output": "Task completed"}]
    
    def execute_plan(self, agent, plan: List[Dict[str, Any]]) -> str:
        """Execute a plan step by step."""
        results = []
        
        for step in plan:
            log("🎯", f"Executing step {step['id']}: {step['description']}")
            
            # Execute each step through the agent
            result = agent.run(step["description"])
            results.append({
                "step_id": step["id"],
                "result": result,
                "success": True
            })
            
            log("✅", f"Step {step['id']} completed")
        
        return f"Plan executed successfully. {len(plan)} steps completed."
