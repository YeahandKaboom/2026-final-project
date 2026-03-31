#!/usr/bin/env python3
"""
VOLCANO ADVENTURE - Mine Rubies & Battle Rock Monsters!
Epic adventure game with village, volcano exploration, and hidden caves!
"""

import pygame
import math
import random
import sys
from enum import Enum
from collections import defaultdict

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
RUBY_RED = (224, 17, 95)
LAVA_RED = (255, 100, 0)
VOLCANO_BROWN = (101, 67, 33)
VOLCANO_RED = (255, 50, 0)
SKY_BLUE = (135, 206, 235)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
CAVE_BLACK = (20, 20, 30)
ROCK_GRAY = (105, 105, 105)

# Game states
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    SHOP = 2
    CAVE = 3
    VOLCANO = 4

# Player states
class PlayerState(Enum):
    OVERWORLD = 0
    IN_VOLCANO = 1
    IN_CAVE = 2

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4
        self.jump_power = 10
        self.gravity = 0.5
        self.max_fall_speed = 12
        self.on_ground = False
        
        # State
        self.state = PlayerState.OVERWORLD
        
        # Inventory
        self.rubies = 0
        self.gold = 0
        self.pickaxe_power = 1
        self.health = 100
        self.max_health = 100
        
    def update(self, keys, world):
        # Movement based on state
        if self.state == PlayerState.OVERWORLD:
            target_vel_x = 0
            target_vel_y = 0
            
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                target_vel_x = -self.speed
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                target_vel_x = self.speed
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                target_vel_y = -self.speed
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                target_vel_y = self.speed
                
            self.vel_x = target_vel_x
            self.vel_y = target_vel_y
            
        elif self.state == PlayerState.IN_VOLCANO:
            # Slower movement in volcano
            target_vel_x = 0
            target_vel_y = 0
            
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                target_vel_x = -self.speed * 0.7
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                target_vel_x = self.speed * 0.7
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                target_vel_y = -self.speed * 0.7
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                target_vel_y = self.speed * 0.7
                
            self.vel_x = target_vel_x
            self.vel_y = target_vel_y
            
        elif self.state == PlayerState.IN_CAVE:
            # Normal movement in cave
            target_vel_x = 0
            target_vel_y = 0
            
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                target_vel_x = -self.speed
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                target_vel_x = self.speed
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                target_vel_y = -self.speed
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                target_vel_y = self.speed
                
            self.vel_x = target_vel_x
            self.vel_y = target_vel_y
            
        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed
                
        # Move
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # World collision
        self.resolve_collisions(world)
        
        self.x = self.rect.x
        self.y = self.rect.y
        
    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            
    def resolve_collisions(self, world):
        self.on_ground = False
        
        # Ground collision
        for x in range(self.rect.left // 40, self.rect.right // 40 + 1):
            for y in range(self.rect.top // 40, self.rect.bottom // 40 + 1):
                if 0 <= x < world.width and 0 <= y < world.height:
                    if world.blocks[x][y] != 0:  # Solid block
                        block_rect = pygame.Rect(x * 40, y * 40, 40, 40)
                        if self.rect.colliderect(block_rect):
                            if self.vel_y > 0:  # Falling
                                self.rect.bottom = block_rect.top
                                self.on_ground = True
                                self.vel_y = 0
                            elif self.vel_y < 0:  # Jumping
                                self.rect.top = block_rect.bottom
                                self.vel_y = 0
                            elif self.vel_x > 0:  # Moving right
                                self.rect.right = block_rect.left
                                self.vel_x = 0
                            elif self.vel_x < 0:  # Moving left
                                self.rect.left = block_rect.right
                                self.vel_x = 0
                            return
                            
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw player
        pygame.draw.rect(screen, BLUE, (draw_x, draw_y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, self.width, self.height), 2)
        
        # Draw face
        pygame.draw.circle(screen, WHITE, (draw_x + 8, draw_y + 8), 3)
        pygame.draw.circle(screen, WHITE, (draw_x + 22, draw_y + 8), 3)
        
        # Draw health bar
        health_rect = pygame.Rect(draw_x, draw_y - 15, 30, 5)
        pygame.draw.rect(screen, RED, health_rect)
        health_fill = pygame.Rect(draw_x, draw_y - 15, int(30 * self.health / self.max_health), 5)
        pygame.draw.rect(screen, GREEN, health_fill)

class Villager:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 35
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.animation_frame = 0
        self.dialogue = ""
        self.dialogue_timer = 0
        
    def update(self):
        self.animation_frame += 1
        if self.dialogue_timer > 0:
            self.dialogue_timer -= 1
            
    def set_dialogue(self, text):
        self.dialogue = text
        self.dialogue_timer = 180  # 3 seconds at 60 FPS
        
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw villager body
        pygame.draw.rect(screen, PINK, (draw_x, draw_y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, self.width, self.height), 2)
        
        # Draw face
        pygame.draw.circle(screen, WHITE, (draw_x + 8, draw_y + 10), 3)
        pygame.draw.circle(screen, WHITE, (draw_x + 17, draw_y + 10), 3)
        
        # Draw mining animation
        if self.animation_frame % 40 < 20:
            # Arm up
            pygame.draw.rect(screen, PINK, (draw_x + 22, draw_y + 15, 8, 3))
        else:
            # Arm down
            pygame.draw.rect(screen, PINK, (draw_x + 22, draw_y + 20, 8, 3))
            
        # Draw dialogue
        if self.dialogue_timer > 0:
            dialogue_text = pygame.font.Font(None, 20).render(self.dialogue, True, WHITE)
            dialogue_rect = dialogue_text.get_rect(center=(draw_x + self.width // 2, draw_y - 20))
            pygame.draw.rect(screen, BLACK, dialogue_rect.inflate(10, 5))
            pygame.draw.rect(screen, WHITE, dialogue_rect.inflate(10, 5), 2)
            screen.blit(dialogue_text, dialogue_rect)

class RockMonster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = 0
        self.speed = 1.5
        self.health = 50
        self.max_health = 50
        self.damage = 10
        self.attack_cooldown = 0
        self.animation_frame = 0
        
    def update(self, player):
        # Simple AI - chase player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < 200:  # Chase range
            # Move towards player
            if distance > 0:
                self.vel_x = (dx / distance) * self.speed
                self.vel_y = (dy / distance) * self.speed
        else:
            # Random movement
            if random.random() < 0.02:
                self.vel_x = random.uniform(-2, 2)
                self.vel_y = random.uniform(-2, 2)
                
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        self.animation_frame += 1
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
        
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw rock monster
        pygame.draw.rect(screen, ROCK_GRAY, (draw_x, draw_y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, self.width, self.height), 3)
        
        # Draw eyes (glowing red)
        eye_glow = self.animation_frame % 40 < 20
        eye_color = RED if eye_glow else DARK_RED
        pygame.draw.circle(screen, eye_color, (draw_x + 10, draw_y + 10), 5)
        pygame.draw.circle(screen, eye_color, (draw_x + 30, draw_y + 10), 5)
        
        # Draw health bar
        health_rect = pygame.Rect(draw_x, draw_y - 10, 40, 5)
        pygame.draw.rect(screen, RED, health_rect)
        health_fill = pygame.Rect(draw_x, draw_y - 10, int(40 * self.health / self.max_health), 5)
        pygame.draw.rect(screen, GREEN, health_fill)

class Ruby:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.collected = False
        self.animation_frame = 0
        self.glow_timer = 0
        
    def update(self):
        self.animation_frame += 1
        self.glow_timer += 1
        
    def draw(self, screen, camera_x, camera_y):
        if self.collected:
            return
            
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Glowing effect
        glow_size = self.size + int(5 * math.sin(self.glow_timer * 0.1))
        glow_color = (*RUBY_RED, 100)
        pygame.draw.circle(screen, glow_color, (draw_x, draw_y), glow_size)
        
        # Ruby core
        pygame.draw.circle(screen, RUBY_RED, (draw_x, draw_y), self.size)
        pygame.draw.circle(screen, (255, 100, 100), (draw_x, draw_y), self.size, 2)

class World:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.blocks = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.generate_world()
        
    def generate_world(self):
        # Generate terrain
        for x in range(self.width):
            height = int(15 + 3 * math.sin(x * 0.2) + random.randint(-2, 2))
            
            for y in range(self.height):
                if y >= self.height - height:
                    self.blocks[x][y] = 1  # Ground block
                else:
                    self.blocks[x][y] = 0  # Air
                    
        # Add volcano
        volcano_x = 35
        volcano_y = 10
        for x in range(volcano_x - 2, volcano_x + 3):
            for y in range(volcano_y, volcano_y + 8):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.blocks[x][y] = 2  # Volcano rock
                    
        # Add cave entrance
        cave_x = 40
        cave_y = self.height - 8
        for x in range(cave_x, cave_x + 3):
            for y in range(cave_y, cave_y + 3):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.blocks[x][y] = 0  # Cave entrance
                    
    def get_block_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.blocks[x][y]
        return 0
        
    def mine_block(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.blocks[x][y] == 1:  # Mine ground
                self.blocks[x][y] = 0
                return 1  # Ground block
            elif self.blocks[x][y] == 2:  # Mine volcano rock
                if random.random() < 0.3:  # 30% chance for ruby
                    return 3  # Ruby!
                else:
                    self.blocks[x][y] = 0
                    return 2  # Volcano rock
        return 0
        
    def draw(self, screen, camera_x, camera_y):
        # Draw blocks
        for x in range(self.width):
            for y in range(self.height):
                if self.blocks[x][y] != 0:
                    draw_x = x * 40 - camera_x
                    draw_y = y * 40 - camera_y
                    
                    if self.blocks[x][y] == 1:  # Ground
                        color = BROWN
                    elif self.blocks[x][y] == 2:  # Volcano rock
                        color = VOLCANO_BROWN
                    else:
                        color = GRAY
                        
                    pygame.draw.rect(screen, color, (draw_x, draw_y, 40, 40))
                    pygame.draw.rect(screen, BLACK, (draw_x, draw_y, 40, 40), 2)

class CaveWorld:
    def __init__(self):
        self.width = 20
        self.height = 15
        self.blocks = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.rubies = []
        self.monsters = []
        self.generate_cave()
        
    def generate_cave(self):
        # Generate cave walls
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.blocks[x][y] = 1  # Cave wall
                else:
                    self.blocks[x][y] = 0  # Empty
                    
        # Add some random walls
        for _ in range(15):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            self.blocks[x][y] = 1
            
        # Spawn rubies
        for _ in range(8):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            self.rubies.append(Ruby(x * 40 + 20, y * 40 + 20))
            
        # Spawn monsters
        for _ in range(3):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            self.monsters.append(RockMonster(x * 40 + 20, y * 40 + 20))
            
    def draw(self, screen):
        # Draw cave background
        screen.fill(CAVE_BLACK)
        
        # Draw cave walls
        for x in range(self.width):
            for y in range(self.height):
                if self.blocks[x][y] == 1:
                    pygame.draw.rect(screen, ROCK_GRAY, (x * 40, y * 40, 40, 40))
                    pygame.draw.rect(screen, BLACK, (x * 40, y * 40, 40, 40), 2)
                    
        # Draw rubies
        for ruby in self.rubies:
            if not ruby.collected:
                ruby.draw(screen, 0, 0)
                
        # Draw monsters
        for monster in self.monsters:
            monster.draw(screen, 0, 0)

class VolcanoWorld:
    def __init__(self):
        self.width = 25
        self.height = 20
        self.blocks = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.lava_level = 10
        self.generate_volcano()
        
    def generate_volcano(self):
        # Generate volcano interior
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == self.height - 1:
                    self.blocks[x][y] = 2  # Volcano wall
                elif y > self.height - 5:
                    self.blocks[x][y] = 2  # Volcano floor
                else:
                    self.blocks[x][y] = 0  # Empty
                    
        # Add some platforms
        for _ in range(8):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 8)
            for i in range(3):
                if x + i < self.width:
                    self.blocks[x + i][y] = 2  # Platform
                    
    def draw(self, screen):
        # Draw volcano background
        screen.fill(LAVA_RED)
        
        # Draw volcano blocks
        for x in range(self.width):
            for y in range(self.height):
                if self.blocks[x][y] == 2:
                    pygame.draw.rect(screen, VOLCANO_BROWN, (x * 40, y * 40, 40, 40))
                    pygame.draw.rect(screen, BLACK, (x * 40, y * 40, 40, 40), 2)
                    
        # Draw lava
        lava_rect = pygame.Rect(0, (self.height - self.lava_level) * 40, self.width * 40, self.lava_level * 40)
        pygame.draw.rect(screen, LAVA_RED, lava_rect)
        
        # Draw lava bubbles
        for _ in range(10):
            x = random.randint(0, self.width * 40)
            y = (self.height - self.lava_level) * 40 + random.randint(-20, 20)
            pygame.draw.circle(screen, ORANGE, (x, y), random.randint(5, 15))

class VolcanoAdventureGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🌋 VOLCANO ADVENTURE - Mine Rubies & Battle Monsters! 🌋")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Game objects
        self.world = World()
        self.player = Player(200, 400)
        self.camera_x = 0
        self.camera_y = 0
        
        # Village
        self.villagers = []
        for i in range(6):
            x = 150 + i * 60
            y = 350
            self.villagers.append(Villager(x, y))
            
        # Special worlds
        self.cave_world = None
        self.volcano_world = None
        
        # Rubies in overworld
        self.overworld_rubies = []
        for _ in range(5):
            x = random.randint(100, 800)
            y = random.randint(200, 400)
            self.overworld_rubies.append(Ruby(x, y))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.CAVE:
                        # Exit cave
                        self.state = GameState.PLAYING
                        self.player.x = 1640  # Outside cave
                        self.player.y = 320
                        self.player.state = PlayerState.OVERWORLD
                    elif self.state == GameState.VOLCANO:
                        # Exit volcano
                        self.state = GameState.PLAYING
                        self.player.x = 1400  # Outside volcano
                        self.player.y = 280
                        self.player.state = PlayerState.OVERWORLD
                    else:
                        self.state = GameState.MENU
                        
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.PLAYING:
                        self.player.jump()
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - mine/attack
                    if self.state == GameState.PLAYING:
                        # Mine block
                        world_x = int((self.player.x + self.player.width // 2) // 40)
                        world_y = int((self.player.y + self.player.height // 2) // 40)
                        mined = self.world.mine_block(world_x, world_y)
                        
                        if mined == 3:  # Found ruby!
                            self.player.rubies += 1
                            
                    elif self.state == GameState.CAVE:
                        # Attack monsters or collect rubies
                        for ruby in self.cave_world.rubies:
                            if not ruby.collected:
                                ruby_rect = pygame.Rect(ruby.x - 10, ruby.y - 10, 20, 20)
                                player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                                if ruby_rect.colliderect(player_rect):
                                    ruby.collected = True
                                    self.player.rubies += 1
                                    
                        # Attack monsters
                        for monster in self.cave_world.monsters:
                            monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
                            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                            if monster_rect.colliderect(player_rect):
                                if monster.attack_cooldown <= 0:
                                    died = monster.take_damage(self.player.pickaxe_power * 5)
                                    if died:
                                        self.cave_world.monsters.remove(monster)
                                        self.player.gold += 50
                                        
                elif event.button == 3:  # Right click - interact
                    if self.state == GameState.PLAYING:
                        # Check for special interactions
                        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                        
                        # Check cave entrance
                        cave_rect = pygame.Rect(1600, 280, 120, 60)
                        if player_rect.colliderect(cave_rect):
                            self.state = GameState.CAVE
                            self.cave_world = CaveWorld()
                            self.player.x = 100
                            self.player.y = 200
                            self.player.state = PlayerState.IN_CAVE
                            
                        # Check volcano entrance
                        volcano_rect = pygame.Rect(1400, 240, 120, 80)
                        if player_rect.colliderect(volcano_rect):
                            self.state = GameState.VOLCANO
                            self.volcano_world = VolcanoWorld()
                            self.player.x = 200
                            self.player.y = 100
                            self.player.state = PlayerState.IN_VOLCANO
                            
                        # Talk to villagers
                        for villager in self.villagers:
                            villager_rect = pygame.Rect(villager.x, villager.y, villager.width, villager.height)
                            if player_rect.colliderect(villager_rect):
                                villager.set_dialogue("Welcome to our village! The volcano holds many rubies!")
                                
    def update_camera(self):
        # Center camera on player
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Keep camera in bounds
        if self.state == GameState.PLAYING:
            self.camera_x = max(0, min(self.camera_x, self.world.width * 40 - SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y, self.world.height * 40 - SCREEN_HEIGHT))
            
    def update(self):
        keys = pygame.key.get_pressed()
        
        if self.state == GameState.PLAYING:
            self.player.update(keys, self.world)
            self.update_camera()
            
            # Update villagers
            for villager in self.villagers:
                villager.update()
                
            # Update overworld rubies
            for ruby in self.overworld_rubies:
                if not ruby.collected:
                    ruby.update()
                    ruby_rect = pygame.Rect(ruby.x - 10, ruby.y - 10, 20, 20)
                    player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                    if ruby_rect.colliderect(player_rect):
                        ruby.collected = True
                        self.player.rubies += 1
                        
        elif self.state == GameState.CAVE:
            self.player.update(keys, self.cave_world)
            
            # Update cave monsters
            for monster in self.cave_world.monsters:
                monster.update(self.player)
                
                # Check monster collision with player
                monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
                player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                if monster_rect.colliderect(player_rect):
                    if monster.attack_cooldown <= 0:
                        self.player.health -= monster.damage
                        monster.attack_cooldown = 60
                        
        elif self.state == GameState.VOLCANO:
            self.player.update(keys, self.volcano_world)
            
            # Update lava level
            self.volcano_world.lava_level = max(5, self.volcano_world.lava_level - 0.01)
            
    def draw_menu(self):
        self.screen.fill(SKY_BLUE)
        
        # Title
        title_text = self.font_large.render("🌋 VOLCANO ADVENTURE 🌋", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Mine Rubies & Battle Rock Monsters!", True, RUBY_RED)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Start button
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, GREEN, start_rect)
        pygame.draw.rect(self.screen, WHITE, start_rect, 3)
        start_text = self.font_medium.render("START ADVENTURE", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_rect.center)
        self.screen.blit(start_text, start_text_rect)
        
        # Instructions
        instructions = [
            "🎮 WASD/Arrows: Move | Space: Jump",
            "🖱️ Left Click: Mine/Attack | Right Click: Interact",
            "👶 Talk to villagers for tips!",
            "🌋 Explore volcano and caves!",
            "💎 Collect rubies to become rich!",
            "👹 Battle rock monsters in caves!"
        ]
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - 300, 250 + i * 30))
            
    def draw_playing(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw world
        self.world.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw villagers
        for villager in self.villagers:
            villager.draw(self.screen, self.camera_x, self.camera_y)
            
        # Draw overworld rubies
        for ruby in self.overworld_rubies:
            if not ruby.collected:
                ruby.draw(self.screen, self.camera_x, self.camera_y)
                
        # Draw player
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw UI
        self.draw_ui()
        
        # Draw interaction hints
        self.draw_interaction_hints()
        
    def draw_cave(self):
        self.cave_world.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen, 0, 0)
        
        # Draw UI
        self.draw_ui()
        
        # Exit hint
        exit_text = self.font_small.render("Press ESC to exit cave", True, WHITE)
        self.screen.blit(exit_text, (10, 10))
        
    def draw_volcano(self):
        self.volcano_world.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen, 0, 0)
        
        # Draw UI
        self.draw_ui()
        
        # Exit hint
        exit_text = self.font_small.render("Press ESC to exit volcano", True, WHITE)
        self.screen.blit(exit_text, (10, 10))
        
    def draw_ui(self):
        # Stats panel
        panel_rect = pygame.Rect(10, 10, 250, 120)
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Player stats
        rubies_text = self.font_small.render(f"💎 Rubies: {self.player.rubies}", True, RUBY_RED)
        self.screen.blit(rubies_text, (20, 20))
        
        gold_text = self.font_small.render(f"🪙 Gold: {self.player.gold}", True, GOLD)
        self.screen.blit(gold_text, (20, 45))
        
        health_text = self.font_small.render(f"❤️ Health: {self.player.health}/{self.player.max_health}", True, RED)
        self.screen.blit(health_text, (20, 70))
        
        power_text = self.font_small.render(f"⛏️ Power: {self.player.pickaxe_power}", True, WHITE)
        self.screen.blit(power_text, (20, 95))
        
        # Location indicator
        if self.player.state == PlayerState.OVERWORLD:
            location = "🌍 Overworld"
        elif self.player.state == PlayerState.IN_VOLCANO:
            location = "🌋 Volcano"
        elif self.player.state == PlayerState.IN_CAVE:
            location = "🕳️ Cave"
        else:
            location = "❓ Unknown"
            
        location_text = self.font_small.render(f"Location: {location}", True, WHITE)
        self.screen.blit(location_text, (20, 120))
        
    def draw_interaction_hints(self):
        # Check for special locations
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        
        # Cave entrance hint
        cave_rect = pygame.Rect(1600, 280, 120, 60)
        if player_rect.colliderect(cave_rect):
            hint_text = self.font_small.render("🕳️ CAVE - Right Click to Enter", True, WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            pygame.draw.rect(self.screen, BLACK, hint_rect.inflate(10, 5))
            pygame.draw.rect(self.screen, WHITE, hint_rect.inflate(10, 5), 2)
            self.screen.blit(hint_text, hint_rect)
            
        # Volcano entrance hint
        volcano_rect = pygame.Rect(1400, 240, 120, 80)
        if player_rect.colliderect(volcano_rect):
            hint_text = self.font_small.render("🌋 VOLCANO - Right Click to Enter", True, WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            pygame.draw.rect(self.screen, BLACK, hint_rect.inflate(10, 5))
            pygame.draw.rect(self.screen, WHITE, hint_rect.inflate(10, 5), 2)
            self.screen.blit(hint_text, hint_rect)
            
    def run(self):
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update
            self.update()
            
            # Draw based on state
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_playing()
            elif self.state == GameState.CAVE:
                self.draw_cave()
            elif self.state == GameState.VOLCANO:
                self.draw_volcano()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = VolcanoAdventureGame()
    game.run()
