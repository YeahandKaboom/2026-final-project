#!/usr/bin/env python3
"""
🏀 EPIC BASKETBALL 1v1 - HALF COURT SHOWDOWN! 🏀
Fixed camera and life-like court!
"""

import pygame
import math
import random
import sys
from enum import Enum

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors - Life-like court colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 90, 43)  # Wood floor color
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
COURT_GREEN = (139, 90, 43)  # Wood floor
COURT_LINE = (240, 240, 240)  # Slightly off-white lines
HOOP_ORANGE = (255, 69, 0)  # Bright orange

# Game states
class GameState(Enum):
    MENU = 0
    CHARACTER_SELECT = 1
    OPPONENT_SELECT = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5

# Player characters
class CharacterType(Enum):
    WARRIOR = 0
    NINJA = 1
    WIZARD = 2
    ROBOT = 3
    DRAGON = 4
    ASTRONAUT = 5
    PIRATE = 6
    SUPERHERO = 7

# Famous NBA players
class NBAPlayer(Enum):
    MICHAEL_JORDAN = 0
    COOPER_FLAGG = 1
    REGGIE_MILLER = 2
    LEBRON_JAMES = 3
    KOBE_BRYANT = 4
    STEPH_CURRY = 5
    SHAQUILLE_ONEAL = 6
    KEVIN_DURANT = 7

class Basketball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = 12
        self.held_by = None
        self.gravity = 0.5
        self.bounce_damping = 0.7
        self.spinning = False
        self.spin_angle = 0
        
    def update(self):
        if self.held_by is None:
            # Apply physics
            self.vy += self.gravity
            self.x += self.vx
            self.y += self.vy
            
            # Bounce off ground
            if self.y >= SCREEN_HEIGHT - 100 - self.radius:
                self.y = SCREEN_HEIGHT - 100 - self.radius
                self.vy *= -self.bounce_damping
                self.vx *= 0.9  # Friction
                
            # Bounce off walls
            if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
                self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
                self.vx *= -0.8
                
            # Update spin
            if self.spinning:
                self.spin_angle += 10
                
    def shoot(self, target_x, target_y, power):
        """Shoot basketball towards target with given power"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Calculate trajectory
            angle = math.atan2(dy, dx)
            velocity = min(power * 0.3, 25)  # Cap max velocity
            
            self.vx = math.cos(angle) * velocity
            self.vy = math.sin(angle) * velocity - 10  # Add arc
            self.spinning = True
            
    def draw(self, screen):
        # Draw basketball with lines
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw basketball lines
        if self.spinning:
            angle = self.spin_angle
        else:
            angle = 0
            
        # Vertical line
        end_x1 = self.x + math.cos(math.radians(angle)) * self.radius
        end_y1 = self.y + math.sin(math.radians(angle)) * self.radius
        end_x2 = self.x - math.cos(math.radians(angle)) * self.radius
        end_y2 = self.y - math.sin(math.radians(angle)) * self.radius
        pygame.draw.line(screen, BLACK, (end_x1, end_y1), (end_x2, end_y2), 2)
        
        # Horizontal line
        end_x3 = self.x + math.cos(math.radians(angle + 90)) * self.radius
        end_y3 = self.y - math.sin(math.radians(angle + 90)) * self.radius
        end_x4 = self.x - math.cos(math.radians(angle + 90)) * self.radius
        end_y4 = self.y - math.sin(math.radians(angle + 90)) * self.radius
        pygame.draw.line(screen, BLACK, (end_x3, end_y3), (end_x4, end_y4), 2)
    
    def draw_with_offset(self, screen, cam_x, cam_y):
        """Draw basketball with camera offset"""
        # Draw at offset position
        draw_x = self.x + cam_x
        draw_y = self.y + cam_y
        
        # Draw basketball with lines
        pygame.draw.circle(screen, ORANGE, (int(draw_x), int(draw_y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(draw_x), int(draw_y)), self.radius, 2)
        
        # Draw basketball lines
        if self.spinning:
            angle = self.spin_angle
        else:
            angle = 0
            
        # Vertical line
        end_x1 = draw_x + math.cos(math.radians(angle)) * self.radius
        end_y1 = draw_y + math.sin(math.radians(angle)) * self.radius
        end_x2 = draw_x - math.cos(math.radians(angle)) * self.radius
        end_y2 = draw_y - math.sin(math.radians(angle)) * self.radius
        pygame.draw.line(screen, BLACK, (end_x1, end_y1), (end_x2, end_y2), 2)
        
        # Horizontal line
        end_x3 = draw_x + math.cos(math.radians(angle + 90)) * self.radius
        end_y3 = draw_y - math.sin(math.radians(angle + 90)) * self.radius
        end_x4 = draw_x - math.cos(math.radians(angle + 90)) * self.radius
        end_y4 = draw_y - math.sin(math.radians(angle + 90)) * self.radius
        pygame.draw.line(screen, BLACK, (end_x3, end_y3), (end_x4, end_y4), 2)

class Player:
    def __init__(self, x, y, character_type, is_player=True):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.character_type = character_type
        self.is_player = is_player
        
        # Character stats
        self.set_stats()
        
        # Physics
        self.speed = self.base_speed
        self.jump_power = self.base_jump
        self.on_ground = False
        self.gravity = 0.8
        
        # Basketball
        self.has_ball = True  # Start with ball always
        self.shoot_power = 0
        self.shoot_charging = False
        
        # Advanced dribbling system
        self.dribble_timer = 0
        self.is_dribbling = False
        self.dribble_style = "normal"  # normal, through_legs, behind_back
        self.dribble_height = 25
        self.ball_rotation = 0
        self.dribble_speed = 0.1
        
        # Realistic body animation
        self.animation_frame = 0
        self.facing_right = True
        self.body_angle = 0
        self.arm_angle = 0
        self.leg_angle_left = 0
        self.leg_angle_right = 0
        self.head_angle = 0
        self.walking_cycle = 0
        self.running_cycle = 0
        self.jumping_animation = 0
        
        # Character appearance
        self.skin_color = (255, 220, 177)  # Default skin tone
        self.hair_color = (50, 25, 0)  # Default hair
        self.jersey_color = (0, 100, 200)  # Default jersey
        self.short_color = (0, 50, 150)  # Default shorts
        self.shoe_color = (0, 0, 0)  # Default shoes
        
        # Body dimensions
        self.head_radius = 12
        self.neck_length = 8
        self.torso_height = 25
        self.torso_width = 20
        self.arm_length = 18
        self.leg_length = 30
        self.leg_width = 8
        
    def set_stats(self):
        """Set stats based on character type"""
        stats = {
            CharacterType.WARRIOR: {"speed": 4, "jump": 12, "shoot": 15, "defense": 8, "color": RED},
            CharacterType.NINJA: {"speed": 6, "jump": 15, "shoot": 12, "defense": 5, "color": BLACK},
            CharacterType.WIZARD: {"speed": 5, "jump": 14, "shoot": 18, "defense": 6, "color": PURPLE},
            CharacterType.ROBOT: {"speed": 3, "jump": 10, "shoot": 20, "defense": 10, "color": GRAY},
            CharacterType.DRAGON: {"speed": 5, "jump": 18, "shoot": 16, "defense": 7, "color": (255, 140, 0)},
            CharacterType.ASTRONAUT: {"speed": 5, "jump": 16, "shoot": 14, "defense": 6, "color": BLUE},
            CharacterType.PIRATE: {"speed": 4, "jump": 13, "shoot": 13, "defense": 7, "color": (101, 67, 33)},
            CharacterType.SUPERHERO: {"speed": 7, "jump": 20, "shoot": 17, "defense": 9, "color": (255, 215, 0)}
        }
        
        stat = stats[self.character_type]
        self.base_speed = stat["speed"]
        self.base_jump = stat["jump"]
        self.shoot_skill = stat["shoot"]
        self.defense = stat["defense"]
        self.color = stat["color"]
        
    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.vy += self.gravity
            
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Ground collision
        if self.y >= SCREEN_HEIGHT - 140:
            self.y = SCREEN_HEIGHT - 140
            self.vy = 0
            self.on_ground = True
            self.jumping_animation = 0
        else:
            self.on_ground = False
            
        # Boundaries
        self.x = max(20, min(SCREEN_WIDTH - 20, self.x))
        
        # Advanced dribbling mechanics
        if self.has_ball and self.on_ground:
            self.dribble_timer += 1
            
            # Dribble frequency based on movement speed
            dribble_frequency = 15 if abs(self.vx) > 2 else 20
            
            if self.dribble_timer >= dribble_frequency:
                self.is_dribbling = True
                self.dribble_timer = 0
                
                # Randomly change dribble style for variety
                if random.random() < 0.1:  # 10% chance to change style
                    styles = ["normal", "through_legs", "behind_back"]
                    self.dribble_style = random.choice(styles)
                    
                # Update ball rotation
                self.ball_rotation += 45
            else:
                self.is_dribbling = False
        else:
            self.dribble_timer = 0
            self.is_dribbling = False
            
        # Realistic body animation
        self.animation_frame += 0.1
        
        # Walking/running animation
        if abs(self.vx) > 0.5:
            if abs(self.vx) > 3:  # Running
                self.running_cycle += 0.3
                self.leg_angle_left = math.sin(self.running_cycle) * 30
                self.leg_angle_right = math.sin(self.running_cycle + math.pi) * 30
                self.arm_angle = math.sin(self.running_cycle * 2) * 20
            else:  # Walking
                self.walking_cycle += 0.15
                self.leg_angle_left = math.sin(self.walking_cycle) * 15
                self.leg_angle_right = math.sin(self.walking_cycle + math.pi) * 15
                self.arm_angle = math.sin(self.walking_cycle * 2) * 10
        else:  # Standing
            self.leg_angle_left *= 0.9  # Smooth return to neutral
            self.leg_angle_right *= 0.9
            self.arm_angle *= 0.9
            
        # Body leaning based on movement
        self.body_angle = self.vx * 2
        
        # Head movement
        self.head_angle = math.sin(self.animation_frame) * 2
        
        # Jumping animation
        if not self.on_ground:
            self.jumping_animation = min(self.jumping_animation + 0.2, 1)
            self.leg_angle_left = -20
            self.leg_angle_right = -20
            self.arm_angle = 45 if self.has_ball else -30
        else:
            self.jumping_animation = max(self.jumping_animation - 0.1, 0)
            
        # Friction
        self.vx *= 0.9
        
    def draw_realistic(self, screen):
        """Draw realistic character with anti-aliased graphics"""
        # Calculate body positions based on animations
        
        # Head position
        head_x = self.x + math.sin(math.radians(self.head_angle)) * 2
        head_y = self.y - 50 - self.jumping_animation * 10
        
        # Neck position
        neck_x = self.x
        neck_y = self.y - 38 - self.jumping_animation * 8
        
        # Torso position (leaning based on movement)
        torso_x = self.x + math.sin(math.radians(self.body_angle)) * 5
        torso_y = self.y - 25 - self.jumping_animation * 5
        
        # Draw legs with anti-aliasing
        # Left leg
        left_hip_x = torso_x - 5
        left_hip_y = torso_y + self.torso_height // 2
        left_knee_x = left_hip_x + math.sin(math.radians(self.leg_angle_left)) * 15
        left_knee_y = left_hip_y + 15
        left_foot_x = left_hip_x + math.sin(math.radians(self.leg_angle_left)) * 30
        left_foot_y = self.y
        
        # Draw left leg with thicker lines for clarity
        pygame.draw.line(screen, self.short_color, (left_hip_x, left_hip_y), (left_knee_x, left_knee_y), self.leg_width + 2)
        pygame.draw.line(screen, self.short_color, (left_knee_x, left_knee_y), (left_foot_x, left_foot_y), self.leg_width + 2)
        pygame.draw.circle(screen, self.shoe_color, (int(left_foot_x), int(left_foot_y)), 8)
        pygame.draw.circle(screen, BLACK, (int(left_foot_x), int(left_foot_y)), 8, 2)
        
        # Right leg
        right_hip_x = torso_x + 5
        right_hip_y = torso_y + self.torso_height // 2
        right_knee_x = right_hip_x + math.sin(math.radians(self.leg_angle_right)) * 15
        right_knee_y = right_hip_y + 15
        right_foot_x = right_hip_x + math.sin(math.radians(self.leg_angle_right)) * 30
        right_foot_y = self.y
        
        # Draw right leg with thicker lines
        pygame.draw.line(screen, self.short_color, (right_hip_x, right_hip_y), (right_knee_x, right_knee_y), self.leg_width + 2)
        pygame.draw.line(screen, self.short_color, (right_knee_x, right_knee_y), (right_foot_x, right_foot_y), self.leg_width + 2)
        pygame.draw.circle(screen, self.shoe_color, (int(right_foot_x), int(right_foot_y)), 8)
        pygame.draw.circle(screen, BLACK, (int(right_foot_x), int(right_foot_y)), 8, 2)
        
        # Draw torso (jersey) with better contrast
        torso_rect = pygame.Rect(torso_x - self.torso_width // 2 - 2, torso_y - 2, 
                               self.torso_width + 4, self.torso_height + 4)
        pygame.draw.rect(screen, self.jersey_color, torso_rect)
        pygame.draw.rect(screen, BLACK, torso_rect, 3)
        
        # Draw arms with thicker lines
        # Left arm
        left_shoulder_x = torso_x - self.torso_width // 2
        left_shoulder_y = torso_y + 5
        left_elbow_x = left_shoulder_x + math.sin(math.radians(self.arm_angle + 90)) * self.arm_length // 2
        left_elbow_y = left_shoulder_y + 10
        left_hand_x = left_shoulder_x + math.sin(math.radians(self.arm_angle + 90)) * self.arm_length
        left_hand_y = left_shoulder_y + 20
        
        # Draw left arm
        pygame.draw.line(screen, self.skin_color, (left_shoulder_x, left_shoulder_y), (left_elbow_x, left_elbow_y), 8)
        pygame.draw.line(screen, self.skin_color, (left_elbow_x, left_elbow_y), (left_hand_x, left_hand_y), 7)
        pygame.draw.circle(screen, self.skin_color, (int(left_hand_x), int(left_hand_y)), 8)
        pygame.draw.circle(screen, BLACK, (int(left_hand_x), int(left_hand_y)), 8, 2)
        
        # Right arm (adjusted for dribbling)
        right_shoulder_x = torso_x + self.torso_width // 2
        right_shoulder_y = torso_y + 5
        
        if self.has_ball:
            # Arm position for dribbling
            if self.dribble_style == "normal":
                right_elbow_x = right_shoulder_x + math.sin(math.radians(self.arm_angle - 45)) * self.arm_length // 2
                right_elbow_y = right_shoulder_y + 15
                right_hand_x = right_shoulder_x + math.sin(math.radians(self.arm_angle - 45)) * self.arm_length
                right_hand_y = right_shoulder_y + 25
            elif self.dribble_style == "through_legs":
                right_elbow_x = right_shoulder_x + math.sin(math.radians(self.arm_angle - 90)) * self.arm_length // 2
                right_elbow_y = right_shoulder_y + 20
                right_hand_x = right_shoulder_x + math.sin(math.radians(self.arm_angle - 90)) * self.arm_length
                right_hand_y = right_shoulder_y + 30
            elif self.dribble_style == "behind_back":
                right_elbow_x = right_shoulder_x - math.sin(math.radians(self.arm_angle)) * self.arm_length // 2
                right_elbow_y = right_shoulder_y + 15
                right_hand_x = right_shoulder_x - math.sin(math.radians(self.arm_angle)) * self.arm_length
                right_hand_y = right_shoulder_y + 25
        else:
            # Normal arm position
            right_elbow_x = right_shoulder_x + math.sin(math.radians(self.arm_angle - 90)) * self.arm_length // 2
            right_elbow_y = right_shoulder_y + 10
            right_hand_x = right_shoulder_x + math.sin(math.radians(self.arm_angle - 90)) * self.arm_length
            right_hand_y = right_shoulder_y + 20
            
        # Draw right arm
        pygame.draw.line(screen, self.skin_color, (right_shoulder_x, right_shoulder_y), (right_elbow_x, right_elbow_y), 8)
        pygame.draw.line(screen, self.skin_color, (right_elbow_x, right_elbow_y), (right_hand_x, right_hand_y), 7)
        pygame.draw.circle(screen, self.skin_color, (int(right_hand_x), int(right_hand_y)), 8)
        pygame.draw.circle(screen, BLACK, (int(right_hand_x), int(right_hand_y)), 8, 2)
        
        # Draw neck with thicker line
        pygame.draw.line(screen, self.skin_color, (neck_x, neck_y), (torso_x, torso_y), 10)
        
        # Draw head with better contrast
        pygame.draw.circle(screen, self.skin_color, (int(head_x), int(head_y)), self.head_radius + 2)
        pygame.draw.circle(screen, BLACK, (int(head_x), int(head_y)), self.head_radius + 2, 3)
        
        # Draw hair with better definition
        hair_rect = pygame.Rect(head_x - self.head_radius - 2, head_y - self.head_radius - 7, 
                               (self.head_radius + 2) * 2, 10)
        pygame.draw.rect(screen, self.hair_color, hair_rect)
        pygame.draw.rect(screen, BLACK, hair_rect, 2)
        
        # Draw face features with better visibility
        # Eyes
        eye_y = int(head_y - 2)
        if self.facing_right:
            # Left eye
            pygame.draw.circle(screen, WHITE, (int(head_x + 4), eye_y), 4)
            pygame.draw.circle(screen, BLACK, (int(head_x + 5), eye_y), 3)
            # Right eye
            pygame.draw.circle(screen, WHITE, (int(head_x - 4), eye_y), 4)
            pygame.draw.circle(screen, BLACK, (int(head_x - 3), eye_y), 3)
        else:
            # Left eye
            pygame.draw.circle(screen, WHITE, (int(head_x - 4), eye_y), 4)
            pygame.draw.circle(screen, BLACK, (int(head_x - 5), eye_y), 3)
            # Right eye
            pygame.draw.circle(screen, WHITE, (int(head_x + 4), eye_y), 4)
            pygame.draw.circle(screen, BLACK, (int(head_x + 3), eye_y), 3)
            
        # Draw basketball when player has ball with better visibility
        if self.has_ball:
            # Ball position based on dribble style
            if self.dribble_style == "normal":
                ball_x = right_hand_x
                ball_y = right_hand_y - 5
            elif self.dribble_style == "through_legs":
                ball_x = torso_x
                ball_y = self.y - 10
            elif self.dribble_style == "behind_back":
                ball_x = torso_x - 20
                ball_y = torso_y + 10
                
            # Dribble animation
            if self.is_dribbling:
                ball_y += 8  # Ball moves down when dribbling
                
            # Draw basketball with better contrast
            pygame.draw.circle(screen, ORANGE, (int(ball_x), int(ball_y)), 10)
            pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), 10, 3)
            
            # Basketball lines with rotation and better visibility
            angle = math.radians(self.ball_rotation)
            end_x1 = ball_x + math.cos(angle) * 10
            end_y1 = ball_y + math.sin(angle) * 10
            end_x2 = ball_x - math.cos(angle) * 10
            end_y2 = ball_y - math.sin(angle) * 10
            pygame.draw.line(screen, BLACK, (end_x1, end_y1), (end_x2, end_y2), 2)
            
            # Horizontal line
            end_x3 = ball_x + math.cos(angle + math.pi/2) * 10
            end_y3 = ball_y + math.sin(angle + math.pi/2) * 10
            end_x4 = ball_x - math.cos(angle + math.pi/2) * 10
            end_y4 = ball_y - math.sin(angle + math.pi/2) * 10
            pygame.draw.line(screen, BLACK, (end_x3, end_y3), (end_x4, end_y4), 2)
            
    def draw(self, screen):
        """Draw character using realistic method"""
        self.draw_realistic(screen)
        
        # Draw character name
        font = pygame.font.Font(None, 20)
        name = self.character_type.name.replace("_", " ")
        name_text = font.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(int(self.x), int(self.y - 70)))
        screen.blit(name_text, name_rect)
        
        # Draw shoot power bar when charging
        if self.shoot_charging:
            bar_width = 40
            bar_height = 6
            bar_x = self.x - bar_width // 2
            bar_y = self.y - 60
            
            # Background
            pygame.draw.rect(screen, BLACK, (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
            
            # Power fill
            fill_width = int(bar_width * (self.shoot_power / 100))
            power_color = GREEN if self.shoot_power < 70 else YELLOW if self.shoot_power < 90 else RED
            pygame.draw.rect(screen, power_color, (bar_x, bar_y, fill_width, bar_height))
        
    def jump(self):
        if self.on_ground:
            self.vy = -self.jump_power
            self.on_ground = False
            
    def move_left(self):
        self.vx = -self.speed
        self.facing_right = False
        
    def move_right(self):
        self.vx = self.speed
        self.facing_right = True
        
    def draw(self, screen):
        # Draw character body
        body_rect = pygame.Rect(self.x - 15, self.y - 40, 30, 40)
        pygame.draw.rect(screen, self.color, body_rect)
        pygame.draw.rect(screen, BLACK, body_rect, 2)
        
        # Draw head
        head_center = (int(self.x), int(self.y - 50))
        pygame.draw.circle(screen, self.color, head_center, 12)
        pygame.draw.circle(screen, BLACK, head_center, 12, 2)
        
        # Draw eyes
        eye_y = int(self.y - 52)
        if self.facing_right:
            pygame.draw.circle(screen, WHITE, (int(self.x + 4), eye_y), 3)
            pygame.draw.circle(screen, BLACK, (int(self.x + 5), eye_y), 2)
        else:
            pygame.draw.circle(screen, WHITE, (int(self.x - 4), eye_y), 3)
            pygame.draw.circle(screen, BLACK, (int(self.x - 5), eye_y), 2)
        
        # Draw character name
        font = pygame.font.Font(None, 20)
        name = self.character_type.name.replace("_", " ")
        name_text = font.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(int(self.x), int(self.y - 70)))
        screen.blit(name_text, name_rect)
        
        # Draw shoot power bar when charging
        if self.shoot_charging:
            bar_width = 40
            bar_height = 6
            bar_x = self.x - bar_width // 2
            bar_y = self.y - 60
            
            # Background
            pygame.draw.rect(screen, BLACK, (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
            
            # Power fill
            fill_width = int(bar_width * (self.shoot_power / 100))
            power_color = GREEN if self.shoot_power < 70 else YELLOW if self.shoot_power < 90 else RED
            pygame.draw.rect(screen, power_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw basketball when player has ball
        if self.has_ball:
            ball_y = self.y - 25
            if self.is_dribbling:
                ball_y += 5  # Ball moves up when dribbling
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(ball_y)), 8)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(ball_y)), 8, 2)
    
    def draw_with_offset(self, screen, cam_x, cam_y):
        """Draw player with camera offset using realistic method"""
        # Temporarily modify position for drawing
        original_x = self.x
        original_y = self.y
        self.x += cam_x
        self.y += cam_y
        
        # Draw realistic character
        self.draw_realistic(screen)
        
        # Draw character name
        font = pygame.font.Font(None, 20)
        name = self.character_type.name.replace("_", " ")
        name_text = font.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(int(self.x), int(self.y - 70)))
        screen.blit(name_text, name_rect)
        
        # Draw shoot power bar when charging
        if self.shoot_charging:
            bar_width = 40
            bar_height = 6
            bar_x = self.x - bar_width // 2
            bar_y = self.y - 60
            
            # Background
            pygame.draw.rect(screen, BLACK, (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
            
            # Power fill
            fill_width = int(bar_width * (self.shoot_power / 100))
            power_color = GREEN if self.shoot_power < 70 else YELLOW if self.shoot_power < 90 else RED
            pygame.draw.rect(screen, power_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Restore original position
        self.x = original_x
        self.y = original_y

class NBAOpponent(Player):
    def __init__(self, x, y, nba_player):
        super().__init__(x, y, CharacterType.WARRIOR, False)  # Base character
        self.nba_player = nba_player
        self.set_nba_stats()
        self.ai_timer = 0
        self.ai_action_timer = 0
        
    def set_nba_stats(self):
        """Set stats based on NBA player"""
        nba_stats = {
            NBAPlayer.MICHAEL_JORDAN: {"speed": 6, "jump": 16, "shoot": 20, "defense": 8, "color": RED},
            NBAPlayer.COOPER_FLAGG: {"speed": 5, "jump": 14, "shoot": 16, "defense": 9, "color": BLUE},
            NBAPlayer.REGGIE_MILLER: {"speed": 4, "jump": 13, "shoot": 18, "defense": 6, "color": YELLOW},
            NBAPlayer.LEBRON_JAMES: {"speed": 5, "jump": 15, "shoot": 17, "defense": 9, "color": (255, 140, 0)},
            NBAPlayer.KOBE_BRYANT: {"speed": 5, "jump": 15, "shoot": 19, "defense": 8, "color": PURPLE},
            NBAPlayer.STEPH_CURRY: {"speed": 5, "jump": 13, "shoot": 20, "defense": 5, "color": BLUE},
            NBAPlayer.SHAQUILLE_ONEAL: {"speed": 3, "jump": 12, "shoot": 14, "defense": 10, "color": BLACK},
            NBAPlayer.KEVIN_DURANT: {"speed": 5, "jump": 16, "shoot": 19, "defense": 7, "color": (0, 100, 255)}
        }
        
        stat = nba_stats[self.nba_player]
        self.base_speed = stat["speed"]
        self.base_jump = stat["jump"]
        self.shoot_skill = stat["shoot"]
        self.defense = stat["defense"]
        self.color = stat["color"]
        self.speed = self.base_speed
        self.jump_power = self.base_jump
        
    def ai_update(self, ball, player, hoop_x, hoop_y):
        """AI behavior for opponent"""
        self.ai_timer += 1
        
        # Get ball if not held
        if ball.held_by is None and not self.has_ball:
            # Move towards ball
            if ball.x < self.x - 20:
                self.move_left()
            elif ball.x > self.x + 20:
                self.move_right()
                
            # Try to grab ball
            dist_to_ball = math.sqrt((ball.x - self.x)**2 + (ball.y - self.y)**2)
            if dist_to_ball < 30:
                ball.held_by = self
                self.has_ball = True
                
        # If has ball, try to score
        elif self.has_ball:
            # Move towards hoop
            if hoop_x < self.x - 50:
                self.move_left()
            elif hoop_x > self.x + 50:
                self.move_right()
                
            # Shoot if close enough to hoop
            dist_to_hoop = math.sqrt((hoop_x - self.x)**2 + (hoop_y - self.y)**2)
            if dist_to_hoop < 300 and random.random() < 0.02:
                self.shoot_ball(ball, hoop_x, hoop_y)
                
        # Defend if player has ball
        elif player.has_ball:
            # Move towards player
            if player.x < self.x - 40:
                self.move_left()
            elif player.x > self.x + 40:
                self.move_right()
                
            # Try to steal
            dist_to_player = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
            if dist_to_player < 40 and random.random() < 0.01:
                # Steal attempt
                if random.random() < 0.3:  # 30% steal chance
                    player.has_ball = False
                    ball.held_by = self
                    self.has_ball = True
                    
        # Random jump
        if self.on_ground and random.random() < 0.01:
            self.jump()
            
    def shoot_ball(self, ball, hoop_x, hoop_y):
        """AI shoot ball"""
        if self.has_ball:
            # Calculate shot with some randomness based on skill
            accuracy = self.shoot_skill / 20.0
            target_x = hoop_x + random.randint(-50, 50) * (1 - accuracy)
            target_y = hoop_y + random.randint(-30, 30) * (1 - accuracy)
            
            ball.held_by = None
            self.has_ball = False
            ball.shoot(target_x, target_y, self.shoot_skill * 5)
            
    def draw(self, screen):
        super().draw(screen)
        
        # Draw NBA player name
        font = pygame.font.Font(None, 20)
        nba_name = self.nba_player.name.replace("_", " ")
        nba_text = font.render(nba_name, True, YELLOW)
        nba_rect = nba_text.get_rect(center=(int(self.x), int(self.y - 85)))
        screen.blit(nba_text, nba_rect)

class Hoop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 10
        self.rim_height = 15
        
    def check_score(self, ball):
        """Check if ball goes through hoop"""
        # Check if ball passes through hoop area
        if (abs(ball.x - self.x) < self.width // 2 and 
            abs(ball.y - self.y) < 20 and
            ball.vy > 0):  # Ball must be moving downward
            return True
        return False
        
    def draw(self, screen):
        # Draw backboard
        backboard_rect = pygame.Rect(self.x + 30, self.y - 60, 10, 80)
        pygame.draw.rect(screen, WHITE, backboard_rect)
        pygame.draw.rect(screen, BLACK, backboard_rect, 2)
        
        # Backboard square
        pygame.draw.rect(screen, WHITE, (self.x + 25, self.y - 40, 20, 20), 2)
        
        # Draw rim
        pygame.draw.ellipse(screen, HOOP_ORANGE, 
                          (self.x - self.width // 2, self.y - self.rim_height // 2, 
                           self.width, self.rim_height), 3)
        
        # Draw net
        net_points = []
        for i in range(8):
            x = self.x - self.width // 2 + i * (self.width // 7)
            net_points.append((x, self.y))
            net_points.append((x - 5, self.y + 30))
            
        for i in range(0, len(net_points) - 2, 2):
            pygame.draw.line(screen, WHITE, net_points[i], net_points[i + 1], 2)
    
    def draw_with_offset(self, screen, cam_x, cam_y):
        """Draw hoop with camera offset"""
        # Draw at offset position
        draw_x = self.x + cam_x
        draw_y = self.y + cam_y
        
        # Draw backboard
        backboard_rect = pygame.Rect(draw_x + 30, draw_y - 60, 10, 80)
        pygame.draw.rect(screen, WHITE, backboard_rect)
        pygame.draw.rect(screen, BLACK, backboard_rect, 2)
        
        # Backboard square
        pygame.draw.rect(screen, WHITE, (draw_x + 25, draw_y - 40, 20, 20), 2)
        
        # Draw rim
        pygame.draw.ellipse(screen, HOOP_ORANGE, 
                          (draw_x - self.width // 2, draw_y - self.rim_height // 2, 
                           self.width, self.rim_height), 3)
        
        # Draw net
        net_points = []
        for i in range(8):
            x = draw_x - self.width // 2 + i * (self.width // 7)
            net_points.append((x, draw_y))
            net_points.append((x - 5, draw_y + 30))
            
        for i in range(0, len(net_points) - 2, 2):
            pygame.draw.line(screen, WHITE, net_points[i], net_points[i + 1], 2)

class EpicBasketballGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏀 EPIC BASKETBALL 1v1 - HALF COURT SHOWDOWN! 🏀")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_huge = pygame.font.Font(None, 72)
        
        # Game objects
        self.player = None
        self.opponent = None
        self.ball = None
        self.hoop = None
        
        # Selections
        self.selected_character = None
        self.selected_opponent = None
        
        # Score
        self.player_score = 0
        self.opponent_score = 0
        self.max_score = 11  # Win by 2
        
        # Game time
        self.game_timer = 0
        self.shot_clock = 24  # 24 second shot clock
        
        # Visual effects
        self.particles = []
        self.screen_shake = 0
        self.celebration_timer = 0
        
    def create_particle(self, x, y, color, count=10):
        """Create celebration particles"""
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-8, -2),
                'color': color,
                'life': random.randint(30, 60),
                'size': random.randint(2, 6)
            }
            self.particles.append(particle)
            
    def update_particles(self):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self):
        """Draw particle effects"""
        for particle in self.particles:
            alpha = particle['life'] / 60
            size = int(particle['size'] * alpha)
            if size > 0:
                pygame.draw.circle(self.screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), size)
    
    def draw_court(self):
        """Draw professional basketball court with crystal clear graphics"""
        # Draw wood floor with realistic texture
        wood_base = (210, 180, 140)  # Light wood color
        self.screen.fill(wood_base)
        
        # Add wood grain texture
        for i in range(0, SCREEN_WIDTH, 4):
            for j in range(0, SCREEN_HEIGHT, 8):
                wood_variation = (random.randint(-10, 10), random.randint(-10, 10), random.randint(-5, 5))
                wood_color = tuple(max(0, min(255, wood_base[k] + wood_variation[k])) for k in range(3))
                pygame.draw.rect(self.screen, wood_color, (i, j, 4, 8))
        
        # Court boundary (clear white lines)
        pygame.draw.rect(self.screen, WHITE, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150), 4)
        
        # Half court line
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH // 2, 50), 
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100), 4)
        
        # Center court circle
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 80, 4)
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 75, 2)
        
        # Three-point line (left side)
        pygame.draw.arc(self.screen, WHITE, (50, SCREEN_HEIGHT // 2 - 120, 240, 240), 
                      -math.pi/2, math.pi/2, 4)
        
        # Three-point line (right side) 
        pygame.draw.arc(self.screen, WHITE, (SCREEN_WIDTH - 290, SCREEN_HEIGHT // 2 - 120, 240, 240), 
                      math.pi/2, 3*math.pi/2, 4)
        
        # Free throw circle (left)
        pygame.draw.circle(self.screen, WHITE, (200, SCREEN_HEIGHT // 2), 60, 3)
        pygame.draw.circle(self.screen, WHITE, (200, SCREEN_HEIGHT // 2), 55, 2)
        
        # Free throw circle (right)
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2), 60, 3)
        pygame.draw.circle(self.screen, WHITE, (SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2), 55, 2)
        
        # Free throw line (left)
        pygame.draw.line(self.screen, WHITE, (140, SCREEN_HEIGHT // 2 - 60), 
                        (260, SCREEN_HEIGHT // 2 - 60), 3)
        
        # Free throw line (right)
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH - 260, SCREEN_HEIGHT // 2 - 60), 
                        (SCREEN_WIDTH - 140, SCREEN_HEIGHT // 2 - 60), 3)
        
        # Lane lines (left)
        pygame.draw.line(self.screen, WHITE, (140, SCREEN_HEIGHT // 2 - 60), 
                        (140, SCREEN_HEIGHT // 2 + 60), 3)
        pygame.draw.line(self.screen, WHITE, (260, SCREEN_HEIGHT // 2 - 60), 
                        (260, SCREEN_HEIGHT // 2 + 60), 3)
        
        # Lane lines (right)
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH - 260, SCREEN_HEIGHT // 2 - 60), 
                        (SCREEN_WIDTH - 260, SCREEN_HEIGHT // 2 + 60), 3)
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH - 140, SCREEN_HEIGHT // 2 - 60), 
                        (SCREEN_WIDTH - 140, SCREEN_HEIGHT // 2 + 60), 3)
        
        # Baseline (left)
        pygame.draw.line(self.screen, WHITE, (50, SCREEN_HEIGHT - 100), 
                        (50, 50), 4)
        
        # Baseline (right)
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 100), 
                        (SCREEN_WIDTH - 50, 50), 4)
        
        # Add court text
        font = pygame.font.Font(None, 36)
        court_text = font.render("1v1 BASKETBALL", True, (100, 100, 100))
        text_rect = court_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(court_text, text_rect)
        
        # Free throw line
        pygame.draw.line(self.screen, COURT_LINE, (200, SCREEN_HEIGHT - 100), 
                        (200, SCREEN_HEIGHT - 300), 3)
        
        # Paint area
        pygame.draw.rect(self.screen, COURT_LINE, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 250, 200, 150), 3)
        
        # Free throw circle
        pygame.draw.arc(self.screen, COURT_LINE, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 300, 100, 100), 0, math.pi, 3)
        
        # Three point line
        pygame.draw.arc(self.screen, COURT_LINE, (50, SCREEN_HEIGHT - 350, 300, 300), 
                       0, math.pi, 3)
        
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_huge.render("🏀 EPIC BASKETBALL 🏀", True, ORANGE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_large.render("1v1 HALF COURT SHOWDOWN!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        options = [
            "Press SPACE to Start",
            "Press C for Character Select",
            "Press Q to Quit"
        ]
        
        for i, option in enumerate(options):
            text = self.font_medium.render(option, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * 50))
            self.screen.blit(text, text_rect)
            
        # NBA Players showcase
        showcase_text = self.font_small.render("Play as: Warrior, Ninja, Wizard, Robot, Dragon, Astronaut, Pirate, Superhero", True, YELLOW)
        showcase_rect = showcase_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(showcase_text, showcase_rect)
        
        nba_text = self.font_small.render("VS: Michael Jordan, Cooper Flagg, Reggie Miller, LeBron James, Kobe Bryant, Steph Curry, Shaq, Kevin Durant", True, RED)
        nba_rect = nba_text.get_rect(center=(SCREEN_WIDTH // 2, 580))
        self.screen.blit(nba_text, nba_rect)
        
    def draw_character_select(self):
        """Draw character selection screen"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("SELECT YOUR CHARACTER!", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Draw character options
        characters = list(CharacterType)
        for i, char in enumerate(characters):
            x = 150 + (i % 4) * 250
            y = 150 + (i // 4) * 200
            
            # Character preview
            preview_rect = pygame.Rect(x - 40, y - 40, 80, 80)
            color = {
                CharacterType.WARRIOR: RED,
                CharacterType.NINJA: BLACK,
                CharacterType.WIZARD: PURPLE,
                CharacterType.ROBOT: GRAY,
                CharacterType.DRAGON: (255, 140, 0),
                CharacterType.ASTRONAUT: BLUE,
                CharacterType.PIRATE: (101, 67, 33),
                CharacterType.SUPERHERO: (255, 215, 0)
            }[char]
            
            pygame.draw.rect(self.screen, color, preview_rect)
            pygame.draw.rect(self.screen, WHITE, preview_rect, 3)
            
            # Character name
            name_text = self.font_small.render(char.name.replace("_", " "), True, WHITE)
            name_rect = name_text.get_rect(center=(x, y + 60))
            self.screen.blit(name_text, name_rect)
            
            # Selection indicator
            if self.selected_character == char:
                pygame.draw.rect(self.screen, YELLOW, preview_rect, 5)
                
        # Instructions
        inst_text = self.font_medium.render("Click to select, Press ENTER to continue", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(inst_text, inst_rect)
        
    def draw_opponent_select(self):
        """Draw opponent selection screen"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("SELECT YOUR OPPONENT!", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Draw NBA player options
        players = list(NBAPlayer)
        for i, player in enumerate(players):
            x = 150 + (i % 4) * 250
            y = 150 + (i // 4) * 200
            
            # Player preview
            preview_rect = pygame.Rect(x - 40, y - 40, 80, 80)
            color = {
                NBAPlayer.MICHAEL_JORDAN: RED,
                NBAPlayer.COOPER_FLAGG: BLUE,
                NBAPlayer.REGGIE_MILLER: YELLOW,
                NBAPlayer.LEBRON_JAMES: (255, 140, 0),
                NBAPlayer.KOBE_BRYANT: PURPLE,
                NBAPlayer.STEPH_CURRY: BLUE,
                NBAPlayer.SHAQUILLE_ONEAL: BLACK,
                NBAPlayer.KEVIN_DURANT: (0, 100, 255)
            }[player]
            
            pygame.draw.rect(self.screen, color, preview_rect)
            pygame.draw.rect(self.screen, WHITE, preview_rect, 3)
            
            # Player name
            name_text = self.font_small.render(player.name.replace("_", " "), True, WHITE)
            name_rect = name_text.get_rect(center=(x, y + 60))
            self.screen.blit(name_text, name_rect)
            
            # Selection indicator
            if self.selected_opponent == player:
                pygame.draw.rect(self.screen, YELLOW, preview_rect, 5)
                
        # Instructions
        inst_text = self.font_medium.render("Click to select, Press ENTER to start game!", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(inst_text, inst_rect)
        
    def draw_game(self):
        """Draw game screen with camera following player"""
        # Calculate camera offset for player-centered view
        camera_offset_x = SCREEN_WIDTH // 2 - self.player.x
        camera_offset_y = SCREEN_HEIGHT // 2 - self.player.y
        
        # Apply slight angle effect based on player movement
        angle_offset = self.player.vx * 2  # Lean when moving
        
        # Draw court with camera offset
        self.draw_court_with_offset(camera_offset_x, camera_offset_y, angle_offset)
        
        # Draw game objects with camera offset
        self.hoop.draw_with_offset(self.screen, camera_offset_x, camera_offset_y)
        self.ball.draw_with_offset(self.screen, camera_offset_x, camera_offset_y)
        self.player.draw_with_offset(self.screen, camera_offset_x, camera_offset_y)
        self.opponent.draw_with_offset(self.screen, camera_offset_x, camera_offset_y)
        
        # Draw particles (no camera offset)
        self.draw_particles()
        
        # Draw UI (no camera offset)
        self.draw_game_ui()
        
        # Apply screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            
    def draw_court_with_offset(self, cam_x, cam_y, angle):
        """Draw court with camera offset and angle"""
        # Simple court drawing with offset
        for i in range(0, SCREEN_WIDTH, 2):
            for j in range(0, SCREEN_HEIGHT, 2):
                # Apply angle transformation
                offset_x = i + cam_x + math.sin(angle * 0.1) * (j - SCREEN_HEIGHT//2) * 0.05
                offset_y = j + cam_y
                color = COURT_GREEN if (i // 2 + j // 2) % 2 == 0 else BROWN
                self.screen.set_at((int(offset_x), int(offset_y)), color)
                
    def draw_with_offset(self, screen, cam_x, cam_y):
        """Draw object with camera offset"""
        # Draw at offset position
        draw_x = self.x + cam_x
        draw_y = self.y + cam_y
        
        # Call original draw method with offset
        if hasattr(self, 'draw'):
            # Temporarily modify position for drawing
            original_x = self.x
            original_y = self.y
            self.x = draw_x
            self.y = draw_y
            self.draw(screen)
            # Restore original position
            self.x = original_x
            self.y = original_y
            
    def draw_game_ui(self):
        """Draw game UI"""
        # Score
        score_text = self.font_large.render(f"Player: {self.player_score}  -  {self.opponent_score} : Opponent", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(score_text, score_rect)
        
        # Shot clock
        shot_clock_color = RED if self.shot_clock < 5 else WHITE
        shot_text = self.font_medium.render(f"Shot Clock: {self.shot_clock}", True, shot_clock_color)
        self.screen.blit(shot_text, (SCREEN_WIDTH // 2 - 60, 70))
        
        # Controls
        controls = [
            "WASD/Arrows: Move",
            "SPACE: Jump",
            "Hold X: Charge Shot",
            "P: Pause"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, WHITE)
            self.screen.blit(control_text, (10, 10 + i * 25))
            
        # Celebration message
        if self.celebration_timer > 0:
            celeb_text = self.font_huge.render("SCORE! 🏀", True, YELLOW)
            celeb_rect = celeb_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(celeb_text, celeb_rect)
            self.celebration_timer -= 1
            
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        # Winner announcement
        if self.player_score > self.opponent_score:
            winner_text = "YOU WIN! 🏆"
            winner_color = YELLOW
        else:
            winner_text = "OPPONENT WINS! 🏆"
            winner_color = RED
            
        winner = self.font_huge.render(winner_text, True, winner_color)
        winner_rect = winner.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(winner, winner_rect)
        
        # Final score
        score_text = self.font_large.render(f"Final Score: {self.player_score} - {self.opponent_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # Options
        options = [
            "Press SPACE to play again",
            "Press M for main menu",
            "Press Q to quit"
        ]
        
        for i, option in enumerate(options):
            text = self.font_medium.render(option, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400 + i * 40))
            self.screen.blit(text, text_rect)
            
    def handle_menu_click(self, pos):
        """Handle mouse clicks in menu"""
        x, y = pos
        
        # Check character selection
        if self.state == GameState.CHARACTER_SELECT:
            characters = list(CharacterType)
            for i, char in enumerate(characters):
                button_x = 150 + (i % 4) * 250
                button_y = 150 + (i // 4) * 200
                
                if (abs(x - button_x) < 40 and abs(y - button_y) < 40):
                    self.selected_character = char
                    
        # Check opponent selection
        elif self.state == GameState.OPPONENT_SELECT:
            players = list(NBAPlayer)
            for i, player in enumerate(players):
                button_x = 150 + (i % 4) * 250
                button_y = 150 + (i // 4) * 200
                
                if (abs(x - button_x) < 40 and abs(y - button_y) < 40):
                    self.selected_opponent = player
                    
    def start_game(self):
        """Start the game with selected characters"""
        if self.selected_character and self.selected_opponent:
            # Create game objects
            self.player = Player(300, SCREEN_HEIGHT - 200, self.selected_character, True)
            self.opponent = NBAOpponent(900, SCREEN_HEIGHT - 200, self.selected_opponent)
            self.ball = Basketball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.hoop = Hoop(SCREEN_WIDTH - 150, 200)
            
            # Reset score
            self.player_score = 0
            self.opponent_score = 0
            self.game_timer = 0
            self.shot_clock = 24
            
            # Start game
            self.state = GameState.PLAYING
            
    def update_game(self):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
            
        # Update game timer
        self.game_timer += 1
        
        # Update shot clock
        if self.game_timer % 60 == 0:  # Every second
            self.shot_clock -= 1
            if self.shot_clock <= 0:
                self.shot_clock = 24
                # Turnover - switch ball possession
                if self.player.has_ball:
                    self.player.has_ball = False
                    self.ball.held_by = None
                elif self.opponent.has_ball:
                    self.opponent.has_ball = False
                    self.ball.held_by = None
                    
        # Update players
        self.player.update()
        self.opponent.update()
        
        # Update ball
        if self.ball.held_by:
            # Ball follows player with better positioning
            if self.ball.held_by == self.player:
                self.ball.x = self.player.x
                self.ball.y = self.player.y - 30
                # Add dribble effect
                if self.player.is_dribbling:
                    self.ball.y += 5
            else:
                self.ball.x = self.opponent.x
                self.ball.y = self.opponent.y - 30
                # Add dribble effect
                if self.opponent.is_dribbling:
                    self.ball.y += 5
        else:
            # Enhanced ball physics
            self.ball.update()
            
            # Better court boundaries
            if self.ball.x < 50:
                self.ball.x = 50
                self.ball.vx *= -0.8
            elif self.ball.x > SCREEN_WIDTH - 50:
                self.ball.x = SCREEN_WIDTH - 50
                self.ball.vx *= -0.8
                
            # Ball goes out of bounds - reset possession
            if self.ball.y > SCREEN_HEIGHT - 50 or self.ball.y < 0:
                self.reset_ball_possession()
                
        # Enhanced AI update
        self.opponent.ai_update(self.ball, self.player, self.hoop.x, self.hoop.y)
        
        # Check for scoring with better detection
        if self.hoop.check_score(self.ball):
            if self.ball.held_by == self.player or (self.player.has_ball and self.ball.held_by is None):
                self.player_score += 1
                self.create_particle(self.hoop.x, self.hoop.y, YELLOW, 30)
                self.screen_shake = 15
                self.celebration_timer = 60
            else:
                self.opponent_score += 1
                self.create_particle(self.hoop.x, self.hoop.y, RED, 30)
                self.screen_shake = 15
                
            # Reset ball with better positioning
            self.reset_ball_possession()
            self.shot_clock = 24
            
        # Check for winner
        if self.player_score >= self.max_score:
            self.state = GameState.GAME_OVER
        elif self.opponent_score >= self.max_score:
            self.state = GameState.GAME_OVER
            
    def reset_ball_possession(self):
        """Reset ball possession after score or out of bounds"""
        self.ball = Basketball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player.has_ball = False
        self.opponent.has_ball = False
        
        # Random possession after reset
        if random.random() < 0.5:
            self.player.has_ball = True
            self.ball.held_by = self.player
        else:
            self.opponent.has_ball = True
            self.ball.held_by = self.opponent
                
        # Update particles
        self.update_particles()
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.CHARACTER_SELECT
                    elif event.key == pygame.K_c:
                        self.state = GameState.CHARACTER_SELECT
                    elif event.key == pygame.K_q:
                        self.running = False
                        
                elif self.state == GameState.CHARACTER_SELECT:
                    if event.key == pygame.K_RETURN and self.selected_character:
                        self.state = GameState.OPPONENT_SELECT
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.OPPONENT_SELECT:
                    if event.key == pygame.K_RETURN and self.selected_opponent:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.CHARACTER_SELECT
                        
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.CHARACTER_SELECT
                        self.selected_character = None
                        self.selected_opponent = None
                    elif event.key == pygame.K_m:
                        self.state = GameState.MENU
                        self.selected_character = None
                        self.selected_opponent = None
                    elif event.key == pygame.K_q:
                        self.running = False
                        
            elif event.type == pygame.KEYUP:
                if self.state == GameState.PLAYING:
                    if event.key == pygame.K_x:
                        # Release shot
                        if self.player.shoot_charging and self.player.has_ball:
                            self.player.shoot_ball(self.ball, self.hoop.x, self.hoop.y)
                            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state in [GameState.CHARACTER_SELECT, GameState.OPPONENT_SELECT]:
                    self.handle_menu_click(event.pos)
                    
        # Handle continuous key presses for game
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            
            # Player movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
                
            # Shoot charging
            if keys[pygame.K_x] and self.player.has_ball:
                if not self.player.shoot_charging:
                    self.player.shoot_charging = True
                    self.player.shoot_power = 0
                else:
                    self.player.shoot_power = min(100, self.player.shoot_power + 2)
                    
    def shoot_ball(self, player, ball, target_x, target_y):
        """Handle shooting mechanics"""
        if player.has_ball:
            ball.held_by = None
            player.has_ball = False
            ball.shoot(target_x, target_y, player.shoot_power * player.shoot_skill / 10)
            player.shoot_power = 0
            player.shoot_charging = False
            self.shot_clock = 24
            
    def draw(self):
        """Draw everything"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.CHARACTER_SELECT:
            self.draw_character_select()
        elif self.state == GameState.OPPONENT_SELECT:
            self.draw_opponent_select()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            # Draw pause overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font_huge.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)
            
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    game = EpicBasketballGame()
    game.run()

if __name__ == "__main__":
    main()
