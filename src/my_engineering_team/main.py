#!/usr/bin/env python
import sys
import os
import warnings
import traceback

from my_engineering_team.crew import MyEngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
Requirements for Snake Demo Game
1. Main Goal
Create a simple "Snake" game where the player controls a snake, collects food, and avoids collisions with obstacles.
2. Core Mechanics
Game Field:
A square or rectangular area with borders.
Snake:
Composed of a head and body segments.
Moves in 4 directions (up, down, left, right) based on player input.
Grows by one segment when eating food.
Food:
Appears randomly on the field.
Respawns after being eaten.
Game Over Conditions:
Snake collides with the field border or its own body.
3. Controls
PC: Arrow keys or WASD.
Mobile Devices: Optional (not required for demo).
4. Features
Start:
Snake begins with minimal length (e.g., 3 segments).
Food appears on the field.
Score:
Increases by 1 for each food eaten.
Displayed on-screen.
Restart:
After losing, the player can restart or exit.
5. Graphics and Sound
Graphics: Minimalist style.
Example: Monochrome squares (e.g., green snake, red food, black background).
Smooth snake movement animation.
Sound: Optional (not required for demo).
6. Interface
Score: Displayed in a screen corner.
Messages:
"Press Start" (on the main screen).
"Game Over. Score: [X]" (after losing).
7. Excluded Features for Simplification
Difficulty levels (snake speed is fixed).
Control customization.
High score tracking.
Pause functionality.
Mobile device adaptation.
Note: The demo focuses on core snake mechanics with a minimal interface and no extra features.
"""
module_name = "Snake.py"
class_name = "Snake"


def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
         }
    
    try:
    # Create and run the crew
       print("START EXECUTION")
       result = MyEngineeringTeam().crew().kickoff(inputs=inputs)
    
    except Exception as e:
       print("[ERROR] An exception occurred during crew kickoff:")
       traceback.print_exc()
       raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()