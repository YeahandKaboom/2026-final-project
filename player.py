import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a simple geometric cube shape
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        pygame.draw.rect(self.image, WHITE, (0, 0, 40, 40), 2)  # Outline
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_y = 0
        self.current_speed = INITIAL_PLAYER_SPEED  # Current game speed
        self.on_ground = False
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.frames_survived = 0
        self.jump_count = 0  # Track jumps for double jump
        self.max_jumps = 2  # Allow double jump
    
    def handle_input(self, keys, mouse_pressed):
        # Jump on space or mouse click
        if (keys[pygame.K_SPACE] or mouse_pressed) and self.jump_count < self.max_jumps:
            self.vel_y = JUMP_STRENGTH
            self.jump_count += 1
            self.on_ground = False
    
    def update(self, obstacles):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position - constant forward movement
        self.rect.x += self.current_speed
        self.rect.y += self.vel_y
        self.frames_survived += 1
        
        # Reset on_ground
        self.on_ground = False
        
        # Ground collision
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            self.jump_count = 0  # Reset jumps when on ground
        
        # Check obstacle collisions
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Only die on spikes, can jump on boxes and tall boxes
                if obstacle.obstacle_type == 1:  # TYPE_SPIKE
                    return False  # Die on spikes
                # Can stand on boxes and tall boxes
                elif obstacle.obstacle_type == 0 or obstacle.obstacle_type == 2:  # TYPE_BOX or TYPE_TALL_BOX
                    # Check if we're landing on top
                    if self.rect.bottom <= obstacle.rect.top + 10 and self.vel_y >= 0:
                        self.rect.bottom = obstacle.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                        self.jump_count = 0
        
        # Game over if player goes off-screen (falls or goes too far)
        if self.rect.top > SCREEN_HEIGHT:
            return False
        
        return True  # Still alive
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        surface.blit(self.image, adjusted_rect)
