import sys
import argparse

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from agent import (
    Agent,
    CalculatorTool,
    FileReadTool,
    FileWriteTool,
    SystemInfoTool,
    SearchTool,
)

BANNER = r"""
  ____                       _        _                    _   
 / ___| _ __ ___   __ _ _ __| |_     / \   __ _  ___ _ __ | |_ 
 \___ \| '_ ` _ \ / _` | '__| __|   / _ \ / _` |/ _ \ '_ \| __|
  ___) | | | | | | (_| | |  | |_   / ___ \ (_| |  __/ | | | |_ 
 |____/|_| |_| |_|\__,_|_|   \__| /_/   \_\__, |\___|_| |_|\__|
                                          |___/                
       ⚡ Autonomous ReAct AI Agent Framework in Python ⚡
"""


def create_default_agent(verbose: bool = True) -> Agent:
    tools = [
        CalculatorTool(),
        FileReadTool(),
        FileWriteTool(),
        SystemInfoTool(),
        SearchTool(),
    ]
    return Agent(tools=tools, verbose=verbose)


def interactive_mode(agent: Agent):
    print(BANNER)
    print("Welcome to SmartAgent Interactive CLI!")
    print("Type your task/question below (or 'exit' / 'quit' to leave).\n")
    print("Sample commands you can try:")
    print("  - 'Calculate (25 * 4) + sqrt(144)'")
    print("  - 'What is the current time and OS?'")
    print("  - 'What is an AI agent?'")
    print("  - 'Write a note to summary.txt'\n")

    while True:
        try:
            user_input = input("SmartAgent > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("\nGoodbye! Have a great day!")
                break
            agent.run(user_input)
            print()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(description="SmartAgent - Autonomous ReAct AI Agent")
    parser.add_argument("--task", type=str, help="Single task to run directly")
    parser.add_argument("--quiet", action="store_true", help="Disable verbose reasoning trace")
    args = parser.parse_args()

    agent = create_default_agent(verbose=not args.quiet)

    if args.task:
        answer = agent.run(args.task)
        if args.quiet:
            print(answer)
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
