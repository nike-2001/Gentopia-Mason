from typing import Optional, Type
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool
import random
import time

class WellnessArgs(BaseModel):
    screen_time_hours: Optional[float] = Field(0, description="Number of hours of screen time.")
    habit_goal: Optional[str] = Field(None, description="The habit goal for the user (e.g., 'reduce screen time', 'practice mindfulness').")

class DigitalWellnessTool(BaseTool):
    """Tool that helps track digital wellness habits and provides wellness tips."""
    name = "digital_wellness_tool"
    description = ("A digital wellness tool that monitors screen time, tracks habits, and provides mindfulness exercises.")
    args_schema: Optional[Type[BaseModel]] = WellnessArgs

    wellness_tips = [
        "Take a break from your screen and stretch your legs for 5 minutes.",
        "Practice the 20-20-20 rule: Every 20 minutes, look at something 20 feet away for 20 seconds.",
        "Try a breathing exercise: Inhale deeply for 4 seconds, hold for 4, exhale for 4, and repeat."
    ]

    def _run(self, screen_time_hours: float = 0, habit_goal: Optional[str] = None) -> str:
        if screen_time_hours > 4:
            return f"You've spent {screen_time_hours} hours on your screen today. Consider taking a break: {random.choice(self.wellness_tips)}"
        elif habit_goal:
            return f"You're working on your goal: {habit_goal}. Keep it up! Here's a tip: {random.choice(self.wellness_tips)}"
        else:
            return f"Keep up the good work! {random.choice(self.wellness_tips)}"

    async def _arun(self, screen_time_hours: float = 0, habit_goal: Optional[str] = None) -> str:
        return self._run(screen_time_hours, habit_goal)

# Example usage
if __name__ == "__main__":
    digital_wellness_tool = DigitalWellnessTool()
    
    # Example user input
    screen_time = 5.5  # hours spent on screen today
    habit = "reduce screen time"
    
    # Run the tool
    output = digital_wellness_tool._run(screen_time_hours=screen_time, habit_goal=habit)
    print(output)
