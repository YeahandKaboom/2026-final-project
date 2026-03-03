import pygame
import math
from constants import *

class Collectible(pygame.sprite.Sprite):
    """Collectible items that give bonus points"""
    TYPE_COIN = 0
    TYPE_STAR = 1
    
    def __init__(self, x, y, collectible_type=TYPE_COIN):
        super().__init__()
        self.collectible_type = collectible_type
        self.x = x
        self.y = y
        
        if collectible_type == self.TYPE_COIN:
            # Draw coin (yellow circle)
            self.image = pygame.Surface((COLLECTIBLE_SIZE, COLLECTIBLE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (COLLECTIBLE_SIZE // 2, COLLECTIBLE_SIZE // 2), COLLECTIBLE_SIZE // 2)
            pygame.draw.circle(self.image, DARK_GRAY, (COLLECTIBLE_SIZE // 2, COLLECTIBLE_SIZE // 2), COLLECTIBLE_SIZE // 2 - 2, 1)
            self.points = 25
            
        elif collectible_type == self.TYPE_STAR:
            # Draw star (more points)
            self.image = pygame.Surface((COLLECTIBLE_SIZE + 5, COLLECTIBLE_SIZE + 5), pygame.SRCALPHA)
            center = (COLLECTIBLE_SIZE // 2 + 2, COLLECTIBLE_SIZE // 2 + 2)
            # Simple star shape
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    r = COLLECTIBLE_SIZE // 2 + 2
                else:
                    r = COLLECTIBLE_SIZE // 4
                points.append((center[0] + r * math.sin(angle), center[1] - r * math.cos(angle)))
            pygame.draw.polygon(self.image, GREEN, points)
            self.points = 100
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False
    
    def update(self, player_speed):
        """Move collectible with game speed"""
        self.rect.x -= player_speed
    
    def is_off_screen(self):
        """Check if collectible is off-screen to the left"""
        return self.rect.right < 0
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        if -30 < adjusted_rect.x < SCREEN_WIDTH:  # Only draw if visible
            surface.blit(self.image, adjusted_rect)
