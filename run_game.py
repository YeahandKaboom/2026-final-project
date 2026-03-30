#!/usr/bin/env python3
"""
REAL MINECRAFT - Standalone Game Launcher
A complete Minecraft-like game with weapons, animals, building, and combat!
"""

import sys
import os
import subprocess
import pygame
from real_minecraft import Game

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("✅ Pygame installed successfully!")
        return True
    except:
        print("❌ Failed to install packages automatically")
        print("📦 Please run: pip install pygame")
        return False

def main():
    """Main launcher function"""
    print("🎮 REAL MINECRAFT - Standalone Game")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("⚠️  Pygame not found!")
        if install_dependencies():
            print("🔄 Restarting game...")
            subprocess.run([sys.executable] + sys.argv)
            return
        else:
            print("❌ Cannot start game without required packages")
            input("Press Enter to exit...")
            return
    
    print("✅ All dependencies satisfied!")
    print("🎯 Starting game with:")
    print("   🦊 Ralph & Frank Foxes")
    print("   ⚔️ Weapons & Combat") 
    print("   🏗️ Building System")
    print("   🍖 No Hunger System")
    print("   🌍 Beautiful World")
    print("=" * 50)
    print("🎮 Launching REAL Minecraft...")
    
    try:
        # Initialize and run game
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Game closed by user")
    except Exception as e:
        print(f"❌ Game error: {e}")
        print("🔧 Please report this issue")
    finally:
        pygame.quit()
        print("👋 Thanks for playing REAL Minecraft!")

if __name__ == "__main__":
    main()
