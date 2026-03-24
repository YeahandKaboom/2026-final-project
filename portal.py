import pygame
from constants import *

class Portal(pygame.sprite.Sprite):
    """Portal for level transition"""
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        
        # Create portal visual - much larger animated circular portal
        self.image = pygame.Surface((120, 120), pygame.SRCALPHA)  # Doubled size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.used = False  # Track if portal has been used
        
    def update(self, player_speed):
        """Move portal with game speed and update animation"""
        self.rect.x -= player_speed
        self.animation_frame += self.animation_speed
        
        # Redraw portal with animation
        self.image = pygame.Surface((120, 120), pygame.SRCALPHA)
        
        # Animated swirling effect - larger and more prominent
        for i in range(4):  # One more ring for visual impact
            radius = 50 - i * 8  # Larger radii
            color_intensity = int(150 + 105 * abs(pygame.math.Vector2(1, 0).rotate(self.animation_frame * 50 + i * 90).x))
            color = (color_intensity, 0, 255 - color_intensity // 2)
            
            # Draw rotating arcs - thicker lines
            start_angle = self.animation_frame + i * 90
            pygame.draw.arc(self.image, color, 
                          (60 - radius, 60 - radius, radius * 2, radius * 2),
                          start_angle, start_angle + 3.14, 5)  # Thicker lines
        
        # Portal center glow - removed
        # glow_size = int(20 + 10 * abs(pygame.math.Vector2(1, 0).rotate(self.animation_frame * 100).x))
        # pygame.draw.circle(self.image, (200, 100, 255), (60, 60), glow_size)
        
        # Portal frame - removed
        # pygame.draw.circle(self.image, WHITE, (60, 60), 55, 4)  # Thicker frame
        
        # Add pulsing outer ring - removed
        # pulse_size = int(65 + 5 * abs(pygame.math.Vector2(1, 0).rotate(self.animation_frame * 30).x))
        # pygame.draw.circle(self.image, (255, 200, 255), (60, 60), pulse_size, 2)
        
    def is_off_screen(self):
        """Check if portal is off-screen to the left"""
        return self.rect.right < 0
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        if -120 < adjusted_rect.x < SCREEN_WIDTH:  # Only draw if visible (larger portal)
            surface.blit(self.image, adjusted_rect)
