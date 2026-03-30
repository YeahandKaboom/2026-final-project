#!/usr/bin/env python3
"""
MONEY CRAFT EPIC - Mine Wealth & Throw Kids in Volcanoes!
The ultimate money-making idle game with dark humor!
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
LAVA_RED = (255, 100, 0)
VOLCANO_BROWN = (101, 67, 33)
VOLCANO_RED = (255, 50, 0)
SKY_BLUE = (135, 206, 235)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Game states
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    SHOP = 2

# Upgrade types
class UpgradeType(Enum):
    PICKAXE = 0
    DRILL = 1
    EXCAVATOR = 2
    DYNAMITE = 3
    VOLCANO_LAUNCHER = 4
    KID_MAGNET = 5
    MEGA_DRILL = 6  # NEW: Super fast mining
    QUANTUM_PICKAXE = 7  # NEW: Insane mining power
    CHILD_WORKERS = 8  # NEW: Village children help mine!
    VOLCANO_UPGRADE = 9  # NEW: Upgrade giant volcano

# Kid types
class KidType(Enum):
    NORMAL = 0
    GOLDEN = 1
    RARE = 2

class Particle:
    def __init__(self, x, y, vel_x, vel_y, color, size, life):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.5  # Gravity
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class Kid:
    def __init__(self, x, y, kid_type=KidType.NORMAL):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-5, -2)
        self.type = kid_type
        self.value = self.get_value()
        self.size = 20 if kid_type == KidType.NORMAL else 25
        self.rotation = 0
        self.scream_timer = 0
        
    def get_value(self):
        if self.type == KidType.NORMAL:
            return random.randint(10, 50)
        elif self.type == KidType.GOLDEN:
            return random.randint(100, 500)
        else:  # RARE
            return random.randint(1000, 5000)
            
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.3  # Gravity
        
        self.rotation += 5
        
        # Bounce off walls
        if self.x <= 10 or self.x >= SCREEN_WIDTH - 10:
            self.vel_x *= -0.8
        if self.y <= 10:
            self.vel_y = abs(self.vel_y) * 0.8
            
    def draw(self, screen):
        # Draw kid based on type
        if self.type == KidType.NORMAL:
            color = PINK
        elif self.type == KidType.GOLDEN:
            color = GOLD
        else:  # RARE
            colors = [PURPLE, CYAN, YELLOW, ORANGE]
            color = colors[int(self.rotation / 10) % len(colors)]
            
        # Draw body
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw face
        face_color = WHITE
        pygame.draw.circle(screen, face_color, (int(self.x - 5), int(self.y - 5)), 3)
        pygame.draw.circle(screen, face_color, (int(self.x + 5), int(self.y - 5)), 3)
        
        # Draw scream when thrown
        if self.scream_timer > 0:
            scream_text = pygame.font.Font(None, 16).render("AHHH!", True, RED)
            screen.blit(scream_text, (int(self.x - 20), int(self.y - 30)))
            self.scream_timer -= 1

class Volcano:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False
        self.eruption_timer = 0
        self.lava_height = 0
        
    def erupt(self):
        self.active = True
        self.eruption_timer = 120  # 2 seconds at 60 FPS
        
    def update(self):
        if self.active:
            self.eruption_timer -= 1
            
            # Animate lava
            if self.eruption_timer < 60:
                self.lava_height = min(50, (60 - self.eruption_timer))
            else:
                self.lava_height = max(0, self.lava_height - 2)
                
            if self.eruption_timer <= 0:
                self.active = False
                self.lava_height = 0
                
    def draw(self, screen):
        # Draw volcano cone
        pygame.draw.polygon(screen, VOLCANO_BROWN, [
            (self.x, self.y),
            (self.x - 40, self.y + 80),
            (self.x + 40, self.y + 80)
        ])
        
        # Draw crater
        pygame.draw.ellipse(screen, BLACK, (self.x - 30, self.y + 60, 60, 40))
        
        # Draw lava if active
        if self.active and self.lava_height > 0:
            lava_rect = pygame.Rect(self.x - 20, self.y + 60 - self.lava_height, 40, self.lava_height)
            pygame.draw.rect(screen, LAVA_RED, lava_rect)
            
            # Lava particles
            for _ in range(3):
                particle_x = self.x + random.randint(-20, 20)
                particle_y = self.y + 60 - self.lava_height + random.randint(-10, 10)
                pygame.draw.circle(screen, ORANGE, (particle_x, particle_y), random.randint(3, 8))

class MoneyCraftGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("💰 MONEY CRAFT - Mine Wealth & Throw Kids! 💰")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Game data
        self.money = 100  # Starting money
        self.money_per_second = 0
        self.total_kids_thrown = 0
        self.total_money_earned = 0
        
        # Mining (UPGRADED!)
        self.pickaxe_power = 1
        self.mining_speed = 1
        self.auto_mine = False
        self.mine_progress = 0
        self.mining_multiplier = 1.0  # NEW: Mining factor multiplier!
        self.mining_combo = 0  # NEW: Combo system!
        self.last_mine_time = 0
        
        # Kids
        self.kids = []
        self.kid_spawn_timer = 0
        self.kid_value_multiplier = 1
        
        # Volcanoes
        self.volcanoes = []
        self.volcano_cost = 1000
        self.volcanoes_owned = 0
        
        # GIANT VOLCANO (NEW!)
        self.giant_volcano = {
            'x': SCREEN_WIDTH - 300,
            'y': 200,
            'erupting': False,
            'eruption_timer': 0,
            'lava_height': 0,
            'smoke_particles': []
        }
        
        # CHILD VILLAGE (NEW!)
        self.child_village = {
            'x': 100,
            'y': 300,
            'mining_children': [],
            'village_hut': True
        }
        
        # Spawn village children
        for i in range(8):  # 8 children mining in village
            child_x = self.child_village['x'] + random.randint(-50, 50)
            child_y = self.child_village['y'] + random.randint(-30, 30)
            mining_child = {
                'x': child_x,
                'y': child_y,
                'mining': True,
                'progress': random.randint(0, 100),
                'ore_found': random.choice(['gold', 'diamond', 'ruby', 'emerald']),
                'animation_frame': 0
            }
            self.child_village['mining_children'].append(mining_child)
        
        # Upgrades
        self.owned_upgrades = {
            UpgradeType.PICKAXE: True,
            UpgradeType.DRILL: False,
            UpgradeType.EXCAVATOR: False,
            UpgradeType.DYNAMITE: False,
            UpgradeType.VOLCANO_LAUNCHER: False,
            UpgradeType.KID_MAGNET: False
        }
        
        self.upgrade_costs = {
            UpgradeType.PICKAXE: 0,  # Free
            UpgradeType.DRILL: 500,
            UpgradeType.EXCAVATOR: 2000,
            UpgradeType.DYNAMITE: 100,
            UpgradeType.VOLCANO_LAUNCHER: 5000,
            UpgradeType.KID_MAGNET: 3000,
            UpgradeType.MEGA_DRILL: 10000,  # NEW: Super fast!
            UpgradeType.QUANTUM_PICKAXE: 50000,  # NEW: Insane power!
            UpgradeType.CHILD_WORKERS: 15000,  # NEW: Village help!
            UpgradeType.VOLCANO_UPGRADE: 25000  # NEW: Giant volcano!
        }
        
        # Particles
        self.particles = []
        
    def spawn_kid(self):
        # Spawn kid at random location
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, 300)
        
        # Kid type based on upgrades
        if self.owned_upgrades[UpgradeType.KID_MAGNET]:
            # Higher chance for rare kids
            rand = random.random()
            if rand < 0.1:
                kid_type = KidType.RARE
            elif rand < 0.3:
                kid_type = KidType.GOLDEN
            else:
                kid_type = KidType.NORMAL
        else:
            kid_type = KidType.NORMAL
            
        kid = Kid(x, y, kid_type)
        self.kids.append(kid)
        
    def spawn_volcano(self):
        # Spawn volcano at bottom of screen
        x = random.randint(200, SCREEN_WIDTH - 200)
        y = SCREEN_HEIGHT - 150
        volcano = Volcano(x, y)
        self.volcanoes.append(volcano)
        
    def handle_menu_click(self, pos):
        # Start button
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        if start_rect.collidepoint(pos):
            self.state = GameState.PLAYING
            return True
        return False
        
    def handle_shop_click(self, pos):
        # Check upgrade buttons
        y_offset = 200
        
        for i, (upgrade_type, cost) in enumerate(self.upgrade_costs.items()):
            if not self.owned_upgrades[upgrade_type]:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_offset + i * 60, 300, 40)
                if button_rect.collidepoint(pos):
                    if self.money >= cost:
                        self.money -= cost
                        self.owned_upgrades[upgrade_type] = True
                        
                        # Apply upgrade effects
                        if upgrade_type == UpgradeType.DRILL:
                            self.mining_speed = 2
                        elif upgrade_type == UpgradeType.EXCAVATOR:
                            self.mining_speed = 5
                            self.pickaxe_power = 3
                        elif upgrade_type == UpgradeType.DYNAMITE:
                            self.pickaxe_power = 5
                        elif upgrade_type == UpgradeType.VOLCANO_LAUNCHER:
                            self.volcanoes_owned += 1
                        elif upgrade_type == UpgradeType.KID_MAGNET:
                            self.kid_value_multiplier = 2
                    return True
        return False
        
    def handle_playing_click(self, pos):
        # Mine button
        mine_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 150, 50)
        if mine_rect.collidepoint(pos):
            self.auto_mine = not self.auto_mine
            return True
            
        # Auto-mine toggle
        auto_rect = pygame.Rect(50, SCREEN_HEIGHT - 40, 150, 40)
        if auto_rect.collidepoint(pos):
            self.auto_mine = not self.auto_mine
            return True
            
        # Shop button
        shop_rect = pygame.Rect(SCREEN_WIDTH - 200, 50, 150, 40)
        if shop_rect.collidepoint(pos):
            self.state = GameState.SHOP
            return True
            
        # Volcano button
        if self.volcanoes_owned > 0:
            volcano_rect = pygame.Rect(SCREEN_WIDTH - 200, 100, 150, 40)
            if volcano_rect.collidepoint(pos):
                if self.money >= self.volcano_cost:
                    self.money -= self.volcano_cost
                    self.spawn_volcano()
                return True
                
        # Throw kid button
        if len(self.kids) > 0:
            throw_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50)
            if throw_rect.collidepoint(pos):
                # Remove first kid and throw to volcano
                if self.volcanoes:
                    kid = self.kids.pop(0)
                    kid.vel_x = random.uniform(-8, 8)
                    kid.vel_y = random.uniform(-15, -10)
                    kid.scream_timer = 30
                    self.total_kids_thrown += 1
                    
                    # Find nearest volcano
                    nearest_volcano = min(self.volcanoes, 
                                       key=lambda v: math.sqrt((v.x - kid.x)**2 + (v.y - kid.y)**2))
                    if nearest_volcano:
                        nearest_volcano.erupt()
                return True
        return False
        
    def update_menu(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.handle_menu_click(event.pos):
                    return
                    
    def draw_giant_volcano(self, screen):
        # Draw MASSIVE volcano in distance
        volcano = self.giant_volcano
        
        # Draw giant volcano cone
        pygame.draw.polygon(screen, VOLCANO_BROWN, [
            (volcano['x'], volcano['y']),
            (volcano['x'] - 120, volcano['y'] + 200),
            (volcano['x'] + 120, volcano['y'] + 200)
        ])
        
        # Draw massive crater
        pygame.draw.ellipse(screen, BLACK, (volcano['x'] - 80, volcano['y'] + 160, 160, 80))
        
        # Draw lava if erupting
        if volcano['erupting'] and volcano['lava_height'] > 0:
            lava_rect = pygame.Rect(volcano['x'] - 60, volcano['y'] + 160 - volcano['lava_height'], 120, volcano['lava_height'])
            pygame.draw.rect(screen, LAVA_RED, lava_rect)
            
            # Massive lava particles
            for _ in range(10):
                particle_x = volcano['x'] + random.randint(-60, 60)
                particle_y = volcano['y'] + 160 - volcano['lava_height'] + random.randint(-20, 20)
                pygame.draw.circle(screen, ORANGE, (particle_x, particle_y), random.randint(5, 15))
                
        # Draw smoke particles
        for particle in volcano['smoke_particles'][:]:
            particle['y'] -= 1
            particle['x'] += random.uniform(-1, 1)
            particle['life'] -= 1
            
            if particle['life'] > 0:
                alpha = int(100 * (particle['life'] / particle['max_life']))
                color = (*GRAY, alpha)
                pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), particle['size'])
            else:
                volcano['smoke_particles'].remove(particle)
                
        # Add new smoke
        if random.random() < 0.1:
            smoke_particle = {
                'x': volcano['x'] + random.randint(-40, 40),
                'y': volcano['y'] + 140,
                'size': random.randint(10, 25),
                'life': 100,
                'max_life': 100
            }
            volcano['smoke_particles'].append(smoke_particle)
            
    def draw_child_village(self, screen):
        # Draw village of mining children
        village = self.child_village
        
        # Draw village hut
        if village['village_hut']:
            # Hut base
            hut_rect = pygame.Rect(village['x'] - 40, village['y'] - 20, 80, 60)
            pygame.draw.rect(screen, BROWN, hut_rect)
            pygame.draw.rect(screen, BLACK, hut_rect, 2)
            
            # Hut roof
            pygame.draw.polygon(screen, DARK_RED, [
                (village['x'] - 50, village['y'] - 20),
                (village['x'] + 50, village['y'] - 20),
                (village['x'], village['y'] - 50)
            ])
            
            # Hut door
            door_rect = pygame.Rect(village['x'] - 10, village['y'], 20, 30)
            pygame.draw.rect(screen, BLACK, door_rect)
            
            # Sign
            sign_text = self.font_small.render("MINING VILLAGE", True, WHITE)
            screen.blit(sign_text, (village['x'] - 60, village['y'] - 70))
            
        # Draw mining children
        for child in village['mining_children']:
            # Child body
            pygame.draw.circle(screen, PINK, (int(child['x']), int(child['y'])), 12)
            
            # Mining pickaxe
            pickaxe_x = child['x'] + 15
            pickaxe_y = child['y'] - 5
            pygame.draw.rect(screen, GRAY, (pickaxe_x, pickaxe_y, 15, 3))
            pygame.draw.rect(screen, BROWN, (pickaxe_x, pickaxe_y + 3, 15, 6))
            
            # Mining animation
            child['animation_frame'] += 1
            if child['animation_frame'] % 20 < 10:
                # Swinging down
                pygame.draw.rect(screen, GRAY, (pickaxe_x - 5, pickaxe_y + 9, 25, 3))
            else:
                # Swinging up
                pygame.draw.rect(screen, GRAY, (pickaxe_x - 5, pickaxe_y - 12, 25, 3))
                
            # Mining progress
            if child['mining']:
                child['progress'] += 1
                if child['progress'] >= 100:
                    # Found ore!
                    ore_values = {
                        'gold': 25,
                        'diamond': 100,
                        'ruby': 50,
                        'emerald': 75
                    }
                    found_value = ore_values.get(child['ore_found'], 25)
                    self.money += found_value
                    child['progress'] = 0
                    child['ore_found'] = random.choice(['gold', 'diamond', 'ruby', 'emerald'])
                    
                    # Create ore particle
                    ore_colors = {
                        'gold': GOLD,
                        'diamond': (185, 242, 255),
                        'ruby': RED,
                        'emerald': GREEN
                    }
                    for _ in range(5):
                        particle = Particle(
                            child['x'] + random.randint(-10, 10),
                            child['y'] + random.randint(-10, 10),
                            random.uniform(-3, 3),
                            random.uniform(-5, -2),
                            ore_colors.get(child['ore_found'], GOLD),
                            random.randint(3, 8),
                            random.randint(20, 40)
                        )
                        self.particles.append(particle)
                        
            # Draw progress bar
            progress_rect = pygame.Rect(child['x'] - 20, child['y'] - 25, 40, 5)
            pygame.draw.rect(screen, BLACK, progress_rect)
            progress_fill = pygame.Rect(child['x'] - 20, child['y'] - 25, int(40 * child['progress'] / 100), 5)
            pygame.draw.rect(screen, GREEN, progress_fill)
                    
    def update_playing(self, events):
        # Handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_playing_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    
        # Auto-mining with BETTER FACTORS!
        if self.auto_mine:
            # Apply mining multiplier and combo
            base_speed = self.mining_speed * self.mining_multiplier
            if self.mining_combo > 0:
                combo_bonus = 1 + (self.mining_combo * 0.1)
                base_speed *= combo_bonus
                
            self.mine_progress += base_speed
            
            # Combo timing
            current_time = pygame.time.get_ticks()
            if current_time - self.last_mine_time < 1000:  # Within 1 second
                self.mining_combo += 1
            else:
                self.mining_combo = 0
            self.last_mine_time = current_time
            
            if self.mine_progress >= 100:
                self.mine_progress = 0
                # Earn money with multipliers
                base_earned = self.pickaxe_power * 10
                total_earned = int(base_earned * self.mining_multiplier)
                if self.mining_combo > 5:
                    total_earned *= 2  # Combo bonus!
                    
                self.money += total_earned
                self.total_money_earned += total_earned
                self.money_per_second += total_earned
                
                # EPIC mine particles
                particle_count = self.pickaxe_power * 3
                if self.mining_combo > 5:
                    particle_count *= 2  # Combo particles!
                    
                for _ in range(particle_count):
                    particle = Particle(
                        SCREEN_WIDTH // 2 + random.randint(-80, 80),
                        SCREEN_HEIGHT // 2 + random.randint(-80, 80),
                        random.uniform(-8, 8),
                        random.uniform(-12, -4),
                        GOLD,
                        random.randint(5, 15),
                        random.randint(30, 60)
                    )
                    self.particles.append(particle)
                    
        # Update giant volcano
        volcano = self.giant_volcano
        if volcano['erupting']:
            volcano['eruption_timer'] -= 1
            
            # Animate massive lava
            if volcano['eruption_timer'] < 120:
                volcano['lava_height'] = min(100, (120 - volcano['eruption_timer']))
            else:
                volcano['lava_height'] = max(0, volcano['lava_height'] - 3)
                
            if volcano['eruption_timer'] <= 0:
                volcano['erupting'] = False
                volcano['lava_height'] = 0
                
        # Update village children mining
        for child in self.child_village['mining_children']:
            if child['mining']:
                child['progress'] += 1
                if child['progress'] >= 100:
                    # Village child found ore!
                    ore_values = {
                        'gold': 25,
                        'diamond': 100,
                        'ruby': 50,
                        'emerald': 75
                    }
                    found_value = ore_values.get(child['ore_found'], 25)
                    self.money += found_value
                    child['progress'] = 0
                    child['ore_found'] = random.choice(['gold', 'diamond', 'ruby', 'emerald'])
                    
        # Update kids
        self.kid_spawn_timer -= 1
        if self.kid_spawn_timer <= 0 and len(self.kids) < 10:
            self.spawn_kid()
            self.kid_spawn_timer = random.randint(300, 600)  # 5-10 seconds
            
        for kid in self.kids[:]:
            kid.update()
            
        # Update volcanoes
        for volcano in self.volcanoes[:]:
            volcano.update()
            
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            
        # Calculate money per second
        self.money_per_second = max(0, self.total_money_earned // max(1, pygame.time.get_ticks() // 1000))
        
    def draw_menu(self):
        self.screen.fill(SKY_BLUE)
        
        # Title
        title_text = self.font_large.render("💰 MONEY CRAFT 💰", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Mine Wealth & Throw Kids in Volcanoes!", True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Start button
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, GREEN, start_rect)
        pygame.draw.rect(self.screen, WHITE, start_rect, 3)
        start_text = self.font_medium.render("START", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_rect.center)
        self.screen.blit(start_text, start_text_rect)
        
        # Instructions
        instructions = [
            "🎮 Mine for wealth by clicking or auto-mining!",
            "👶 Throw kids into volcanoes for MASSIVE profits!",
            "🌋 Buy upgrades to increase your power!",
            "⚠️ Dark humor parody game - not serious!"
        ]
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - 300, 300 + i * 30))
            
    def draw_shop(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("🛒 UPGRADE SHOP 🛒", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Money display
        money_text = self.font_medium.render(f"💰 Money: ${self.money}", True, WHITE)
        self.screen.blit(money_text, (50, 100))
        
        # Stats
        stats = [
            f"Kids Thrown: {self.total_kids_thrown}",
            f"Volcanoes Owned: {self.volcanoes_owned}",
            f"Money/Second: ${self.money_per_second}",
            f"Pickaxe Power: {self.pickaxe_power}"
        ]
        for i, stat in enumerate(stats):
            stat_text = self.font_small.render(stat, True, WHITE)
            self.screen.blit(stat_text, (50, 200 + i * 30))
        
        # Upgrades
        y_offset = 300
        for i, (upgrade_type, cost) in enumerate(self.upgrade_costs.items()):
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_offset + i * 60, 300, 40)
            
            if self.owned_upgrades[upgrade_type]:
                color = GREEN
                status = "OWNED"
            else:
                color = RED
                status = f"${cost}"
                
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Upgrade name
            names = {
                UpgradeType.DRILL: "⚡ DRILL - Auto Mine x2",
                UpgradeType.EXCAVATOR: "⛏️ EXCAVATOR - Auto Mine x5, Power x3",
                UpgradeType.DYNAMITE: "💣 DYNAMITE - Pickaxe Power x5",
                UpgradeType.VOLCANO_LAUNCHER: "🌋 VOLCANO LAUNCHER - Summon Volcanoes",
                UpgradeType.KID_MAGNET: "🧲 KID MAGNET - 2x Kid Values"
            }
            
            if upgrade_type in names:
                name_text = self.font_small.render(names[upgrade_type], True, WHITE)
                self.screen.blit(name_text, (button_rect.x + 10, button_rect.y + 5))
                
            status_text = self.font_small.render(status, True, WHITE)
            self.screen.blit(status_text, (button_rect.x + 10, button_rect.y + 25))
            
        # Back button
        back_text = self.font_small.render("Press ESC to go back", True, WHITE)
        self.screen.blit(back_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))
        
    def draw_playing(self):
        # Background
        self.screen.fill(SKY_BLUE)
        
        # Draw ground
        pygame.draw.rect(self.screen, BROWN, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200))
        
        # Draw GIANT VOLCANO in distance!
        self.draw_giant_volcano(self.screen)
        
        # Draw CHILD VILLAGE!
        self.draw_child_village(self.screen)
        
        # Draw regular volcanoes
        for volcano in self.volcanoes:
            volcano.draw(self.screen)
            
        # Draw kids
        for kid in self.kids:
            kid.draw(self.screen)
            
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
            
        # UI Panel
        panel_rect = pygame.Rect(0, 0, 350, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 3)
        
        # Money display
        money_text = self.font_medium.render(f"💰 ${self.money}", True, GOLD)
        self.screen.blit(money_text, (20, 20))
        
        # Money per second
        mps_text = self.font_small.render(f"${self.money_per_second}/sec", True, WHITE)
        self.screen.blit(mps_text, (20, 60))
        
        # Mining progress
        if self.auto_mine:
            progress_text = "AUTO-MINING"
            progress_color = GREEN
        else:
            progress_text = "CLICK TO MINE"
            progress_color = WHITE
            
        mine_text = self.font_small.render(progress_text, True, progress_color)
        self.screen.blit(mine_text, (20, 90))
        
        # Progress bar
        progress_rect = pygame.Rect(20, 120, 200, 20)
        pygame.draw.rect(self.screen, DARK_RED, progress_rect)
        progress_fill = pygame.Rect(20, 120, int(200 * self.mine_progress / 100), 20)
        pygame.draw.rect(self.screen, GREEN, progress_fill)
        pygame.draw.rect(self.screen, WHITE, progress_rect, 2)
        
        # Mine button
        mine_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 150, 50)
        pygame.draw.rect(self.screen, WHITE, mine_rect)
        pygame.draw.rect(self.screen, BLACK, mine_rect, 3)
        mine_text = self.font_small.render("MINE", True, BLACK)
        mine_text_rect = mine_text.get_rect(center=mine_rect.center)
        self.screen.blit(mine_text, mine_text_rect)
        
        # Auto-mine toggle
        auto_rect = pygame.Rect(50, SCREEN_HEIGHT - 40, 150, 40)
        if self.auto_mine:
            auto_color = GREEN
            auto_text = "AUTO: ON"
        else:
            auto_color = RED
            auto_text = "AUTO: OFF"
            
        pygame.draw.rect(self.screen, auto_color, auto_rect)
        pygame.draw.rect(self.screen, WHITE, auto_rect, 2)
        auto_text_render = self.font_small.render(auto_text, True, BLACK)
        auto_text_rect = auto_text_render.get_rect(center=auto_rect.center)
        self.screen.blit(auto_text_render, auto_text_rect)
        
        # Shop button
        shop_rect = pygame.Rect(SCREEN_WIDTH - 200, 50, 150, 40)
        pygame.draw.rect(self.screen, PURPLE, shop_rect)
        pygame.draw.rect(self.screen, WHITE, shop_rect, 3)
        shop_text = self.font_small.render("SHOP", True, WHITE)
        shop_text_rect = shop_text.get_rect(center=shop_rect.center)
        self.screen.blit(shop_text, shop_text_rect)
        
        # Volcano button
        if self.volcanoes_owned > 0:
            volcano_rect = pygame.Rect(SCREEN_WIDTH - 200, 100, 150, 40)
            volcano_color = GREEN if self.money >= self.volcano_cost else RED
            pygame.draw.rect(self.screen, volcano_color, volcano_rect)
            pygame.draw.rect(self.screen, WHITE, volcano_rect, 2)
            volcano_text = self.font_small.render(f"VOLCANO ${self.volcano_cost}", True, WHITE)
            volcano_text_rect = volcano_text.get_rect(center=volcano_rect.center)
            self.screen.blit(volcano_text, volcano_text_rect)
            
        # Throw kid button
        if len(self.kids) > 0:
            throw_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50)
            pygame.draw.rect(self.screen, ORANGE, throw_rect)
            pygame.draw.rect(self.screen, WHITE, throw_rect, 3)
            throw_text = self.font_small.render("THROW KID", True, BLACK)
            throw_text_rect = throw_text.get_rect(center=throw_rect.center)
            self.screen.blit(throw_text, throw_text_rect)
            
        # Kids counter
        kids_text = self.font_small.render(f"Kids: {len(self.kids)}", True, WHITE)
        self.screen.blit(kids_text, (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 150))
        
    def run(self):
        while self.running:
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # Update based on state
            if self.state == GameState.MENU:
                self.update_menu(events)
                self.draw_menu()
            elif self.state == GameState.SHOP:
                self.update_shop(events)
                self.draw_shop()
            elif self.state == GameState.PLAYING:
                self.update_playing(events)
                self.draw_playing()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = MoneyCraftGame()
    game.run()
