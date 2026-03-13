import pygame
import random
from constants import *

class Boost(pygame.sprite.Sprite):
    """Boost power-up that gives speed boost when jumped on"""
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        
        # Create glowing white circle boost
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.collected = False
        
    def update(self, player_speed):
        """Move boost with game speed and update animation"""
        if not self.collected:
            self.rect.x -= player_speed
            self.animation_frame += self.animation_speed
            
            # Redraw boost with glowing animation
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            
            # Animated glowing effect
            glow_size = int(8 + 4 * abs(pygame.math.Vector2(1, 0).rotate(self.animation_frame * 100).x))
            
            # Outer glow
            for i in range(3):
                alpha = 100 - i * 30
                size = glow_size + i * 3
                glow_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 255, 255, alpha), (size, size), size)
                self.image.blit(glow_surf, (15 - size, 15 - size))
            
            # Inner bright circle
            pygame.draw.circle(self.image, WHITE, (15, 15), 6)
            pygame.draw.circle(self.image, (200, 200, 255), (15, 15), 4)
    
    def is_off_screen(self):
        """Check if boost is off-screen to the left"""
        return self.rect.right < 0
    
    def draw(self, surface, camera_offset_x=0):
        if not self.collected:
            adjusted_rect = self.rect.copy()
            adjusted_rect.x -= camera_offset_x
            if -30 < adjusted_rect.x < SCREEN_WIDTH:  # Only draw if visible
                surface.blit(self.image, adjusted_rect)
