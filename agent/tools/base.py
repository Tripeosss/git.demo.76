from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all Agent tools."""

    name: str = "base_tool"
    description: str = "Base tool description"

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute the tool action."""
        pass

    def to_dict(self) -> Dict[str, str]:
        """Return tool metadata for the LLM prompt."""
        return {
            "name": self.name,
            "description": self.description,
        }
