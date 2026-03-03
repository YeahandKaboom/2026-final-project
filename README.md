# Geometry Dash

A Geometry Dash inspired game built with Pygame featuring endless runner mechanics with geometric obstacles.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Controls

- **SPACE or MOUSE CLICK**: Jump
- The player automatically moves forward at constant speed
- Click anywhere to restart after game over

## Gameplay

- Avoid randomly generated obstacles (boxes, spikes, tall walls)
- Score increases as you progress further
- Three types of obstacles appear in random order:
  - **Boxes** (Red) - Standard obstacles
  - **Spikes** (Yellow) - Dangerous pointy obstacles
  - **Tall Boxes** (Purple) - Tall walls that require precise jumps

## Features

- Continuous horizontal scrolling
- Auto-generated obstacles with random patterns
- Score and distance tracking
- Game over detection with collision system
- Smooth camera following the player
- Geometric shape-based graphics
- Patterned ground with scrolling effect

## Project Structure

- `main.py` - Main game loop with spawn management
- `player.py` - Player class with jumping mechanics and collision detection
- `game_platform.py` - Ground class with scrolling pattern
- `enemy.py` - Obstacle class with multiple geometric shapes
- `constants.py` - Game configuration and physics constants
- `requirements.txt` - Python dependencies

## Physics

- Gravity: 0.6
- Jump Strength: -16
- Player Speed: 8 pixels per frame
- FPS: 60
