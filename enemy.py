import pygame
from constants import *

class Obstacle(pygame.sprite.Sprite):
    """Obstacle types for Geometry Dash"""
    TYPE_BOX = 0
    TYPE_SPIKE = 1
    TYPE_TALL_BOX = 2
    
    def __init__(self, x, y, obstacle_type=TYPE_BOX):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.x = x
        self.y = y
        
        # Create obstacle visuals
        if obstacle_type == self.TYPE_BOX:
            self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (0, 0, 50, 80))
            pygame.draw.rect(self.image, (200, 0, 0), (5, 5, 40, 70))
            pygame.draw.rect(self.image, WHITE, (0, 0, 50, 80), 2)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            
        elif obstacle_type == self.TYPE_SPIKE:
            self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
            # Draw spike/triangle with shading
            points = [(20, 0), (0, 60), (40, 60)]
            pygame.draw.polygon(self.image, YELLOW, points)
            pygame.draw.polygon(self.image, (200, 200, 0), [(20, 0), (0, 60), (20, 50)])
            pygame.draw.line(self.image, WHITE, (20, 0), (20, 55), 1)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            
        elif obstacle_type == self.TYPE_TALL_BOX:
            self.image = pygame.Surface((40, 100), pygame.SRCALPHA)
            pygame.draw.rect(self.image, PURPLE, (0, 0, 40, 100))
            pygame.draw.rect(self.image, (150, 0, 150), (3, 3, 34, 94))
            pygame.draw.rect(self.image, WHITE, (0, 0, 40, 100), 2)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self, player_speed):
        """Move obstacle with game speed"""
        self.rect.x -= player_speed
    
    def is_off_screen(self):
        """Check if obstacle is off-screen to the left"""
        return self.rect.right < 0
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        if -50 < adjusted_rect.x < SCREEN_WIDTH:  # Only draw if visible
            surface.blit(self.image, adjusted_rect)
