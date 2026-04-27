"""CLI entry point for Jarvis agent."""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.agent.loop import AgentLoop
from jarvis.llm.ollama import OllamaLLM
from jarvis.tools.registry import ToolRegistry


def main():
    parser = argparse.ArgumentParser(description="OpenJarvis - Personal AI Agent")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask Jarvis a question or give a task")
    ask_parser.add_argument("prompt", type=str, help="Your question or task for Jarvis")
    ask_parser.add_argument("--model", type=str, default="deepseek-coder", help="LLM model to use")
    
    args = parser.parse_args()
    
    if args.command == "ask":
        # Initialize components
        llm = OllamaLLM(model=args.model)
        tool_registry = ToolRegistry()
        agent = AgentLoop(llm=llm, tools=tool_registry.get_tools())
        
        # Run the agent
        response = agent.run(args.prompt)
        print(f"\n🤖 Jarvis: {response}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
