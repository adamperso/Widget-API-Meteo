"""Memory management for Jarvis agent."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from jarvis.utils.logger import log


class Memory:
    """
    Manages agent memory including:
    - Action history
    - Long-term context
    - Project learning
    """
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.history_file = self.memory_dir / "history.json"
        self.context_dir = self.memory_dir / "context"
        
        # Ensure directories exist
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.context_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize history
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                log("⚠️", f"Error loading history: {e}")
        return []
    
    def _save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            log("❌", f"Error saving history: {e}")
    
    def add_action(self, action_type: str, details: Dict[str, Any]):
        """Record an action in memory."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "details": details
        }
        self.history.append(entry)
        self._save_history()
        log("💾", f"Action recorded: {action_type}")
    
    def get_recent_actions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent actions from history."""
        return self.history[-limit:]
    
    def save_context(self, context_name: str, content: Any):
        """Save persistent context."""
        context_file = self.context_dir / f"{context_name}.json"
        try:
            with open(context_file, "w") as f:
                json.dump(content, f, indent=2)
            log("💾", f"Context saved: {context_name}")
        except Exception as e:
            log("❌", f"Error saving context: {e}")
    
    def load_context(self, context_name: str) -> Optional[Any]:
        """Load persistent context."""
        context_file = self.context_dir / f"{context_name}.json"
        if context_file.exists():
            try:
                with open(context_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                log("❌", f"Error loading context: {e}")
        return None
    
    def clear_history(self):
        """Clear all history."""
        self.history = []
        self._save_history()
        log("🗑️", "History cleared")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get memory summary."""
        return {
            "total_actions": len(self.history),
            "recent_actions": self.get_recent_actions(5),
            "context_files": [f.stem for f in self.context_dir.glob("*.json")]
        }
