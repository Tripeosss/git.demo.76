"""
Custom Tool Example
Shows how easily developers can create custom tools and attach them to SmartAgent.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent import Agent, BaseTool


class WeatherTool(BaseTool):
    name = "get_weather"
    description = "Provides current weather forecast for a given city name. Input: city name."

    def run(self, city: str) -> str:
        city_clean = city.strip().title()
        # Simulated live weather data
        weather_db = {
            "Hanoi": "Sunny, 28°C, Humidity: 65%",
            "Ho Chi Minh": "Scattered Clouds, 32°C, Humidity: 75%",
            "Tokyo": "Clear, 18°C, Humidity: 50%",
            "New York": "Breezy, 15°C, Humidity: 45%",
        }
        return weather_db.get(
            city_clean,
            f"Weather in {city_clean}: Partly Cloudy, 24°C, Wind: 10 km/h."
        )


def main():
    agent = Agent(tools=[WeatherTool()], verbose=True)

    print("\n--- Testing Custom Weather Tool ---")
    agent.run("What is the weather in Hanoi?")


if __name__ == "__main__":
    main()
