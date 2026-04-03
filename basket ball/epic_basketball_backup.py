#!/usr/bin/env python3
"""
🏀 EPIC BASKETBALL 1v1 - HALF COURT SHOWDOWN! 🏀
Play as your character vs legendary NBA players!
Michael Jordan, Cooper Flagg, Reggie Miller and more!
"""

import pygame
import math
import random
import sys
from enum import Enum

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
COURT_GREEN = (25, 102, 50)
COURT_LINE = (240, 240, 240)
HOOP_ORANGE = (255, 69, 0)

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
        end_y3 = self.y + math.sin(math.radians(angle + 90)) * self.radius
        end_x4 = self.x - math.cos(math.radians(angle + 90)) * self.radius
        end_y4 = self.y - math.sin(math.radians(angle + 90)) * self.radius
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
        self.has_ball = False
        self.shoot_power = 0
        self.shoot_charging = False
        
        # Animation
        self.animation_frame = 0
        self.facing_right = True
        
    def set_stats(self):
        """Set stats based on character type"""
        stats = {
            CharacterType.WARRIOR: {"speed": 4, "jump": 12, "shoot": 15, "defense": 8, "color": RED},
            CharacterType.NINJA: {"speed": 6, "jump": 15, "shoot": 12, "defense": 5, "color": BLACK},
            CharacterType.WIZARD: {"speed": 5, "jump": 14, "shoot": 18, "defense": 6, "color": PURPLE},
            CharacterType.ROBOT: {"speed": 3, "jump": 10, "shoot": 20, "defense": 10, "color": GRAY},
            CharacterType.DRAGON: {"speed": 5, "jump": 18, "shoot": 16, "defense": 7, "color": (255, 140, 0)},
            CharacterType.ASTRONAUT: {"speed": 5, "jump": 16, "shoot": 14, "defense": 6, "color": BLUE},
            CharacterType.PIRATE: {"speed": 4, "jump": 13, "shoot": 13, "defense": 7, "color": BROWN},
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
        else:
            self.on_ground = False
            
        # Boundaries
        self.x = max(20, min(SCREEN_WIDTH - 20, self.x))
        
        # Friction
        self.vx *= 0.9
        
        # Animation
        self.animation_frame += 1
        
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
        # Backboard square
        pygame.draw.rect(self.screen, WHITE, (self.x + 25, self.y - 40, 20, 20), 2)        backboard_rect = pygame.Rect(self.x + 30, self.y - 60, 10, 80)
        pygame.draw.rect(screen, WHITE, backboard_rect)
        pygame.draw.rect(screen, BLACK, backboard_rect, 2)
        
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
        """Draw basketball court"""
        # Court background
        # Wood floor effect
        for i in range(0, SCREEN_WIDTH, 80):
            wood_color = (40 + i % 20, 25 + i % 15, 15 + i % 10)
            pygame.draw.rect(self.screen, wood_color, (i, 0, 80, SCREEN_HEIGHT))        self.screen.fill(COURT_GREEN)
        
        # Court lines
        pygame.draw.rect(self.screen, COURT_LINE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100), 3)
        
        # Half court line
        pygame.draw.line(self.screen, COURT_LINE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100), 
                        (SCREEN_WIDTH // 2, 0), 3)
        
        # Free throw line
        pygame.draw.line(self.screen, COURT_LINE, (200, SCREEN_HEIGHT - 100), 
                        (200, SCREEN_HEIGHT - 300), 3)
        
        # Center court circle
        pygame.draw.circle(self.screen, COURT_LINE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200), 60, 3)
        
        # Paint area
        pygame.draw.rect(self.screen, COURT_LINE, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 250, 200, 150), 3)
        
        # Free throw circle
        pygame.draw.arc(self.screen, COURT_LINE, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 300, 100, 100), 0, math.pi, 3)        # Three point line
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
                CharacterType.PIRATE: BROWN,
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
        """Draw game screen"""
        # Draw court
        self.draw_court_with_camera()
        
        # Draw game objects
        self.hoop.draw(self.screen)
        self.ball.draw(self.screen)
        self.player.draw(self.screen)
        self.opponent.draw(self.screen)
        
        # Draw particles
        self.draw_particles()
        
        # Draw UI
        self.draw_game_ui()
        
        # Apply screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            
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
        self.hoop = Hoop(750, 250)            
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
            # Ball follows player
            if self.ball.held_by == self.player:
                self.ball.x = self.player.x
                self.ball.y = self.player.y - 30
            else:
                self.ball.x = self.opponent.x
                self.ball.y = self.opponent.y - 30
        else:
            self.ball.update()
            
        # AI update
        self.opponent.ai_update(self.ball, self.player, self.hoop.x, self.hoop.y)
        
        # Check for scoring
        if self.hoop.check_score(self.ball):
            if self.ball.held_by == self.player or (self.player.has_ball and self.ball.held_by is None):
                self.player_score += 1
                self.create_particle(self.hoop.x, self.hoop.y, YELLOW, 20)
                self.screen_shake = 10
                self.celebration_timer = 60
            else:
                self.opponent_score += 1
                self.create_particle(self.hoop.x, self.hoop.y, RED, 20)
                
            # Reset ball
            self.ball = Basketball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.player.has_ball = False
            self.opponent.has_ball = False
            self.shot_clock = 24
            
            # Check for winner
            if self.player_score >= self.max_score or self.opponent_score >= self.max_score:
                self.state = GameState.GAME_OVER
                
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
