#!/usr/bin/env python3
"""
Simple Game Launcher
Choose between Geometry Dash and Minecraft-like games
"""

import pygame
import sys
import subprocess
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class SimpleLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Launcher")
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_game = 0
        
        self.games = [
            {
                "name": "Geometry Dash",
                "description": "Jump over obstacles",
                "file": "main.py",
                "color": BLUE
            },
            {
                "name": "Minecraft-like",
                "description": "Click blocks to collect, click hotbar to select",
                "file": "minecraft_game.py", 
                "color": GREEN
            },
            {
                "name": "REAL MINECRAFT",
                "description": "WEAPONS! ANIMALS! HUNTING! COMBAT! CRAFTING! SURVIVAL!",
                "file": "real_minecraft.py", 
                "color": (139, 69, 19)  # Brown color
            },
            {
                "name": "Exit",
                "description": "Close launcher",
                "file": None,
                "color": RED
            }
        ]
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.game_font = pygame.font.Font(None, 36)
        self.desc_font = pygame.font.Font(None, 24)
        
    def draw_background(self):
        """Draw animated background"""
        self.screen.fill(BLACK)
        
        # Draw animated grid
        time_offset = pygame.time.get_ticks() / 1000.0
        for x in range(0, SCREEN_WIDTH, 40):
            for y in range(0, SCREEN_HEIGHT, 40):
                if (x // 40 + y // 40) % 2 == 0:
                    alpha = int(50 + 30 * abs(pygame.math.Vector2(1, 0).rotate(time_offset * 30 + x + y).x))
                    pygame.draw.rect(self.screen, (alpha, 0, alpha), (x, y, 40, 40))
    
    def draw_menu(self):
        """Draw the game selection menu"""
        self.draw_background()
        
        # Title
        title_text = self.title_font.render("GAME LAUNCHER", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Game options
        start_y = 120
        for i, game in enumerate(self.games):
            # Highlight selected option
            if i == self.selected_game:
                # Draw selection box
                box_rect = pygame.Rect(50, start_y + i * 70 - 5, 500, 60)
                pygame.draw.rect(self.screen, game["color"], box_rect, 3)
                # Fill with transparent color
                s = pygame.Surface((496, 56))
                s.set_alpha(50)
                s.fill(game["color"])
                self.screen.blit(s, (52, start_y + i * 70 - 3))
            
            # Game name
            color = WHITE if i == self.selected_game else game["color"]
            name_text = self.game_font.render(game["name"], True, color)
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 70 + 5))
            self.screen.blit(name_text, name_rect)
            
            # Game description
            desc_text = self.desc_font.render(game["description"], True, GRAY)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 70 + 30))
            self.screen.blit(desc_text, desc_rect)
        
        # Instructions
        inst_text = self.desc_font.render("UP/DOWN: Navigate | ENTER: Select | ESC: Exit", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(inst_text, inst_rect)
    
    def launch_game(self, game_file):
        """Launch the selected game"""
        if game_file is None:
            return "exit"
        
        try:
            if os.path.exists(game_file):
                print(f"Launching {game_file}...")
                subprocess.run([sys.executable, game_file], check=True)
            else:
                print(f"Game file {game_file} not found!")
        except subprocess.CalledProcessError as e:
            print(f"Error running {game_file}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        return "continue"
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_game = (self.selected_game - 1) % len(self.games)
                elif event.key == pygame.K_DOWN:
                    self.selected_game = (self.selected_game + 1) % len(self.games)
                elif event.key == pygame.K_RETURN:
                    selected = self.games[self.selected_game]
                    result = self.launch_game(selected["file"])
                    if result == "exit":
                        self.running = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """Main launcher loop"""
        while self.running:
            self.handle_events()
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = SimpleLauncher()
    launcher.run()
