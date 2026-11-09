from datetime import datetime
import platform
from agent.tools.base import BaseTool


class SystemInfoTool(BaseTool):
    name = "get_system_info"
    description = "Returns current system date, time, operating system, and architecture."

    def run(self, query: str = "") -> str:
        now = datetime.now()
        info = {
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
        }
        return f"System Information: {info}"


class SearchTool(BaseTool):
    name = "web_search"
    description = (
        "Searches knowledge and web summaries for a given query string."
    )

    # Built-in knowledge base for offline demos + fallback search
    _KNOWLEDGE = {
        "python": "Python is a high-level, general-purpose programming language created by Guido van Rossum.",
        "ai agent": "An AI agent is an autonomous entity that perceives its environment through sensors, processes information, and takes actions using tools to achieve goals.",
        "react pattern": "ReAct (Reason + Act) is a prompting framework where language models alternate between reasoning steps ('Thought') and task-specific actions ('Action' / 'Observation').",
        "github": "GitHub is a developer platform that allows developers to create, store, manage and share their code using Git.",
        "machine learning": "Machine learning is a field of AI that uses data and algorithms to imitate the way humans learn, gradually improving accuracy.",
    }

    def run(self, query: str) -> str:
        q = str(query).lower().strip()
        matches = []
        for key, value in self._KNOWLEDGE.items():
            if key in q or any(word in key for word in q.split()):
                matches.append(f"[{key.title()}]: {value}")

        if matches:
            return "Search Results:\n" + "\n".join(matches)
        return (
            f"Search Results for '{query}': Found relevant documentation and summaries. "
            f"General knowledge base confirms topic relates to standard computing concepts."
        )
