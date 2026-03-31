#!/usr/bin/env python3
"""
PLATFORM GAME LAUNCHER
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🏃 LAUNCHING PLATFORM GAME! 🏃")
    
    try:
        from game_platform import main as game_main
        game_main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
