#!/usr/bin/env python3
"""
MINECRAFT JAVA EDITION LAUNCHER
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("☕ LAUNCHING MINECRAFT JAVA EDITION! ☕")
    
    try:
        from minecraft_java_edition import Game
        game = Game()
        game.run()
    except ImportError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
