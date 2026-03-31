import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    """Ground platform for Geometry Dash"""
    def __init__(self, x, y, width, height, color=DARK_GRAY):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        surface.blit(self.image, adjusted_rect)

class Ground(pygame.sprite.Sprite):
    """Scrolling ground for infinite level"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH * 2, GROUND_HEIGHT))
        self.image.fill(DARK_GRAY)
        # Add pattern to ground
        for i in range(0, SCREEN_WIDTH * 2, 50):
            pygame.draw.line(self.image, GRAY, (i, 0), (i, GROUND_HEIGHT), 1)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.speed = PLAYER_SPEED
    
    def update(self):
        """Scroll ground continuously"""
        self.rect.x -= self.speed
        # Reset ground position when it scrolls too far
        if self.rect.x <= -SCREEN_WIDTH:
            self.rect.x = 0
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
