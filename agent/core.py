import sys
import re
from typing import List, Dict, Optional, Callable
from agent.tools.base import BaseTool
from agent.memory import AgentMemory
from agent.llm import BaseLLM, MockLLM

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SYSTEM_PROMPT_TEMPLATE = """You are SmartAgent, a helpful and precise autonomous AI assistant.
Answer the user's question or solve their task using the ReAct (Reasoning + Acting) loop.

You have access to the following tools:
{tool_descriptions}

Use the following format strictly:

Question: the input question or task you must solve
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat up to {max_iterations} times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""


class Agent:
    """
    Modular Autonomous AI Agent implementing the ReAct framework.
    """

    def __init__(
        self,
        llm: Optional[BaseLLM] = None,
        tools: Optional[List[BaseTool]] = None,
        max_iterations: int = 5,
        verbose: bool = True,
    ):
        self.llm = llm or MockLLM()
        self.tools: Dict[str, BaseTool] = {tool.name: tool for tool in (tools or [])}
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.memory = AgentMemory()

    def add_tool(self, tool: BaseTool) -> None:
        """Register a new tool with the agent."""
        self.tools[tool.name] = tool

    def _build_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            f"- {name}: {tool.description}" for name, tool in self.tools.items()
        )
        tool_names = ", ".join(self.tools.keys())
        return SYSTEM_PROMPT_TEMPLATE.format(
            tool_descriptions=tool_descriptions,
            tool_names=tool_names,
            max_iterations=self.max_iterations,
        )

    def run(self, question: str) -> str:
        """
        Execute the agent loop for the given question/goal.
        """
        self.memory.clear_scratchpad()
        self.memory.add_user_message(question)

        system_prompt = self._build_system_prompt()
        iteration = 0

        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🤖 [Agent Started] Task: {question}")
            print(f"{'='*60}")

        while iteration < self.max_iterations:
            iteration += 1

            # Construct current prompt with previous scratchpad steps
            scratchpad_text = self.memory.get_scratchpad_text()
            current_prompt = f"Question: {question}\n"
            if scratchpad_text:
                current_prompt += f"{scratchpad_text}\n"

            # LLM generates next thought/action
            response = self.llm.generate(current_prompt, system_prompt=system_prompt)

            # Check if Final Answer reached
            if "Final Answer:" in response:
                final_answer = response.split("Final Answer:")[-1].strip()
                if self.verbose:
                    thought = self._extract_field(response, "Thought")
                    if thought:
                        print(f"💭 Thought: {thought}")
                    print(f"\n🎯 Final Answer:\n{final_answer}")
                self.memory.add_agent_message(final_answer)
                return final_answer

            # Parse Thought, Action, Action Input
            thought = self._extract_field(response, "Thought")
            action = self._extract_field(response, "Action")
            action_input = self._extract_field(response, "Action Input")

            if self.verbose:
                if thought:
                    print(f"💭 Thought: {thought}")
                print(f"🛠️  Action: {action}")
                print(f"📥 Action Input: {action_input}")

            # Execute Tool
            if action in self.tools:
                try:
                    tool = self.tools[action]
                    observation = str(tool.run(action_input))
                except Exception as e:
                    observation = f"Error executing {action}: {str(e)}"
            else:
                observation = f"Tool '{action}' not recognized. Available tools: {list(self.tools.keys())}"

            if self.verbose:
                print(f"👁️  Observation: {observation}")
                print("-" * 50)

            # Record step in scratchpad
            self.memory.record_step(
                thought=thought or "Proceeding with tool execution",
                action=action,
                action_input=action_input,
                observation=observation,
            )

        fallback = "Agent reached maximum iteration limit without finding a definitive answer."
        if self.verbose:
            print(f"⚠️ {fallback}")
        return fallback

    @staticmethod
    def _extract_field(text: str, field_name: str) -> str:
        pattern = rf"{field_name}:\s*(.*?)(?=\n(?:Thought|Action|Action Input|Observation|Final Answer):|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
