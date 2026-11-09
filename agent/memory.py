from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Step:
    thought: str
    action: str
    action_input: str
    observation: str


class AgentMemory:
    """Stores conversation turns, scratchpad reasoning steps, and agent state."""

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []
        self.scratchpad: List[Step] = []

    def add_user_message(self, message: str) -> None:
        self.history.append({"role": "user", "content": message})
        self._trim()

    def add_agent_message(self, message: str) -> None:
        self.history.append({"role": "assistant", "content": message})
        self._trim()

    def record_step(self, thought: str, action: str, action_input: str, observation: str) -> None:
        self.scratchpad.append(Step(thought, action, action_input, observation))

    def clear_scratchpad(self) -> None:
        self.scratchpad.clear()

    def get_scratchpad_text(self) -> str:
        lines = []
        for step in self.scratchpad:
            lines.append(f"Thought: {step.thought}")
            lines.append(f"Action: {step.action}")
            lines.append(f"Action Input: {step.action_input}")
            lines.append(f"Observation: {step.observation}")
        return "\n".join(lines)

    def _trim(self) -> None:
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]
