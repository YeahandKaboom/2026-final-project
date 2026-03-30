#!/usr/bin/env python3
"""
WEALTH CRAFT - Pure Ruby Mining Adventure!
Mine massive wealth in an epic world of treasures!
"""

import pygame
import random
import math
import json
import time
from enum import Enum
from collections import defaultdict
from simple_enhancements import Enemy, NPC, PowerUp, Quest, Structure, Pet, WeatherSystem, AchievementSystem

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
EMERALD_GREEN = (0, 201, 87)
DIAMOND_BLUE = (185, 242, 255)
LAVA_RED = (255, 100, 0)
VOLCANO_BROWN = (101, 67, 33)
SKY_BLUE = (135, 206, 235)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Game states
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    SHOP = 2
    UNDERGROUND = 3

# Gem types
class GemType(Enum):
    RUBY = 1
    EMERALD = 2
    DIAMOND = 3
    GOLD = 4
    SAPPHIRE = 5
    AMETHYST = 6
    CRYSTAL = 7
    RARE_CRYSTAL = 8

# Biome types
class BiomeType(Enum):
    FOREST = 1
    DESERT = 2
    SNOW = 3
    MOUNTAINS = 4
    SWAMP = 5
    VOLCANIC = 6
    MYSTICAL = 7

# Weather types
class WeatherType(Enum):
    CLEAR = 1
    RAIN = 2
    SNOW = 3
    STORM = 4
    FOG = 5

# Achievement types
class AchievementType(Enum):
    FIRST_GEM = 1
    WEALTHY = 2
    MINER = 3
    EXPLORER = 4
    COMBAT_MASTER = 5
    COLLECTOR = 6
    SPEED_MINER = 7
    RARE_HUNTER = 8

# Quest types
class QuestType(Enum):
    COLLECT_GEMS = 1
    MINE_BLOCKS = 2
    REACH_LEVEL = 3
    FIND_CAVE = 4
    COLLECT_WEALTH = 5
    SURVIVE_TIME = 6

# Enemy types
class EnemyType(Enum):
    GOBLIN = 1
    ROCK_MONSTER = 2
    CREEPER = 3
    DRAGON = 4
    GHOST = 5
    SPIDER = 6

# Power-up types
class PowerUpType(Enum):
    SPEED_BOOST = 1
    DOUBLE_WEALTH = 2
    INSTANT_MINE = 3
    MAGNET_BOOST = 4
    SHIELD = 5
    XRAY_VISION = 6

# Upgrade types
class UpgradeType(Enum):
    PICKAXE = 0
    STEEL_PICKAXE = 1
    GOLDEN_PICKAXE = 2
    DIAMOND_PICKAXE = 3
    MEGA_DRILL = 4
    QUANTUM_MINER = 5
    RUBY_MAGNET = 6
    LUCKY_CHARMS = 7

# Shop items
class ShopItem(Enum):
    STEEL_BOOTS = 0
    GOLDEN_BOOTS = 1
    DIAMOND_BOOTS = 2
    MINING_HELMET = 3
    LUCKY_PICKAXE = 4
    RUBY_DETECTOR = 5
    TREASURE_MAP = 6
    CAVE_LIGHT = 7
    EXPLOSIVES = 8

# Tools and weapons
class ToolType(Enum):
    BASIC_PICKAXE = 0
    STEEL_PICKAXE_TOOL = 1
    GOLDEN_PICKAXE_TOOL = 2
    DIAMOND_PICKAXE_TOOL = 3
    MEGA_DRILL_TOOL = 4
    QUANTUM_MINER_TOOL = 5
    MINING_LASER = 6
    PLASMA_CUTTER = 7
    ANTI_MATTER_PICKAXE = 8

class WeaponType(Enum):
    BASIC_SWORD = 0
    STEEL_SWORD = 1
    GOLDEN_SWORD = 2
    DIAMOND_SWORD = 3
    LASER_GUN = 4
    PLASMA_RIFLE = 5
    ROCKET_LAUNCHER = 6
    ANTI_MATTER_CANNON = 7

# Underground blocks
class UndergroundBlock(Enum):
    STONE = 0
    GOLD_BLOCK = 1
    DIAMOND_BLOCK = 2
    SUS_BLOB = 3
    RUBY_VEIN = 4
    EMERALD_VEIN = 5
    BEDROCK = 6

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
        self.vel_y += 0.3  # Gravity
        self.vel_x *= 0.98  # Friction
        self.life -= 1
        
    def draw(self, screen, camera_x, camera_y):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            pygame.draw.circle(screen, self.color, (int(draw_x), int(draw_y)), self.size)

class Gem:
    def __init__(self, x, y, gem_type):
        self.x = x
        self.y = y
        self.type = gem_type
        self.size = 12
        self.collected = False
        self.animation_frame = 0
        self.glow_timer = 0
        self.rotation = 0
        
        # Gem properties
        self.properties = {
            GemType.RUBY: {"color": RUBY_RED, "value": 100, "name": "Ruby"},
            GemType.EMERALD: {"color": EMERALD_GREEN, "value": 200, "name": "Emerald"},
            GemType.DIAMOND: {"color": DIAMOND_BLUE, "value": 500, "name": "Diamond"},
            GemType.GOLD: {"color": GOLD, "value": 50, "name": "Gold"},
            GemType.SAPPHIRE: {"color": BLUE, "value": 300, "name": "Sapphire"},
            GemType.AMETHYST: {"color": PURPLE, "value": 400, "name": "Amethyst"},
            GemType.CRYSTAL: {"color": WHITE, "value": 600, "name": "Crystal"},
            GemType.RARE_CRYSTAL: {"color": LIGHT_GRAY, "value": 1000, "name": "Rare Crystal"}
        }
        
    def update(self):
        self.animation_frame += 1
        self.glow_timer += 1
        self.rotation += 2
        
    def draw(self, screen, camera_x, camera_y):
        if self.collected:
            return
            
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        props = self.properties[self.type]
        
        # Glowing aura effect
        glow_size = self.size + int(8 * math.sin(self.glow_timer * 0.1))
        glow_color = (*props["color"], 50)
        pygame.draw.circle(screen, glow_color, (int(draw_x), int(draw_y)), glow_size)
        
        # Gem core with rotation
        core_size = self.size
        pygame.draw.circle(screen, props["color"], (int(draw_x), int(draw_y)), core_size)
        
        # Sparkle effect
        if self.animation_frame % 20 < 10:
            sparkle_x = draw_x + int(10 * math.cos(math.radians(self.rotation)))
            sparkle_y = draw_y + int(10 * math.sin(math.radians(self.rotation)))
            pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 3)

class WealthCraftGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("💰 WEALTH CRAFT - Pure Ruby Mining! 💰")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Player
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_width = 30
        self.player_height = 40
        self.player_speed = 5
        self.player_jump_power = 12
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.player_on_ground = False
        
        # Wealth
        self.gems = []
        self.spawn_gems()
        self.wealth = 0
        self.rubies = 0
        self.emeralds = 0
        self.diamonds = 0
        self.gold = 0
        
        # Level system
        self.level = 1
        self.experience = 0
        self.exp_to_next_level = 100
        self.total_earned = 0
        
        # New systems
        self.current_biome = BiomeType.FOREST
        self.current_weather = WeatherType.CLEAR
        self.weather_timer = 0
        self.time_of_day = 0  # 0-2400 for 24 hour cycle
        self.day_night_speed = 1
        
        # Achievements
        self.achievements = {achievement: False for achievement in AchievementType}
        self.achievement_notifications = []
        
        # Quests
        self.active_quests = []
        self.completed_quests = []
        self.quest_progress = {}
        
        # Combat
        self.player_health = 100
        self.player_max_health = 100
        self.combat_mode = False
        self.enemies = []
        self.player_damage = 10
        self.shield_active = False
        self.shield_timer = 0
        
        # Power-ups
        self.active_powerups = {}
        self.speed_boost = 1
        self.wealth_multiplier = 1
        self.instant_mine = False
        self.magnet_boost = 1
        self.xray_vision = False
        
        # Visual enhancements
        self.player_color = BLUE
        self.character_outfit = "basic"
        self.particle_effects = []
        self.animation_timer = 0
        self.particles = []  # Add missing particles list
        
        # World expansion
        self.explored_areas = set()
        self.structures = []
        self.npcs = []
        self.vehicles = []
        self.pets = []
        
        # Save system (moved after owned_tools is defined)
        # self.save_data will be initialized after owned_tools
        
        # Enhancement systems
        self.achievement_system = AchievementSystem()
        self.weather_system = WeatherSystem()
        self.powerups = []
        self.powerup_properties = {
            "speed_boost": {"color": (255, 255, 0), "duration": 10000},
            "double_wealth": {"color": (255, 215, 0), "duration": 15000},
            "instant_mine": {"color": (255, 100, 255), "duration": 8000},
            "magnet_boost": {"color": (100, 255, 255), "duration": 12000},
            "shield": {"color": (100, 100, 255), "duration": 20000},
            "xray_vision": {"color": (255, 255, 100), "duration": 10000}
        }
        self.quest_notifications = []
        self.total_mined = 0
        self.enemies_defeated = 0
        
        # Initialize enhancement systems
        self.enemies = []
        self.npcs = []
        self.structures = []
        self.pets = []
        self.active_quests = []
        self.completed_quests = []
        self.active_powerups = {}
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = 1
        self.wealth_multiplier = 1
        self.instant_mine = False
        self.magnet_boost = 1
        self.xray_vision = False
        self.time_of_day = 0
        self.day_night_speed = 1
        self.explored_areas = set()
        self.player_health = 100
        self.player_max_health = 100
        
        # Save system (now after owned_tools is defined)
        # self.save_data will be initialized after owned_tools
        
        # Mining
        self.pickaxe_power = 1
        self.mining_speed = 1
        self.auto_mine = False
        self.mine_progress = 0
        self.mining_multiplier = 1.0
        self.mining_combo = 0
        self.last_mine_time = 0
        
        # World
        self.world_width = 60
        self.world_height = 40
        self.blocks = [[0 for _ in range(self.world_height)] for _ in range(self.world_width)]
        self.generate_world()
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Quests will be checked in update loop
    
    def update(self):
        # Update all enhancement systems
        self.update_all_systems()
        
        # Update player
        keys = pygame.key.get_pressed()
        
        # Player movement with speed boost
        actual_speed = self.player_speed * self.speed_boost
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= actual_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += actual_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.player_on_ground:
                self.player_vel_y = -self.player_jump_power
                self.player_on_ground = False
                
        # Apply gravity
        self.player_vel_y += 0.5
        self.player_y += self.player_vel_y
        
        # Ground collision
        if self.player_y >= SCREEN_HEIGHT - 100 - self.player_height:
            self.player_y = SCREEN_HEIGHT - 100 - self.player_height
            self.player_vel_y = 0
            self.player_on_ground = True
            
        # World boundaries
        self.player_x = max(0, min(self.player_x, self.world_width * 40 - self.player_width))
        
        # Update camera
        self.camera_x = max(0, min(self.player_x - SCREEN_WIDTH // 2, self.world_width * 40 - SCREEN_WIDTH))
        
        # Auto-mining with instant mine power-up
        if self.auto_mine:
            if self.instant_mine:
                base_speed = 100  # Instant mining
            else:
                base_speed = self.mining_speed * self.mining_multiplier
                
            if self.mining_combo > 0:
                combo_bonus = 1 + (self.mining_combo * 0.2)
                base_speed *= combo_bonus
                
            self.mine_progress += base_speed
            
            # Combo timing
            current_time = pygame.time.get_ticks()
            if current_time - self.last_mine_time < 1000:
                self.mining_combo += 1
            else:
                self.mining_combo = 0
            self.last_mine_time = current_time
            
            if self.mine_progress >= 100:
                self.mine_progress = 0
                
                # Earn wealth with multipliers
                base_earned = self.pickaxe_power * 25
                total_earned = int(base_earned * self.mining_multiplier * self.wealth_multiplier)
                if self.mining_combo > 5:
                    total_earned *= 2
                    
                self.wealth += total_earned
                self.total_earned += total_earned
                self.total_mined += 1
                self.gain_experience(total_earned // 5)
                
                # EPIC mining particles
                particle_count = self.pickaxe_power * 5
                if self.mining_combo > 5:
                    particle_count *= 2
                    
                for _ in range(particle_count):
                    particle = Particle(
                        self.player_x + self.player_width // 2 + random.randint(-30, 30),
                        self.player_y + self.player_height // 2 + random.randint(-30, 30),
                        random.uniform(-8, 8),
                        random.uniform(-15, -5),
                        (255, 215, 0),
                        random.randint(5, 15),
                        random.randint(30, 60)
                    )
                    self.particles.append(particle)
                        
        # Update gems
        for gem in self.gems[:]:
            gem.update()
            
            # Check collection with magnetic boost
            gem_rect = pygame.Rect(gem.x - 10, gem.y - 10, 20, 20)
            player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
            
            # Magnetic collection radius with boost
            collection_radius = 80 * self.magnet_boost
            player_center = (self.player_x + self.player_width // 2, self.player_y + self.player_height // 2)
            gem_center = (gem.x, gem.y)
            
            # Calculate distance
            distance = math.sqrt((player_center[0] - gem_center[0])**2 + (player_center[1] - gem_center[1])**2)
            
            # Magnetic pull effect
            if distance < collection_radius:
                # Pull gem toward player
                pull_strength = 5 * self.magnet_boost
                dx = player_center[0] - gem_center[0]
                dy = player_center[1] - gem_center[1]
                
                if distance > 0:
                    gem.x += (dx / distance) * pull_strength
                    gem.y += (dy / distance) * pull_strength
            
            # Collection detection
            if distance < 40 or gem_rect.colliderect(player_rect):
                gem.collected = True
                props = gem.properties[gem.type]
                
                if gem.type == GemType.RUBY:
                    self.rubies += 1
                    self.wealth += props["value"]
                elif gem.type == GemType.EMERALD:
                    self.emeralds += 1
                    self.wealth += props["value"]
                elif gem.type == GemType.DIAMOND:
                    self.diamonds += 1
                    self.wealth += props["value"]
                elif gem.type == GemType.GOLD:
                    self.gold += 1
                    self.wealth += props["value"]
                elif gem.type == GemType.SAPPHIRE:
                    self.wealth += props["value"]
                elif gem.type == GemType.AMETHYST:
                    self.wealth += props["value"]
                elif gem.type == GemType.CRYSTAL:
                    self.wealth += props["value"]
                elif gem.type == GemType.RARE_CRYSTAL:
                    self.wealth += props["value"]
                        
                # Apply wealth multiplier
                self.wealth = int(self.wealth * self.wealth_multiplier)
                self.total_earned += props["value"]
                self.gain_experience(props["value"] // 5)
                
                # Collection particles
                for _ in range(15):
                    particle = Particle(
                        gem.x,
                        gem.y,
                        random.uniform(-8, 8),
                        random.uniform(-10, -2),
                        props["color"],
                        random.randint(5, 12),
                        random.randint(30, 60)
                    )
                    self.particles.append(particle)
                        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def update_all_systems(self):
        """Update all game systems"""
        # Update weather
        self.weather_system.update()
        
        # Update day/night cycle
        self.update_day_night_cycle()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player_x, self.player_y)
            
            # Check collision with player
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 30, 30)
            player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
            
            if enemy_rect.colliderect(player_rect):
                if not self.shield_active:
                    self.player_health -= enemy.damage
                    if self.player_health <= 0:
                        self.player_health = 0
                        # Handle game over
                        
        # Update NPCs
        for npc in self.npcs:
            npc.update()
            
        # Update power-ups
        self.update_powerups()
        self.spawn_powerups()
        
        for powerup in self.powerups[:]:
            powerup.update()
            
            # Check collection
            powerup_rect = pygame.Rect(powerup.x, powerup.y, 20, 20)
            player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
            
            if powerup_rect.colliderect(player_rect) and not powerup.collected:
                powerup.collected = True
                self.activate_powerup(powerup.type)
                self.powerups.remove(powerup)
                
        # Update pets
        for pet in self.pets:
            pet.update(self.player_x, self.player_y)
            
        # Update achievements
        self.achievement_system.update()
        self.achievement_system.check_achievement("first_gem", self)
        self.achievement_system.check_achievement("wealthy", self)
        self.achievement_system.check_achievement("miner", self)
        
        # Update quests
        self.check_quests()
    
    def spawn_enemies(self):
        """Spawn enemies in the world"""
        enemy_types = ["goblin", "rock_monster", "creeper", "dragon", "ghost", "spider"]
        
        for _ in range(10):  # Spawn 10 enemies
            enemy_type = random.choice(enemy_types)
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            self.enemies.append(Enemy(x, y, enemy_type))
        
    def create_npcs(self):
        """Create NPC characters"""
        # Create shopkeeper
        self.npcs.append(NPC(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "shopkeeper"))
        
        # Create quest giver
        self.npcs.append(NPC(100, 100, "quest_giver"))
        
        # Create random villagers
        for _ in range(3):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.npcs.append(NPC(x, y, "villager"))
        
    def generate_structures(self):
        """Generate buildings and structures"""
        structure_types = ["house", "shop", "factory"]
        
        for _ in range(5):
            structure_type = random.choice(structure_types)
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            self.structures.append(Structure(x, y, structure_type))
        
    def generate_initial_quests(self):
        """Generate starting quests"""
        # Add collect gems quest
        quest1 = Quest(
            "collect_gems",
            10,
            {"wealth": 200, "experience": 100},
            "Collect 10 gems"
        )
        self.active_quests.append(quest1)
        
        # Add reach level quest
        quest2 = Quest(
            "reach_level",
            3,
            {"wealth": 500, "experience": 200},
            "Reach level 3"
        )
        self.active_quests.append(quest2)
        
        # Add mine blocks quest
        quest3 = Quest(
            "mine_blocks",
            50,
            {"wealth": 300, "experience": 150},
            "Mine 50 blocks"
        )
        self.active_quests.append(quest3)
    
    def update_day_night_cycle(self):
        """Update time of day"""
        self.time_of_day += self.day_night_speed
        if self.time_of_day >= 2400:
            self.time_of_day = 0
        
    def get_sky_color(self):
        """Get sky color based on time of day"""
        if 600 <= self.time_of_day <= 1800:  # Daytime
            return (135, 206, 235)  # Sky blue
        elif 1800 < self.time_of_day <= 2000:  # Sunset
            return (255, 150, 100)
        elif 2000 < self.time_of_day <= 600:  # Night
            return (25, 25, 112)
        else:  # Sunrise
            return (255, 200, 150)
    
    def spawn_powerups(self):
        """Spawn random power-ups"""
        if random.randint(1, 1000) == 1:  # 0.1% chance per frame
            powerup_types = ["speed_boost", "double_wealth", "instant_mine", "magnet_boost", "shield", "xray_vision"]
            powerup_type = random.choice(powerup_types)
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.powerups.append(PowerUp(x, y, powerup_type))
    
    def update_powerups(self):
        """Update active power-ups"""
        current_time = pygame.time.get_ticks()
        
        # Remove expired power-ups
        expired_powerups = []
        for powerup_type, start_time in self.active_powerups.items():
            duration = self.powerup_properties[powerup_type]["duration"]
            if current_time - start_time > duration:
                expired_powerups.append(powerup_type)
                
        for powerup_type in expired_powerups:
            del self.active_powerups[powerup_type]
            self.deactivate_powerup(powerup_type)
    
    def activate_powerup(self, powerup_type):
        """Activate a power-up effect"""
        current_time = pygame.time.get_ticks()
        self.active_powerups[powerup_type] = current_time
        
        if powerup_type == "speed_boost":
            self.speed_boost = 2
        elif powerup_type == "double_wealth":
            self.wealth_multiplier = 2
        elif powerup_type == "instant_mine":
            self.instant_mine = True
        elif powerup_type == "magnet_boost":
            self.magnet_boost = 2
        elif powerup_type == "shield":
            self.shield_active = True
        elif powerup_type == "xray_vision":
            self.xray_vision = True
    
    def deactivate_powerup(self, powerup_type):
        """Deactivate a power-up effect"""
        if powerup_type == "speed_boost":
            self.speed_boost = 1
        elif powerup_type == "double_wealth":
            self.wealth_multiplier = 1
        elif powerup_type == "instant_mine":
            self.instant_mine = False
        elif powerup_type == "magnet_boost":
            self.magnet_boost = 1
        elif powerup_type == "shield":
            self.shield_active = False
        elif powerup_type == "xray_vision":
            self.xray_vision = False
    
    def check_quests(self):
        """Check quest progress"""
        for quest in self.active_quests[:]:
            if quest.type == "collect_gems":
                total_gems = self.rubies + self.emeralds + self.diamonds + self.gold
                if quest.update_progress(total_gems - quest.progress):
                    self.complete_quest(quest)
            elif quest.type == "reach_level":
                if self.level >= quest.target:
                    quest.completed = True
                    self.complete_quest(quest)
            elif quest.type == "mine_blocks":
                if quest.update_progress(self.total_mined - quest.progress):
                    self.complete_quest(quest)
    
    def complete_quest(self, quest):
        """Complete a quest and give rewards"""
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # Give rewards
        self.wealth += quest.reward["wealth"]
        self.gain_experience(quest.reward["experience"])
        
        # Show completion message
        self.quest_notifications.append({"message": f"Quest Complete: {quest.description}!", "timer": 180})
    
    def gain_experience(self, amount):
        """Add experience and check for level up"""
        self.experience += amount
        
        # Check for level up
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # Exponential growth
            
            # Level up bonus
            bonus_wealth = self.level * 100
            self.wealth += bonus_wealth
            self.total_earned += bonus_wealth
    
    def draw_all_systems(self, screen):
        """Draw all game systems"""
        # Draw sky with day/night
        sky_color = self.get_sky_color()
        screen.fill(sky_color)
        
        # Draw weather
        self.weather_system.draw(screen)
        
        # Draw structures
        for structure in self.structures:
            structure.draw(screen, self.camera_x, self.camera_y)
            
        # Draw NPCs
        for npc in self.npcs:
            npc.draw(screen, self.camera_x, self.camera_y)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen, self.camera_x, self.camera_y)
            
        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(screen, self.camera_x, self.camera_y)
            
        # Draw pets
        for pet in self.pets:
            pet.draw(screen, self.camera_x, self.camera_y)
            
        # Draw achievements
        self.achievement_system.draw(screen)
        
        # Draw quest notifications
        for i, notification in enumerate(self.quest_notifications[:]):
            y_pos = 200 + i * 30
            font = pygame.font.Font(None, 24)
            text = font.render("✅ " + notification["message"], True, GREEN)
            screen.blit(text, (50, y_pos))
            
            notification["timer"] -= 1
            if notification["timer"] <= 0:
                self.quest_notifications.remove(notification)
        
        # Initialize enhancement systems
        self.owned_upgrades = {
            UpgradeType.PICKAXE: True,
            UpgradeType.STEEL_PICKAXE: False,
            UpgradeType.GOLDEN_PICKAXE: False,
            UpgradeType.DIAMOND_PICKAXE: False,
            UpgradeType.MEGA_DRILL: False,
            UpgradeType.QUANTUM_MINER: False,
            UpgradeType.RUBY_MAGNET: False,
            UpgradeType.LUCKY_CHARMS: False
        }
        
        self.upgrade_costs = {
            UpgradeType.PICKAXE: {"cost": 0, "level": 1, "name": "⛏️ Basic Pickaxe - Free"},
            UpgradeType.STEEL_PICKAXE: {"cost": 500, "level": 3, "name": "⚙️ Steel Pickaxe - Power x2, Speed x2"},
            UpgradeType.GOLDEN_PICKAXE: {"cost": 2000, "level": 6, "name": "🏆 Golden Pickaxe - Power x3, Speed x3"},
            UpgradeType.DIAMOND_PICKAXE: {"cost": 10000, "level": 12, "name": "💎 Diamond Pickaxe - Power x5, Speed x5"},
            UpgradeType.MEGA_DRILL: {"cost": 5000, "level": 8, "name": "⚡ MEGA Drill - Speed x10"},
            UpgradeType.QUANTUM_MINER: {"cost": 20000, "level": 15, "name": "🚀 Quantum Miner - Speed x25, Power x10"},
            UpgradeType.RUBY_MAGNET: {"cost": 3000, "level": 7, "name": "🧲 Ruby Magnet - 3x Multiplier"},
            UpgradeType.LUCKY_CHARMS: {"cost": 8000, "level": 10, "name": "🍀 Lucky Charms - 5x Gem Spawns"}
        }
        
        # Shop items
        self.owned_items = {
            ShopItem.STEEL_BOOTS: False,
            ShopItem.GOLDEN_BOOTS: False,
            ShopItem.DIAMOND_BOOTS: False,
            ShopItem.MINING_HELMET: False,
            ShopItem.LUCKY_PICKAXE: False,
            ShopItem.RUBY_DETECTOR: False,
            ShopItem.TREASURE_MAP: False,
            ShopItem.CAVE_LIGHT: False,
            ShopItem.EXPLOSIVES: False
        }
        
        self.shop_costs = {
            ShopItem.STEEL_BOOTS: {"cost": 300, "level": 2, "name": "🥾 Steel Boots - 2x Speed"},
            ShopItem.GOLDEN_BOOTS: {"cost": 1000, "level": 5, "name": "👟 Golden Boots - 3x Speed"},
            ShopItem.DIAMOND_BOOTS: {"cost": 5000, "level": 10, "name": "💎 Diamond Boots - 5x Speed"},
            ShopItem.MINING_HELMET: {"cost": 800, "level": 3, "name": "⛑️ Mining Helmet - 2x Power"},
            ShopItem.LUCKY_PICKAXE: {"cost": 1500, "level": 4, "name": "🍀 Lucky Pickaxe - 2x Gem Find"},
            ShopItem.RUBY_DETECTOR: {"cost": 2000, "level": 6, "name": "🔴 Ruby Detector - Shows Rubies"},
            ShopItem.TREASURE_MAP: {"cost": 3000, "level": 8, "name": "🗺️ Treasure Map - Shows All Gems"},
            ShopItem.CAVE_LIGHT: {"cost": 500, "level": 2, "name": "🔦 Cave Light - Brighter Underground"},
            ShopItem.EXPLOSIVES: {"cost": 100, "level": 1, "name": "💣 Explosives - Clear 3x3 Area"}
        }
        
        # Underground mining
        self.underground = None
        self.cave_entrances = []
        self.generate_caves()
        
        # Tools and weapons
        self.owned_tools = {
            ToolType.BASIC_PICKAXE: True,
            ToolType.STEEL_PICKAXE_TOOL: False,
            ToolType.GOLDEN_PICKAXE_TOOL: False,
            ToolType.DIAMOND_PICKAXE_TOOL: False,
            ToolType.MEGA_DRILL_TOOL: False,
            ToolType.QUANTUM_MINER_TOOL: False,
            ToolType.MINING_LASER: False,
            ToolType.PLASMA_CUTTER: False,
            ToolType.ANTI_MATTER_PICKAXE: False
        }
        
        self.owned_weapons = {
            WeaponType.BASIC_SWORD: True,
            WeaponType.STEEL_SWORD: False,
            WeaponType.GOLDEN_SWORD: False,
            WeaponType.DIAMOND_SWORD: False,
            WeaponType.LASER_GUN: False,
            WeaponType.PLASMA_RIFLE: False,
            WeaponType.ROCKET_LAUNCHER: False,
            WeaponType.ANTI_MATTER_CANNON: False
        }
        
        self.current_tool = ToolType.BASIC_PICKAXE
        self.current_weapon = WeaponType.BASIC_SWORD
        
        # Save system (now after owned_tools is defined)
        self.save_data = {
            "level": self.level,
            "wealth": self.wealth,
            "achievements": self.achievements,
            "owned_tools": self.owned_tools,
            "owned_weapons": self.owned_weapons,
            "owned_upgrades": self.owned_upgrades,
            "owned_items": self.owned_items
        }
        
        # Tool and weapon costs
        self.tool_costs = {
            ToolType.BASIC_PICKAXE: {"cost": 0, "level": 1, "name": "⛏️ Basic Pickaxe - Free"},
            ToolType.STEEL_PICKAXE_TOOL: {"cost": 800, "level": 3, "name": "⚙️ Steel Pickaxe - Power x2, Speed x2"},
            ToolType.GOLDEN_PICKAXE_TOOL: {"cost": 2500, "level": 6, "name": "🏆 Golden Pickaxe - Power x3, Speed x3"},
            ToolType.DIAMOND_PICKAXE_TOOL: {"cost": 12000, "level": 12, "name": "💎 Diamond Pickaxe - Power x5, Speed x5"},
            ToolType.MEGA_DRILL_TOOL: {"cost": 6000, "level": 8, "name": "⚡ MEGA Drill - Speed x10"},
            ToolType.QUANTUM_MINER_TOOL: {"cost": 25000, "level": 15, "name": "🚀 Quantum Miner - Speed x25, Power x10"},
            ToolType.MINING_LASER: {"cost": 8000, "level": 10, "name": "🔴 Mining Laser - Instant Mining"},
            ToolType.PLASMA_CUTTER: {"cost": 15000, "level": 13, "name": "🟣 Plasma Cutter - 3x3 Instant"},
            ToolType.ANTI_MATTER_PICKAXE: {"cost": 50000, "level": 20, "name": "⚫ Anti-Matter Pickaxe - 5x5 Instant"}
        }
        
        self.weapon_costs = {
            WeaponType.BASIC_SWORD: {"cost": 0, "level": 1, "name": "⚔️ Basic Sword - Free"},
            WeaponType.STEEL_SWORD: {"cost": 600, "level": 3, "name": "🗡️ Steel Sword - 2x Damage"},
            WeaponType.GOLDEN_SWORD: {"cost": 2000, "level": 6, "name": "🗡️ Golden Sword - 3x Damage"},
            WeaponType.DIAMOND_SWORD: {"cost": 8000, "level": 12, "name": "💎 Diamond Sword - 5x Damage"},
            WeaponType.LASER_GUN: {"cost": 5000, "level": 8, "name": "🔫 Laser Gun - Ranged Attack"},
            WeaponType.PLASMA_RIFLE: {"cost": 12000, "level": 13, "name": "🔫 Plasma Rifle - 3x Ranged"},
            WeaponType.ROCKET_LAUNCHER: {"cost": 20000, "level": 16, "name": "🚀 Rocket Launcher - Area Damage"},
            WeaponType.ANTI_MATTER_CANNON: {"cost": 40000, "level": 20, "name": "⚫ Anti-Matter Cannon - Ultimate"}
        }
        
    def generate_world(self):
        # Generate terrain
        for x in range(self.world_width):
            height = int(20 + 5 * math.sin(x * 0.1) + random.randint(-3, 3))
            
            for y in range(self.world_height):
                if y >= self.world_height - height:
                    if y == self.world_height - height:
                        self.blocks[x][y] = 1  # Grass
                    else:
                        self.blocks[x][y] = 2  # Dirt
                else:
                    self.blocks[x][y] = 0  # Air
                    
        # Add ore deposits
        for _ in range(15):
            x = random.randint(5, self.world_width - 5)
            y = random.randint(5, self.world_height - 10)
            self.blocks[x][y] = 3  # Ore block
            
        # Add gem deposits (rare)
        for _ in range(8):
            x = random.randint(5, self.world_width - 5)
            y = random.randint(5, self.world_height - 10)
            self.blocks[x][y] = 4  # Gem deposit
            
    def spawn_gems(self):
        # Spawn gems in the world
        for _ in range(20):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            
            # Random gem type with rarity
            rand = random.random()
            if rand < 0.5:
                gem_type = GemType.RUBY
            elif rand < 0.8:
                gem_type = GemType.EMERALD
            elif rand < 0.95:
                gem_type = GemType.DIAMOND
            else:
                gem_type = GemType.GOLD
                
            self.gems.append(Gem(x, y, gem_type))
            
    def generate_caves(self):
        # Generate cave entrances in overworld
        for _ in range(3):
            x = random.randint(10, self.world_width - 10)
            y = self.world_height - 8
            self.cave_entrances.append({"x": x, "y": y, "width": 3, "height": 3})
            
            # Create cave entrance in world
            for cx in range(x, x + 3):
                for cy in range(y, y + 3):
                    if 0 <= cx < self.world_width and 0 <= cy < self.world_height:
                        self.blocks[cx][cy] = 0  # Cave entrance
                        
    def enter_underground(self, entrance_x, entrance_y):
        # Generate underground world
        self.underground = {
            "width": 40,
            "height": 30,
            "blocks": [[0 for _ in range(30)] for _ in range(40)],
            "gems": [],
            "entrance_x": entrance_x,
            "entrance_y": entrance_y
        }
        
        # Generate underground cave
        for x in range(40):
            for y in range(30):
                if x == 0 or x == 39 or y == 0 or y == 29:
                    self.underground["blocks"][x][y] = UndergroundBlock.BEDROCK.value
                else:
                    self.underground["blocks"][x][y] = UndergroundBlock.STONE.value
                    
        # Add gold blocks
        for _ in range(15):
            x = random.randint(5, 35)
            y = random.randint(5, 25)
            self.underground["blocks"][x][y] = UndergroundBlock.GOLD_BLOCK.value
            
        # Add diamond blocks (rare)
        for _ in range(5):
            x = random.randint(5, 35)
            y = random.randint(5, 25)
            self.underground["blocks"][x][y] = UndergroundBlock.DIAMOND_BLOCK.value
            
        # Add SUS BLOBS (mystery blocks)
        for _ in range(8):
            x = random.randint(5, 35)
            y = random.randint(5, 25)
            self.underground["blocks"][x][y] = UndergroundBlock.SUS_BLOB.value
            
        # Add ruby veins
        for _ in range(10):
            x = random.randint(5, 35)
            y = random.randint(5, 25)
            self.underground["blocks"][x][y] = UndergroundBlock.RUBY_VEIN.value
            
        # Add emerald veins
        for _ in range(8):
            x = random.randint(5, 35)
            y = random.randint(5, 25)
            self.underground["blocks"][x][y] = UndergroundBlock.EMERALD_VEIN.value
            
        # Add underground gems
        for _ in range(15):
            x = random.randint(5, 35)
            y = random.randint(5, 25)
            gem_type = random.choice([GemType.RUBY, GemType.EMERALD, GemType.DIAMOND, GemType.GOLD])
            self.underground["gems"].append(Gem(x * 40 + 20, y * 40 + 20, gem_type))
            
    def mine_block(self, world_x, world_y):
        if 0 <= world_x < self.world_width and 0 <= world_y < self.world_height:
            block_type = self.blocks[world_x][world_y]
            
            if block_type == 0:  # Air
                return None
            elif block_type == 1:  # Grass
                self.blocks[world_x][world_y] = 0
                return {"type": "dirt", "value": 1}
            elif block_type == 2:  # Dirt
                self.blocks[world_x][world_y] = 0
                return {"type": "dirt", "value": 1}
            elif block_type == 3:  # Ore
                self.blocks[world_x][world_y] = 0
                # Random gem from ore
                rand = random.random()
                if rand < 0.3:
                    return {"type": "ruby", "value": 100}
                elif rand < 0.6:
                    return {"type": "emerald", "value": 200}
                elif rand < 0.9:
                    return {"type": "diamond", "value": 500}
                else:
                    return {"type": "gold", "value": 50}
            elif block_type == 4:  # Gem deposit
                self.blocks[world_x][world_y] = 0
                # Guaranteed gem
                rand = random.random()
                if rand < 0.2:
                    return {"type": "diamond", "value": 500}
                elif rand < 0.5:
                    return {"type": "emerald", "value": 200}
                elif rand < 0.8:
                    return {"type": "ruby", "value": 100}
                else:
                    return {"type": "gold", "value": 50}
                    
        return None
        
    def mine_underground_block(self, world_x, world_y):
        if not self.underground:
            return None
            
        if 0 <= world_x < 40 and 0 <= world_y < 30:
            block_type = self.underground["blocks"][world_x][world_y]
            
            if block_type == UndergroundBlock.STONE.value:
                return None
            elif block_type == UndergroundBlock.BEDROCK.value:
                return None
            elif block_type == UndergroundBlock.GOLD_BLOCK.value:
                self.underground["blocks"][world_x][world_y] = UndergroundBlock.STONE.value
                return {"type": "gold_block", "value": 500}
            elif block_type == UndergroundBlock.DIAMOND_BLOCK.value:
                self.underground["blocks"][world_x][world_y] = UndergroundBlock.STONE.value
                return {"type": "diamond_block", "value": 2000}
            elif block_type == UndergroundBlock.SUS_BLOB.value:
                self.underground["blocks"][world_x][world_y] = UndergroundBlock.STONE.value
                # Mystery reward!
                rand = random.random()
                if rand < 0.1:
                    return {"type": "anti_matter", "value": 10000}  # SUPER RARE!
                elif rand < 0.3:
                    return {"type": "diamond", "value": 500}
                elif rand < 0.6:
                    return {"type": "emerald", "value": 200}
                elif rand < 0.9:
                    return {"type": "ruby", "value": 100}
                else:
                    return {"type": "gold", "value": 50}
            elif block_type == UndergroundBlock.RUBY_VEIN.value:
                self.underground["blocks"][world_x][world_y] = UndergroundBlock.STONE.value
                return {"type": "ruby", "value": 100}
            elif block_type == UndergroundBlock.EMERALD_VEIN.value:
                self.underground["blocks"][world_x][world_y] = UndergroundBlock.STONE.value
                return {"type": "emerald", "value": 200}
                    
        return None
        if 0 <= world_x < self.world_width and 0 <= world_y < self.world_height:
            block_type = self.blocks[world_x][world_y]
            
            if block_type == 0:  # Air
                return None
            elif block_type == 1:  # Grass
                self.blocks[world_x][world_y] = 0
                return {"type": "dirt", "value": 1}
            elif block_type == 2:  # Dirt
                self.blocks[world_x][world_y] = 0
                return {"type": "dirt", "value": 1}
            elif block_type == 3:  # Ore
                self.blocks[world_x][world_y] = 0
                # Random gem from ore
                rand = random.random()
                if rand < 0.3:
                    return {"type": "ruby", "value": 100}
                elif rand < 0.6:
                    return {"type": "emerald", "value": 200}
                elif rand < 0.9:
                    return {"type": "diamond", "value": 500}
                else:
                    return {"type": "gold", "value": 50}
            elif block_type == 4:  # Gem deposit
                self.blocks[world_x][world_y] = 0
                # Guaranteed gem
                rand = random.random()
                if rand < 0.2:
                    return {"type": "diamond", "value": 500}
                elif rand < 0.5:
                    return {"type": "emerald", "value": 200}
                elif rand < 0.8:
                    return {"type": "ruby", "value": 100}
                else:
                    return {"type": "gold", "value": 50}
                    
        return None
        
    def update_player(self, keys):
        # Movement
        target_vel_x = 0
        target_vel_y = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            target_vel_x = -self.player_speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            target_vel_x = self.player_speed
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            target_vel_y = -self.player_speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            target_vel_y = self.player_speed
            
        self.player_vel_x = target_vel_x
        self.player_vel_y = target_vel_y
        
        # Apply gravity
        if not self.player_on_ground:
            self.player_vel_y += 0.8
            if self.player_vel_y > 15:
                self.player_vel_y = 15
                
        # Jump
        if keys[pygame.K_SPACE] and self.player_on_ground:
            self.player_vel_y = -self.player_jump_power
            self.player_on_ground = False
            
        # Move player
        self.player_x += self.player_vel_x
        self.player_y += self.player_vel_y
        
        # World collision
        self.resolve_player_collisions()
        
    def resolve_player_collisions(self):
        self.player_on_ground = False
        
        # Check ground collision
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        
        for x in range(player_rect.left // 40, player_rect.right // 40 + 1):
            for y in range(player_rect.top // 40, player_rect.bottom // 40 + 1):
                if 0 <= x < self.world_width and 0 <= y < self.world_height:
                    if self.blocks[x][y] != 0:
                        block_rect = pygame.Rect(x * 40, y * 40, 40, 40)
                        if player_rect.colliderect(block_rect):
                            if self.player_vel_y > 0:  # Falling
                                self.player_y = block_rect.top - self.player_height
                                self.player_on_ground = True
                                self.player_vel_y = 0
                            elif self.player_vel_y < 0:  # Jumping
                                self.player_y = block_rect.bottom
                                self.player_vel_y = 0
                            elif self.player_vel_x > 0:  # Moving right
                                self.player_x = block_rect.left - self.player_width
                                self.player_vel_x = 0
                            elif self.player_vel_x < 0:  # Moving left
                                self.player_x = block_rect.right
                                self.player_vel_x = 0
                            return
                            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.SHOP:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.UNDERGROUND:
                        # Exit underground
                        self.state = GameState.PLAYING
                        self.player_x = self.underground["entrance_x"] * 40
                        self.player_y = self.underground["entrance_y"] * 40 - 100
                    else:
                        self.state = GameState.MENU
                        
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.PLAYING:
                        self.player_on_ground = False
                        self.player_vel_y = -self.player_jump_power
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MENU:
                    self.handle_menu_click(event.pos)
                elif self.state == GameState.PLAYING:
                    self.handle_playing_click(event.pos)
                elif self.state == GameState.SHOP:
                    self.handle_shop_click(event.pos)
                elif self.state == GameState.UNDERGROUND:
                    self.handle_underground_click(event.pos)
                    
    def handle_menu_click(self, pos):
        # Start button
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        if start_rect.collidepoint(pos):
            self.state = GameState.PLAYING
            
    def handle_playing_click(self, pos):
        # Check for cave entrance first
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        
        for entrance in self.cave_entrances:
            entrance_rect = pygame.Rect(entrance["x"] * 40, entrance["y"] * 40, 
                                    entrance["width"] * 40, entrance["height"] * 40)
            if entrance_rect.colliderect(player_rect):
                # Enter underground
                self.enter_underground(entrance["x"], entrance["y"])
                self.state = GameState.UNDERGROUND
                self.player_x = 200  # Center in underground
                self.player_y = 200
                return
                
        # Mine block at mouse position
        world_x = (pos[0] + self.camera_x) // 40
        world_y = (pos[1] + self.camera_y) // 40
        
        result = self.mine_block(world_x, world_y)
        
        if result:
            # Add to wealth
            if result["type"] == "ruby":
                self.rubies += 1
                self.wealth += result["value"]
            elif result["type"] == "emerald":
                self.emeralds += 1
                self.wealth += result["value"]
            elif result["type"] == "diamond":
                self.diamonds += 1
                self.wealth += result["value"]
            elif result["type"] == "gold":
                self.gold += 1
                self.wealth += result["value"]
            elif result["type"] == "dirt":
                self.wealth += 1
                
            # Create mining particles
            for _ in range(10):
                particle = Particle(
                    world_x * 40 + 20,
                    world_y * 40 + 20,
                    random.uniform(-5, 5),
                    random.uniform(-8, -2),
                    GOLD,
                    random.randint(3, 8),
                    random.randint(20, 40)
                )
                self.particles.append(particle)
                
    def handle_underground_click(self, pos):
        # Mine underground blocks
        world_x = pos[0] // 40
        world_y = pos[1] // 40
        
        result = self.mine_underground_block(world_x, world_y)
        
        if result:
            # Add to wealth
            if result["type"] == "ruby":
                self.rubies += 1
                self.wealth += result["value"]
            elif result["type"] == "emerald":
                self.emeralds += 1
                self.wealth += result["value"]
            elif result["type"] == "diamond":
                self.diamonds += 1
                self.wealth += result["value"]
            elif result["type"] == "gold":
                self.gold += 1
                self.wealth += result["value"]
                
            # Create mining particles
            for _ in range(15):
                particle = Particle(
                    world_x * 40 + 20,
                    world_y * 40 + 20,
                    random.uniform(-8, 8),
                    random.uniform(-12, -4),
                    GOLD,
                    random.randint(5, 15),
                    random.randint(30, 60)
                )
                self.particles.append(particle)
                
    def handle_shop_click(self, pos):
        # Check upgrade buttons
        y_offset = 200
        
        for i, (upgrade_type, upgrade_info) in enumerate(self.upgrade_costs.items()):
            if not self.owned_upgrades[upgrade_type]:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_offset + i * 60, 400, 40)
                if button_rect.collidepoint(pos):
                    if self.wealth >= upgrade_info["cost"] and self.level >= upgrade_info["level"]:
                        self.wealth -= upgrade_info["cost"]
                        self.owned_upgrades[upgrade_type] = True
                        
                        # Apply upgrade effects
                        if upgrade_type == UpgradeType.STEEL_PICKAXE:
                            self.pickaxe_power = 2
                            self.mining_speed = 2
                        elif upgrade_type == UpgradeType.GOLDEN_PICKAXE:
                            self.pickaxe_power = 3
                            self.mining_speed = 3
                        elif upgrade_type == UpgradeType.DIAMOND_PICKAXE:
                            self.pickaxe_power = 5
                            self.mining_speed = 5
                        elif upgrade_type == UpgradeType.MEGA_DRILL:
                            self.mining_speed = 10
                        elif upgrade_type == UpgradeType.QUANTUM_MINER:
                            self.mining_speed = 25
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # Exponential growth
            
            # Level up bonus
            bonus_wealth = self.level * 100
            self.wealth += bonus_wealth
            self.total_earned += bonus_wealth
            
            # Create level up particles
            for _ in range(20):
                particle = Particle(
                    self.player_x + self.player_width // 2,
                    self.player_y + self.player_height // 2,
                    random.uniform(-10, 10),
                    random.uniform(-15, -5),
                    YELLOW,
                    random.randint(8, 20),
                    random.randint(40, 80)
                )
                self.particles.append(particle)
                    
    def draw_menu(self):
        self.screen.fill(SKY_BLUE)
        
        # Title
        title_text = self.font_large.render("💰 WEALTH CRAFT 💰", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Pure Ruby Mining Adventure!", True, RUBY_RED)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Start button
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, GREEN, start_rect)
        pygame.draw.rect(self.screen, WHITE, start_rect, 3)
        start_text = self.font_medium.render("START MINING", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_rect.center)
        self.screen.blit(start_text, start_text_rect)
        
        # Instructions
        instructions = [
            "⛏️ Mine blocks and discover valuable gems!",
            "💎 Collect Rubies, Emeralds, Diamonds & Gold!",
            "🛒 Buy upgrades to multiply your wealth!",
            "⚡ Build your mining empire!",
            "🌟 Become the ultimate gem tycoon!"
        ]
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - 350, 250 + i * 30))
            
    def draw_playing(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw world
        for x in range(self.world_width):
            for y in range(self.world_height):
                if self.blocks[x][y] != 0:
                    draw_x = x * 40 - self.camera_x
                    draw_y = y * 40 - self.camera_y
                    
                    if self.blocks[x][y] == 1:  # Grass
                        color = (34, 139, 34)
                    elif self.blocks[x][y] == 2:  # Dirt
                        color = BROWN
                    elif self.blocks[x][y] == 3:  # Ore
                        color = GRAY
                    elif self.blocks[x][y] == 4:  # Gem deposit
                        color = PURPLE
                    else:
                        color = BLACK
                        
                    pygame.draw.rect(self.screen, color, (draw_x, draw_y, 40, 40))
                    pygame.draw.rect(self.screen, BLACK, (draw_x, draw_y, 40, 40), 2)
                    
        # Draw gems
        for gem in self.gems:
            if not gem.collected:
                gem.draw(self.screen, self.camera_x, self.camera_y)
                
        # Draw player
        player_draw_x = self.player_x - self.camera_x
        player_draw_y = self.player_y - self.camera_y
        pygame.draw.rect(self.screen, BLUE, (player_draw_x, player_draw_y, self.player_width, self.player_height))
        pygame.draw.rect(self.screen, WHITE, (player_draw_x, player_draw_y, self.player_width, self.player_height), 2)
        
        # Draw player face
        pygame.draw.circle(self.screen, WHITE, (player_draw_x + 8, player_draw_y + 8), 3)
        pygame.draw.circle(self.screen, WHITE, (player_draw_x + 22, player_draw_y + 8), 3)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen, self.camera_x, self.camera_y)
            
        # Draw UI
        self.draw_ui()
        
    def draw_ui(self):
        # Stats panel
        panel_rect = pygame.Rect(10, 10, 300, 200)
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Level display
        level_text = self.font_medium.render(f"⭐ Level {self.level}", True, YELLOW)
        self.screen.blit(level_text, (20, 20))
        
        # Experience bar
        exp_rect = pygame.Rect(20, 55, 200, 15)
        pygame.draw.rect(self.screen, BLACK, exp_rect)
        exp_fill = pygame.Rect(20, 55, int(200 * self.experience / self.exp_to_next_level), 15)
        pygame.draw.rect(self.screen, GREEN, exp_fill)
        pygame.draw.rect(self.screen, WHITE, exp_rect, 2)
        
        exp_text = self.font_small.render(f"{self.experience}/{self.exp_to_next_level} EXP", True, WHITE)
        self.screen.blit(exp_text, (20, 72))
        
        # Wealth display
        wealth_text = self.font_medium.render(f"💰 Wealth: ${self.wealth}", True, GOLD)
        self.screen.blit(wealth_text, (20, 95))
        
        # Gem counts
        ruby_text = self.font_small.render(f"💎 Rubies: {self.rubies}", True, RUBY_RED)
        self.screen.blit(ruby_text, (20, 125))
        
        emerald_text = self.font_small.render(f"💚 Emeralds: {self.emeralds}", True, EMERALD_GREEN)
        self.screen.blit(emerald_text, (20, 150))
        
        diamond_text = self.font_small.render(f"💎 Diamonds: {self.diamonds}", True, DIAMOND_BLUE)
        self.screen.blit(diamond_text, (20, 175))
        
        gold_text = self.font_small.render(f"🪙 Gold: {self.gold}", True, GOLD)
        self.screen.blit(gold_text, (20, 200))
        
        # Mining stats
        power_text = self.font_small.render(f"⛏️ Power: {self.pickaxe_power}", True, WHITE)
        self.screen.blit(power_text, (20, 230))
        
        speed_text = self.font_small.render(f"⚡ Speed: {self.mining_speed}x", True, WHITE)
        self.screen.blit(speed_text, (20, 255))
        
        multiplier_text = self.font_small.render(f"✨ Multiplier: {self.mining_multiplier}x", True, WHITE)
        self.screen.blit(multiplier_text, (20, 280))
        
        # Auto-mine status
        if self.auto_mine:
            auto_text = self.font_small.render("🤖 AUTO-MINE: ON", True, GREEN)
            auto_color = GREEN
        else:
            auto_text = self.font_small.render("🤖 AUTO-MINE: OFF", True, RED)
            auto_color = RED
            
        auto_rect = pygame.Rect(20, 240, 150, 30)
        pygame.draw.rect(self.screen, auto_color, auto_rect)
        pygame.draw.rect(self.screen, WHITE, auto_rect, 2)
        self.screen.blit(auto_text, (25, 245))
        
        # Mining progress
        if self.auto_mine:
            progress_rect = pygame.Rect(20, 275, 150, 20)
            pygame.draw.rect(self.screen, BLACK, progress_rect)
            progress_fill = pygame.Rect(20, 275, int(150 * self.mine_progress / 100), 20)
            pygame.draw.rect(self.screen, GREEN, progress_fill)
            pygame.draw.rect(self.screen, WHITE, progress_rect, 2)
            
        # Combo display
        if self.mining_combo > 0:
            combo_text = self.font_small.render(f"🔥 COMBO x{self.mining_combo}!", True, ORANGE)
            self.screen.blit(combo_text, (20, 305))
            
        # Shop button
        shop_rect = pygame.Rect(SCREEN_WIDTH - 200, 50, 150, 40)
        pygame.draw.rect(self.screen, PURPLE, shop_rect)
        pygame.draw.rect(self.screen, WHITE, shop_rect, 3)
        shop_text = self.font_medium.render("SHOP", True, WHITE)
        shop_text_rect = shop_text.get_rect(center=shop_rect.center)
        self.screen.blit(shop_text, shop_text_rect)
        
        # Controls
        controls = [
            "WASD/Arrows: Move | Space: Jump",
            "Left Click: Mine | Right Click: Shop",
            "Auto-mine: Toggle with button",
            "Collect gems by walking over them!",
            "Walk into cave entrances to go underground!"
        ]
        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, WHITE)
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, 120 + i * 25))
            
    def draw_underground(self):
        self.screen.fill(BLACK)
        
        # Draw underground world
        for x in range(40):
            for y in range(30):
                if self.underground["blocks"][x][y] != 0:
                    draw_x = x * 40
                    draw_y = y * 40
                    
                    block_type = self.underground["blocks"][x][y]
                    
                    if block_type == UndergroundBlock.STONE.value:
                        color = GRAY
                    elif block_type == UndergroundBlock.BEDROCK.value:
                        color = BLACK
                    elif block_type == UndergroundBlock.GOLD_BLOCK.value:
                        color = GOLD
                    elif block_type == UndergroundBlock.DIAMOND_BLOCK.value:
                        color = DIAMOND_BLUE
                    elif block_type == UndergroundBlock.SUS_BLOB.value:
                        # Pulsing suspicious blob!
                        pulse = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
                        color = (pulse, 0, pulse)  # Purple pulsing
                    elif block_type == UndergroundBlock.RUBY_VEIN.value:
                        color = RUBY_RED
                    elif block_type == UndergroundBlock.EMERALD_VEIN.value:
                        color = EMERALD_GREEN
                    else:
                        color = BLACK
                        
                    pygame.draw.rect(self.screen, color, (draw_x, draw_y, 40, 40))
                    pygame.draw.rect(self.screen, WHITE, (draw_x, draw_y, 40, 40), 2)
                    
                    # Add special effects for valuable blocks
                    if block_type == UndergroundBlock.GOLD_BLOCK.value:
                        # Gold sparkle
                        sparkle_x = draw_x + 20 + int(5 * math.sin(pygame.time.get_ticks() * 0.01))
                        sparkle_y = draw_y + 20 + int(5 * math.cos(pygame.time.get_ticks() * 0.01))
                        pygame.draw.circle(self.screen, WHITE, (sparkle_x, sparkle_y), 3)
                    elif block_type == UndergroundBlock.DIAMOND_BLOCK.value:
                        # Diamond shine
                        shine_x = draw_x + 20
                        shine_y = draw_y + 20
                        pygame.draw.circle(self.screen, WHITE, (shine_x, shine_y), 5)
                        
        # Draw underground gems
        for gem in self.underground["gems"]:
            if not gem.collected:
                gem.draw(self.screen, 0, 0)  # No camera offset in underground
                
        # Draw player in underground
        pygame.draw.rect(self.screen, BLUE, (self.player_x, self.player_y, self.player_width, self.player_height))
        pygame.draw.rect(self.screen, WHITE, (self.player_x, self.player_y, self.player_width, self.player_height), 2)
        
        # Draw player face
        pygame.draw.circle(self.screen, WHITE, (self.player_x + 8, self.player_y + 8), 3)
        pygame.draw.circle(self.screen, WHITE, (self.player_x + 22, self.player_y + 8), 3)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen, 0, 0)
            
        # Draw UI
        self.draw_underground_ui()
        
    def draw_underground_ui(self):
        # Underground info panel
        panel_rect = pygame.Rect(10, 10, 300, 150)
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Level and wealth display
        level_text = self.font_medium.render(f"⭐ Level {self.level}", True, YELLOW)
        self.screen.blit(level_text, (20, 20))
        
        wealth_text = self.font_medium.render(f"💰 Wealth: ${self.wealth}", True, GOLD)
        self.screen.blit(wealth_text, (20, 50))
        
        # Underground info
        underground_text = self.font_small.render("🕳️ UNDERGROUND MINING", True, CYAN)
        self.screen.blit(underground_text, (20, 80))
        
        # Current tool and weapon
        tool_text = self.font_small.render(f"⛏️ Tool: {self.current_tool.name}", True, WHITE)
        self.screen.blit(tool_text, (20, 105))
        
        weapon_text = self.font_small.render(f"⚔️ Weapon: {self.current_weapon.name}", True, WHITE)
        self.screen.blit(weapon_text, (20, 130))
        
        # Exit instruction
        exit_text = self.font_medium.render("Press ESC to Exit Underground", True, RED)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(exit_text, exit_rect)
        # Stats panel
        panel_rect = pygame.Rect(10, 10, 300, 200)
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Level display
        level_text = self.font_medium.render(f"⭐ Level {self.level}", True, YELLOW)
        self.screen.blit(level_text, (20, 20))
        
        # Experience bar
        exp_rect = pygame.Rect(20, 55, 200, 15)
        pygame.draw.rect(self.screen, BLACK, exp_rect)
        exp_fill = pygame.Rect(20, 55, int(200 * self.experience / self.exp_to_next_level), 15)
        pygame.draw.rect(self.screen, GREEN, exp_fill)
        pygame.draw.rect(self.screen, WHITE, exp_rect, 2)
        
        exp_text = self.font_small.render(f"{self.experience}/{self.exp_to_next_level} EXP", True, WHITE)
        self.screen.blit(exp_text, (20, 72))
        
        # Wealth display
        wealth_text = self.font_medium.render(f"💰 Wealth: ${self.wealth}", True, GOLD)
        self.screen.blit(wealth_text, (20, 95))
        
        # Gem counts
        ruby_text = self.font_small.render(f"💎 Rubies: {self.rubies}", True, RUBY_RED)
        self.screen.blit(ruby_text, (20, 125))
        
        emerald_text = self.font_small.render(f"💚 Emeralds: {self.emeralds}", True, EMERALD_GREEN)
        self.screen.blit(emerald_text, (20, 150))
        
        diamond_text = self.font_small.render(f"💎 Diamonds: {self.diamonds}", True, DIAMOND_BLUE)
        self.screen.blit(diamond_text, (20, 175))
        
        gold_text = self.font_small.render(f"🪙 Gold: {self.gold}", True, GOLD)
        self.screen.blit(gold_text, (20, 200))
        
        # Mining stats
        power_text = self.font_small.render(f"⛏️ Power: {self.pickaxe_power}", True, WHITE)
        self.screen.blit(power_text, (20, 230))
        
        speed_text = self.font_small.render(f"⚡ Speed: {self.mining_speed}x", True, WHITE)
        self.screen.blit(speed_text, (20, 255))
        
        multiplier_text = self.font_small.render(f"✨ Multiplier: {self.mining_multiplier}x", True, WHITE)
        self.screen.blit(multiplier_text, (20, 280))
        
        # Auto-mine status
        if self.auto_mine:
            auto_text = self.font_small.render("🤖 AUTO-MINE: ON", True, GREEN)
            auto_color = GREEN
        else:
            auto_text = self.font_small.render("🤖 AUTO-MINE: OFF", True, RED)
            auto_color = RED
            
        auto_rect = pygame.Rect(20, 240, 150, 30)
        pygame.draw.rect(self.screen, auto_color, auto_rect)
        pygame.draw.rect(self.screen, WHITE, auto_rect, 2)
        self.screen.blit(auto_text, (25, 245))
        
        # Mining progress
        if self.auto_mine:
            progress_rect = pygame.Rect(20, 275, 150, 20)
            pygame.draw.rect(self.screen, BLACK, progress_rect)
            progress_fill = pygame.Rect(20, 275, int(150 * self.mine_progress / 100), 20)
            pygame.draw.rect(self.screen, GREEN, progress_fill)
            pygame.draw.rect(self.screen, WHITE, progress_rect, 2)
            
        # Combo display
        if self.mining_combo > 0:
            combo_text = self.font_small.render(f"🔥 COMBO x{self.mining_combo}!", True, ORANGE)
            self.screen.blit(combo_text, (20, 305))
            
        # Shop button
        shop_rect = pygame.Rect(SCREEN_WIDTH - 200, 50, 150, 40)
        pygame.draw.rect(self.screen, PURPLE, shop_rect)
        pygame.draw.rect(self.screen, WHITE, shop_rect, 3)
        shop_text = self.font_medium.render("SHOP", True, WHITE)
        shop_text_rect = shop_text.get_rect(center=shop_rect.center)
        self.screen.blit(shop_text, shop_text_rect)
        
        # Controls
        controls = [
            "WASD/Arrows: Move | Space: Jump",
            "Left Click: Mine | Right Click: Shop",
            "Auto-mine: Toggle with button",
            "Collect gems by walking over them!"
        ]
        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, WHITE)
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, 120 + i * 25))
            
    def draw_shop(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("🛒 UPGRADE SHOP 🛒", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title_text, title_rect)
        
        # Level and wealth display
        level_text = self.font_medium.render(f"⭐ Level {self.level}", True, YELLOW)
        self.screen.blit(level_text, (50, 80))
        
        wealth_text = self.font_medium.render(f"💰 Wealth: ${self.wealth}", True, GOLD)
        self.screen.blit(wealth_text, (50, 110))
        
        exp_text = self.font_small.render(f"📈 EXP: {self.experience}/{self.exp_to_next_level}", True, WHITE)
        self.screen.blit(exp_text, (50, 140))
        
        # Tab buttons
        tools_tab = pygame.Rect(50, 180, 150, 40)
        weapons_tab = pygame.Rect(210, 180, 150, 40)
        items_tab = pygame.Rect(370, 180, 150, 40)
        
        # Draw tabs
        pygame.draw.rect(self.screen, GREEN, tools_tab)
        pygame.draw.rect(self.screen, WHITE, tools_tab, 2)
        tools_text = self.font_medium.render("TOOLS", True, WHITE)
        tools_text_rect = tools_text.get_rect(center=tools_tab.center)
        self.screen.blit(tools_text, tools_text_rect)
        
        pygame.draw.rect(self.screen, PURPLE, weapons_tab)
        pygame.draw.rect(self.screen, WHITE, weapons_tab, 2)
        weapons_text = self.font_medium.render("WEAPONS", True, WHITE)
        weapons_text_rect = weapons_text.get_rect(center=weapons_tab.center)
        self.screen.blit(weapons_text, weapons_text_rect)
        
        pygame.draw.rect(self.screen, CYAN, items_tab)
        pygame.draw.rect(self.screen, WHITE, items_tab, 2)
        items_text = self.font_medium.render("ITEMS", True, WHITE)
        items_text_rect = items_text.get_rect(center=items_tab.center)
        self.screen.blit(items_text, items_text_rect)
        
        # Draw tools section
        y_offset = 240
        tool_title = self.font_medium.render("⛏️ MINING TOOLS", True, YELLOW)
        self.screen.blit(tool_title, (SCREEN_WIDTH // 2 - 100, y_offset))
        
        y_offset += 40
        for i, (tool_type, tool_info) in enumerate(self.tool_costs.items()):
            if tool_type != ToolType.BASIC_PICKAXE:  # Skip free one
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, y_offset + i * 45, 500, 40)
                
                if self.owned_tools[tool_type]:
                    color = GREEN
                    status = "OWNED"
                elif self.wealth >= tool_info["cost"] and self.level >= tool_info["level"]:
                    color = YELLOW
                    status = f"${tool_info['cost']} (Lvl {tool_info['level']})"
                else:
                    color = RED
                    if self.level < tool_info["level"]:
                        status = f"Lvl {tool_info['level']} Required"
                    else:
                        status = f"${tool_info['cost']} Required"
                        
                pygame.draw.rect(self.screen, color, button_rect)
                pygame.draw.rect(self.screen, WHITE, button_rect, 2)
                
                # Tool name
                name_text = self.font_small.render(tool_info["name"], True, WHITE)
                self.screen.blit(name_text, (button_rect.x + 10, button_rect.y + 5))
                
                # Status
                status_text = self.font_small.render(status, True, WHITE)
                self.screen.blit(status_text, (button_rect.x + 10, button_rect.y + 25))
                
        # Draw weapons section  
        weapons_y_offset = 540
        weapon_title = self.font_medium.render("⚔️ COMBAT WEAPONS", True, PURPLE)
        self.screen.blit(weapon_title, (SCREEN_WIDTH // 2 - 100, weapons_y_offset))
        
        weapons_y_offset += 40
        for i, (weapon_type, weapon_info) in enumerate(self.weapon_costs.items()):
            if weapon_type != WeaponType.BASIC_SWORD:  # Skip free one
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, weapons_y_offset + i * 45, 500, 40)
                
                if self.owned_weapons[weapon_type]:
                    color = GREEN
                    status = "OWNED"
                elif self.wealth >= weapon_info["cost"] and self.level >= weapon_info["level"]:
                    color = YELLOW
                    status = f"${weapon_info['cost']} (Lvl {weapon_info['level']})"
                else:
                    color = RED
                    if self.level < weapon_info["level"]:
                        status = f"Lvl {weapon_info['level']} Required"
                    else:
                        status = f"${weapon_info['cost']} Required"
                        
                pygame.draw.rect(self.screen, color, button_rect)
                pygame.draw.rect(self.screen, WHITE, button_rect, 2)
                
                # Weapon name
                name_text = self.font_small.render(weapon_info["name"], True, WHITE)
                self.screen.blit(name_text, (button_rect.x + 10, button_rect.y + 5))
                
                # Status
                status_text = self.font_small.render(status, True, WHITE)
                self.screen.blit(status_text, (button_rect.x + 10, button_rect.y + 25))
                
        # Back instruction
        back_text = self.font_small.render("Press ESC to go back", True, WHITE)
        self.screen.blit(back_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 30))
        
    def run(self):
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update
            if self.state == GameState.PLAYING:
                self.update()
                
            # Draw based on state
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_playing()
            elif self.state == GameState.SHOP:
                self.draw_shop()
            elif self.state == GameState.UNDERGROUND:
                self.draw_underground()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = WealthCraftGame()
    game.run()
