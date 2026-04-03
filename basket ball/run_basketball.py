#!/usr/bin/env python3
"""
🏀 EPIC BASKETBALL GAME LAUNCHER 🏀
1v1 Half Court Showdown!
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🏀 LAUNCHING EPIC BASKETBALL! 🏀")
    print("🎮 1v1 Half Court Showdown!")
    print("🌟 Play as Warrior, Ninja, Wizard, Robot, Dragon, Astronaut, Pirate, Superhero!")
    print("🏆 VS Michael Jordan, Cooper Flagg, Reggie Miller, LeBron James, Kobe Bryant, Steph Curry, Shaq, Kevin Durant!")
    print("-" * 60)
    
    try:
        from epic_basketball import main as game_main
        game_main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
