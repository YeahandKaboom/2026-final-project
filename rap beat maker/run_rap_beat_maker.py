#!/usr/bin/env python3
"""
🎤 EPIC RAP BEAT MAKER LAUNCHER 🎵
Create the sickest hip-hop beats and rap songs!
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎤 LAUNCHING EPIC RAP BEAT MAKER! 🎤")
    print("🎵 Create the sickest hip-hop beats ever!")
    print("🔥 Trap, Boom Bap, Lo-Fi, Club beats!")
    print("🎤 Write your own rap lyrics!")
    print("🎹 Real-time audio synthesis!")
    print("🌈 Visual effects and particles!")
    print("-" * 60)
    
    try:
        from epic_rap_beat_maker import main as game_main
        game_main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
