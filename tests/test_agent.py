import unittest
from agent import Agent, CalculatorTool, SystemInfoTool, FileWriteTool, FileReadTool
import os


class TestSmartAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent(
            tools=[
                CalculatorTool(),
                SystemInfoTool(),
                FileWriteTool(),
                FileReadTool(),
            ],
            verbose=False,
        )

    def test_calculator_tool(self):
        calc = CalculatorTool()
        result = calc.run("10 + 25 * 2")
        self.assertIn("60", result)

    def test_calculator_advanced(self):
        calc = CalculatorTool()
        result = calc.run("sqrt(100) + 5")
        self.assertIn("15", result)

    def test_system_info_tool(self):
        tool = SystemInfoTool()
        res = tool.run()
        self.assertIn("os", res.lower())

    def test_file_tools(self):
        filepath = "test_output.txt"
        writer = FileWriteTool()
        reader = FileReadTool()

        write_res = writer.run(f"{filepath}:::Unit Test Passed!")
        self.assertIn("Successfully", write_res)

        read_res = reader.run(filepath)
        self.assertIn("Unit Test Passed!", read_res)

        if os.path.exists(filepath):
            os.remove(filepath)

    def test_agent_math_run(self):
        answer = self.agent.run("Calculate 25 + 75")
        self.assertIn("100", answer)


if __name__ == "__main__":
    unittest.main()
