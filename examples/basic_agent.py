"""
Basic Agent Example
Demonstrates running the ReAct agent with default tools and built-in MockLLM.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent import (
    Agent,
    CalculatorTool,
    SystemInfoTool,
    SearchTool,
    FileWriteTool,
    FileReadTool,
)


def main():
    # 1. Initialize Agent with tools
    agent = Agent(
        tools=[
            CalculatorTool(),
            SystemInfoTool(),
            SearchTool(),
            FileWriteTool(),
            FileReadTool(),
        ],
        verbose=True,
    )

    # 2. Run tasks
    print("\n--- Example 1: Math Calculation ---")
    agent.run("Calculate (15 * 4) + sqrt(144)")

    print("\n--- Example 2: System Info ---")
    agent.run("What is the current time and operating system?")

    print("\n--- Example 3: Search and Knowledge ---")
    agent.run("What is an AI agent?")


if __name__ == "__main__":
    main()
