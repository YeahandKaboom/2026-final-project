#!/usr/bin/env python3
"""
MONEY CRAFT GAME LAUNCHER
The Ultimate Mining Adventure with Villages, Tunnels, and Insane World Generation!
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the Money Craft Game"""
    print("🚀 LAUNCHING MONEY CRAFT GAME! 🚀")
    print("💰 The Ultimate Mining Adventure! 💰")
    print("🏘️ Working Villages! 🕳️ Mining Tunnels! 🌈 Insane World! 🛒️ Working Shop!")
    print("-" * 60)
    
    try:
        # Import and run the game
        from wealth_craft_game import WealthCraftGame
        
        # Initialize Pygame
        pygame.init()
        
        # Create and run the game
        game = WealthCraftGame()
        game.run()
        
    except ImportError as e:
        print(f"❌ Error importing game: {e}")
        print("Make sure all game files are in the same directory!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
