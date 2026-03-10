import pygame
from constants import *

class Portal(pygame.sprite.Sprite):
    """Portal obstacle for Geometry Dash"""
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        
        # Create portal visual - animated circular portal
        self.image = pygame.Surface((60, 80), pygame.SRCALPHA)
        self.draw_portal()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        
        # Animation state
        self.animation_frame = 0
        self.particles = []
        
    def draw_portal(self):
        """Draw the portal with animated effect"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparency
        
        # Portal outer ring
        pygame.draw.ellipse(self.image, (150, 50, 255), (5, 5, 50, 70), 3)
        # Inner glow
        pygame.draw.ellipse(self.image, (200, 100, 255), (10, 10, 40, 60), 2)
        # Center portal
        pygame.draw.ellipse(self.image, (100, 0, 200), (15, 15, 30, 50))
        
        # Animated center
        center_size = 20 + (self.animation_frame % 10)
        pygame.draw.ellipse(self.image, (255, 255, 255), 
                          (30 - center_size//2, 40 - center_size//2, center_size, center_size))
    
    def update(self, player_speed):
        """Move portal with game speed and animate"""
        self.rect.x -= player_speed
        self.animation_frame += 1
        
        # Redraw portal with animation
        self.draw_portal()
    
    def is_off_screen(self):
        """Check if portal is off-screen to the left"""
        return self.rect.right < 0
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        if -50 < adjusted_rect.x < SCREEN_WIDTH:  # Only draw if visible
            surface.blit(self.image, adjusted_rect)
