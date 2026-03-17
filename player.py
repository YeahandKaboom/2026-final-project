import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a more visually appealing player shape
        self.base_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Draw a square with gradient-like effect
        pygame.draw.rect(self.base_image, BLUE, (0, 0, 40, 40))
        pygame.draw.rect(self.base_image, (0, 150, 255), (2, 2, 36, 36))
        pygame.draw.rect(self.base_image, WHITE, (0, 0, 40, 40), 3)  # Outline
        # Add eyes for character
        pygame.draw.circle(self.base_image, WHITE, (12, 14), 3)
        pygame.draw.circle(self.base_image, WHITE, (28, 14), 3)
        pygame.draw.circle(self.base_image, BLACK, (12, 14), 1)
        pygame.draw.circle(self.base_image, BLACK, (28, 14), 1)
        
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_y = 0
        self.vel_x = 0  # Add horizontal velocity for wall crash
        self.current_speed = INITIAL_PLAYER_SPEED  # Current game speed
        self.on_ground = False
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.frames_survived = 0
        self.jump_count = 0  # Track jumps for double jump
        self.max_jumps = 2  # Allow double jump
        self.rotation_angle = 0  # Track rotation angle for flip animation
    
    def handle_input(self, keys, mouse_pressed):
        # Jump on space or mouse click
        if (keys[pygame.K_SPACE] or mouse_pressed) and self.jump_count < self.max_jumps:
            self.vel_y = JUMP_STRENGTH
            self.jump_count += 1
            self.on_ground = False
            # Start rotation for front flip - 360 degrees per jump
            self.rotation_angle = 0
    
    def update(self, obstacles):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Reset on_ground first
        self.on_ground = False
        
        # Update position - constant forward movement
        self.rect.x += self.current_speed
        self.rect.y += self.vel_y
        
        # Add horizontal velocity for victory crash animation
        if self.vel_x != 0:
            self.rect.x += self.vel_x
            
        self.frames_survived += 1
        
        # Ground collision
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            self.jump_count = 0  # Reset jumps when on ground
        
        # Check obstacle collisions
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Only die on spikes and upside-down triangles, can jump on boxes and tall boxes
                if obstacle.obstacle_type == 1:  # TYPE_SPIKE
                    return {'alive': False, 'collision_type': 'spike'}  # Die on spikes
                elif obstacle.obstacle_type == 3:  # TYPE_UPSIDE_DOWN_TRIANGLE
                    return {'alive': False, 'collision_type': 'triangle'}  # Die on upside-down triangles
                # Can stand on boxes and tall boxes, but can't pass through them
                elif obstacle.obstacle_type == 0 or obstacle.obstacle_type == 2:  # TYPE_BOX or TYPE_TALL_BOX
                    # Check if we're landing on top
                    if self.rect.bottom <= obstacle.rect.top + 10 and self.vel_y >= 0:
                        self.rect.bottom = obstacle.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                        self.jump_count = 0
                    else:
                        # Can't pass through sides - die if hitting from any other direction
                        return {'alive': False, 'collision_type': 'box'}
        
        # Update rotation angle only when in the air (not on ground)
        if self.on_ground:
            # Reset rotation when on ground - stay straight
            self.rotation_angle = 0
        else:
            # Flip 360 degrees during jump - complete rotation
            self.rotation_angle += 18  # 360 / 20 frames = 18 degrees per frame
            if self.rotation_angle >= 360:
                self.rotation_angle = 0
        
        # Apply rotation to image
        self.image = pygame.transform.rotate(self.base_image, self.rotation_angle)
        # Store the current bottom position before updating rect
        old_bottom = self.rect.bottom
        old_left = self.rect.left
        self.rect = self.image.get_rect()
        self.rect.left = old_left
        self.rect.bottom = old_bottom
        
        return {'alive': True, 'collision_type': None}
    
    def draw(self, surface, camera_offset_x=0):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        surface.blit(self.image, adjusted_rect)
