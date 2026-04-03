#!/usr/bin/env python3
"""
REAL MINECRAFT LAUNCHER
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎯 LAUNCHING REAL MINECRAFT! 🎯")
    
    try:
        from real_minecraft import Game
        game = Game()
        game.run()
    except ImportError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
