# 🤖 SmartAgent: Modular Autonomous ReAct AI Agent

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Architecture-ReAct-orange.svg)](#architecture)
[![Build Status](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#testing)

**SmartAgent** is a lightweight, extensible, and modular AI Agent framework written in Python. It implements the **ReAct (Reasoning + Acting)** paradigm to solve complex tasks by dynamically thinking, selecting tools, observing outcomes, and synthesizing final answers.

> 💡 **Zero-Dependency by Default**: SmartAgent runs completely offline out-of-the-box with a built-in reasoning engine. You can also easily plug in OpenAI (`gpt-4o`), Gemini, or local LLMs whenever you are ready!

---

## 🏗️ Architecture

SmartAgent operates on the cyclic **Thought ➔ Action ➔ Observation** reasoning loop:

```
                  ┌───────────────────────────────┐
                  │       User Goal / Task        │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
          ┌─────────►│  Reasoning (Thought)    │
          │          └────────────┬────────────┘
          │                       │
          │                       ▼
   ┌──────┴──────┐   Tool    ┌────────────┐   Tool Result   ┌───────────────┐
   │ Observation │◄──────────┤   Action   ├────────────────►│ Tool Registry │
   └─────────────┘  Feedback └────────────┘                 │ (Calc, Files, │
                                  │                         │  Search, ...) │
                          (Goal Completed?)                 └───────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │      Final Answer       │
                     └─────────────────────────┘
```

---

## ✨ Features

- 🧠 **ReAct Reasoning Loop**: Strict separation of reasoning steps (`Thought`), execution (`Action`), and evaluation (`Observation`).
- 🛠️ **Built-in Tool Ecosystem**:
  - `CalculatorTool`: Safe AST-based mathematical evaluation (supports functions like `sqrt`, `sin`, `log`, etc.).
  - `FileReadTool` & `FileWriteTool`: Safe local file I/O operations.
  - `SystemInfoTool`: Real-time system diagnostics and datetime.
  - `SearchTool`: Simulated and extensible web/knowledge search.
- 🔌 **Extensible Tool Interface**: Create your own custom tool in less than 10 lines of code with `BaseTool`.
- 💾 **Stateful Memory**: Tracks conversation history and scratchpad execution traces.
- 💻 **Interactive CLI**: Rich command-line interface for chatting and running single tasks.
- 🧪 **Comprehensive Test Suite**: 100% test coverage for core components.

---

## 📁 Project Structure

```
A50701/
├── agent/
│   ├── __init__.py           # Package exports
│   ├── core.py               # Main Agent ReAct execution loop
│   ├── llm.py                # LLM backends (MockLLM, OpenAI, Gemini)
│   ├── memory.py             # Conversation history & Scratchpad memory
│   └── tools/
│       ├── __init__.py       # Tools registry
│       ├── base.py           # BaseTool abstract interface
│       ├── calculator.py     # Safe math evaluation tool
│       ├── file_ops.py       # File reading & writing tools
│       └── system_tools.py   # System diagnostics & search tools
├── examples/
│   ├── basic_agent.py        # Quickstart with default tools
│   └── custom_tool_agent.py  # Building and registering custom tools
├── tests/
│   └── test_agent.py         # Unit tests
├── .gitignore                # Git ignore rules
├── main.py                   # Interactive CLI entrypoint
├── requirements.txt          # Optional dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Quickstart

### 1. Run Interactive CLI (No installation needed)

```bash
python main.py
```

Sample interaction:
```
SmartAgent > Calculate (25 * 4) + sqrt(144)
💭 Thought: The user is asking to calculate a mathematical expression. I should use the calculator tool.
🛠️  Action: calculator
📥 Action Input: (25 * 4) + sqrt(144)
👁️  Observation: Result: 112.0
🎯 Final Answer: Result: 112.0
```

### 2. Run a Single Task via CLI Flag

```bash
python main.py --task "What is the current time and operating system?"
```

### 3. Run Examples

```bash
python examples/basic_agent.py
python examples/custom_tool_agent.py
```

### 4. Run Unit Tests

```bash
python -m unittest discover tests
```

---

## 🧩 Creating a Custom Tool

Extend `BaseTool` and register it with `agent.add_tool()`:

```python
from agent import Agent, BaseTool

class GreetingTool(BaseTool):
    name = "custom_greeting"
    description = "Greets a user warmly in their preferred language. Input: name."

    def run(self, name: str) -> str:
        return f"Xin chào {name}! Welcome to SmartAgent."

agent = Agent(tools=[GreetingTool()])
agent.run("Greet Minh using custom_greeting")
```

---

## 🌐 Connecting Real LLMs (OpenAI / Gemini)

1. Install optional requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Export your API key and pass the backend:
   ```python
   from agent import Agent, OpenAILLM, CalculatorTool

   llm = OpenAILLM(model="gpt-4o-mini", api_key="sk-...")
   agent = Agent(llm=llm, tools=[CalculatorTool()])
   agent.run("Calculate the compound interest on $10,000 at 5% over 10 years.")
   ```

---

## 🇻🇳 Hướng dẫn nhanh (Tiếng Việt)

1. **Khởi chạy ứng dụng trực tiếp:**
   ```bash
   python main.py
   ```
2. **Chạy các ví dụ mẫu:**
   ```bash
   python examples/basic_agent.py
   python examples/custom_tool_agent.py
   ```
3. **Chạy kiểm thử (Unit tests):**
   ```bash
   python -m unittest discover tests
   ```

---

## 📄 License

This project is licensed under the MIT License.
