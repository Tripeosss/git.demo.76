import os
from agent.tools.base import BaseTool


class FileReadTool(BaseTool):
    name = "read_file"
    description = "Reads content from a local file. Input should be the file path."

    def run(self, filepath: str) -> str:
        try:
            if not os.path.exists(filepath):
                return f"Error: File '{filepath}' does not exist."
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return f"Content of {filepath}:\n{content}"
        except Exception as e:
            return f"Error reading file '{filepath}': {str(e)}"


class FileWriteTool(BaseTool):
    name = "write_file"
    description = (
        "Writes text content to a local file. Input format should be 'filepath:::content'."
    )

    def run(self, input_str: str) -> str:
        try:
            if ":::" not in input_str:
                return "Error: Input format must be 'filepath:::content'"
            filepath, content = input_str.split(":::", 1)
            filepath = filepath.strip()
            os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote {len(content)} characters to {filepath}."
        except Exception as e:
            return f"Error writing to file: {str(e)}"
