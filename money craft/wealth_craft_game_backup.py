#!/usr/bin/env python3
"""
WEALTH CRAFT - Pure Ruby Mining Adventure!
Mine massive wealth in an epic world of treasures!
"""

import pygame
import math
import random
import sys
from enum import Enum
from collections import defaultdict
from epic_boss_system import Boss, SpecialEffect
from ultimate_world_generation import WorldGenerator, BiomeType, TerrainType, StructureType
from fun_villages import Village, VillageType, RubyHill, BitcoinMine

# Underground mining blocks
class UndergroundBlock(Enum):
    STONE = 0
    DIRT = 1
    RUBY_VEIN = 2
    EMERALD_VEIN = 3
    DIAMOND_VEIN = 4
    GOLD_VEIN = 5
    BEDROCK = 6

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Colors - VIBRANT AND FUN!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
LIME = (50, 205, 50)
GOLD = (255, 215, 0)
RUBY_RED = (220, 20, 60)
EMERALD_GREEN = (0, 100, 0)
DIAMOND_BLUE = (185, 242, 255)
SAPPHIRE_BLUE = (15, 82, 186)
AMETHYST_PURPLE = (153, 102, 204)
CRYSTAL_WHITE = (255, 255, 255)
RAINBOW_COLORS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
BITCOIN_ORANGE = (247, 147, 26)
BITCOIN_GOLD = (255, 203, 0)

# Fun colors
SKY_BLUE = (135, 206, 235)
SUNNY_YELLOW = (255, 255, 224)
GRASS_GREEN = (34, 139, 34)
MOUNTAIN_BROWN = (139, 90, 43)
VOLCANO_RED = (178, 34, 34)
LAVA_GLOW = (255, 69, 0)
WATER_BLUE = (64, 164, 223)
SAND_TAN = (238, 203, 173)
SNOW_WHITE = (255, 250, 250)
SWAMP_GREEN = (85, 107, 47)
MYSTICAL_PURPLE = (147, 112, 219)
CRYSTAL_PINK = (255, 182, 193)
UNDERWORLD_BLACK = (25, 25, 25)
SKY_ISLAND_BLUE = (173, 216, 230)
LIGHT_GRAY = (192, 192, 192)  # Missing color!

# Game states
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    SHOP = 2
    UNDERGROUND = 3

# Gem types - EXPANDED WITH BITCOIN!
class GemType(Enum):
    RUBY = 0
    EMERALD = 1
    DIAMOND = 2
    GOLD = 3
    SAPPHIRE = 4
    AMETHYST = 5
    CRYSTAL = 6
    RARE_CRYSTAL = 7
    ANCIENT_GEM = 8
    RAINBOW_GEM = 9
    DRAGON_GEM = 10
    COSMIC_GEM = 11
    QUANTUM_GEM = 12
    INFINITY_GEM = 13
    BITCOIN = 14  # NEW! BITCOIN GEM!
    
# Special effects
class EffectType(Enum):
    EXPLOSION = 0
    LIGHTNING = 1
    FIRE = 2
    ICE = 3
    POISON = 4
    HEAL = 5
    TELEPORT = 6
    TIME_WARP = 7
    BLACK_HOLE = 8
    
# Boss types
class BossType(Enum):
    CRYSTAL_GOLEM = 0
    SHADOW_DRAGON = 1
    QUANTUM_BEAST = 2
    COSMIC_TITAN = 3
    INFINITY_WARRIOR = 4
    
# Vehicle types
class VehicleType(Enum):
    MINECART = 0
    DRILL_MACHINE = 1
    FLYING_SHIP = 2
    TELEPORTER = 3
    TIME_MACHINE = 4
    QUANTUM_PORTAL = 5

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

# EPIC NEW FEATURES - LEGENDARY ADDITIONS!
class AchievementType(Enum):
    FIRST_RUBY = 0
    RICH_MINER = 1
    BOSS_HUNTER = 2
    EXPLORER = 3
    SPEED_MINER = 4
    LUCKY_FIND = 5
    MEGA_WEALTH = 6
    DRAGON_SLAYER = 7
    BITCOIN_MINER = 8
    LEGENDARY_STATUS = 9

class MiniGameType(Enum):
    RUBY_RUSH = 0
    LUCKY_SLOTS = 1
    BOSS_BATTLE = 2
    TREASURE_HUNT = 3
    SPACE_MISSION = 4
    DRAGON_RACE = 5

class CharacterSkin(Enum):
    MINER = 0
    NINJA = 1
    ROBOT = 2
    WIZARD = 3
    DRAGON = 4
    ASTRONAUT = 5
    PIRATE = 6
    SUPERHERO = 7

class CastleUpgrade(Enum):
    TOWER = 0
    WALL = 1
    TREASURY = 2
    WORKSHOP = 3
    GARDEN = 4
    DUNGEON = 5
    OBSERVATORY = 6
    THRONE_ROOM = 7

class SpaceFeature(Enum):
    ROCKET = 0
    MOON_BASE = 1
    SPACE_STATION = 2
    ASTEROID_MINE = 3
    ALIEN_TRADING = 4
    BLACK_HOLE = 5
    NEBULA = 6
    COSMIC_PORTAL = 7

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
        
        # Gem properties - EPIC EXPANSION WITH BITCOIN!
        self.properties = {
            GemType.RUBY: {"color": RUBY_RED, "value": 100, "name": "Ruby", "rarity": 1, "effect": None},
            GemType.EMERALD: {"color": EMERALD_GREEN, "value": 200, "name": "Emerald", "rarity": 2, "effect": None},
            GemType.DIAMOND: {"color": DIAMOND_BLUE, "value": 500, "name": "Diamond", "rarity": 3, "effect": None},
            GemType.GOLD: {"color": GOLD, "value": 50, "name": "Gold", "rarity": 1, "effect": None},
            GemType.SAPPHIRE: {"color": BLUE, "value": 300, "name": "Sapphire", "rarity": 2, "effect": None},
            GemType.AMETHYST: {"color": PURPLE, "value": 400, "name": "Amethyst", "rarity": 3, "effect": None},
            GemType.CRYSTAL: {"color": WHITE, "value": 600, "name": "Crystal", "rarity": 4, "effect": None},
            GemType.RARE_CRYSTAL: {"color": LIGHT_GRAY, "value": 1000, "name": "Rare Crystal", "rarity": 5, "effect": None},
            GemType.ANCIENT_GEM: {"color": (139, 69, 19), "value": 2000, "name": "Ancient Gem", "rarity": 6, "effect": "heal"},
            GemType.RAINBOW_GEM: {"color": (255, 0, 255), "value": 5000, "name": "Rainbow Gem", "rarity": 7, "effect": "rainbow"},
            GemType.DRAGON_GEM: {"color": (255, 140, 0), "value": 10000, "name": "Dragon Gem", "rarity": 8, "effect": "fire"},
            GemType.COSMIC_GEM: {"color": (75, 0, 130), "value": 25000, "name": "Cosmic Gem", "rarity": 9, "effect": "cosmic"},
            GemType.QUANTUM_GEM: {"color": (0, 255, 255), "value": 50000, "name": "Quantum Gem", "rarity": 10, "effect": "quantum"},
            GemType.INFINITY_GEM: {"color": (255, 255, 255), "value": 100000, "name": "Infinity Gem", "rarity": 11, "effect": "infinity"},
            GemType.BITCOIN: {"color": BITCOIN_ORANGE, "value": 777777, "name": "₿ BITCOIN ₿", "rarity": 12, "effect": "bitcoin"}  # NEW!
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
        
        # EPIC VISUAL EFFECTS!
        props = self.properties[self.type]
        
        # Glowing aura for rare gems
        if props["rarity"] >= 5:
            glow_size = 20 + props["rarity"] * 3
            glow_alpha = 50 + abs(math.sin(self.glow_timer * 0.1)) * 30
            for i in range(3):
                pygame.draw.circle(screen, (*props["color"], glow_alpha // (i+1)), 
                                 (int(draw_x + 10), int(draw_y + 10)), 
                                 glow_size + i * 5, 1)
        
        # Rotating rainbow effect for rainbow gem
        if self.type == GemType.RAINBOW_GEM:
            rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), 
                             (0, 0, 255), (75, 0, 130), (148, 0, 211)]
            color_index = int(self.animation_frame / 10) % len(rainbow_colors)
            pygame.draw.circle(screen, rainbow_colors[color_index], (int(draw_x + 10), int(draw_y + 10)), 12)
        
        # Pulsing effect for infinity gem
        elif self.type == GemType.INFINITY_GEM:
            pulse = abs(math.sin(self.animation_frame * 0.2))
            size = int(8 + pulse * 8)
            pygame.draw.circle(screen, props["color"], (int(draw_x + 10), int(draw_y + 10)), size)
            # Infinity symbol
            pygame.draw.arc(screen, BLACK, (draw_x + 2, draw_y + 6, 6, 8), 0, math.pi, 2)
            pygame.draw.arc(screen, BLACK, (draw_x + 12, draw_y + 6, 6, 8), math.pi, 2 * math.pi, 2)
        
        # Special effects for other rare gems
        elif props["rarity"] >= 6:
            # Sparkle particles
            for _ in range(3):
                spark_x = draw_x + 10 + random.randint(-15, 15)
                spark_y = draw_y + 10 + random.randint(-15, 15)
                pygame.draw.circle(screen, WHITE, (int(spark_x), int(spark_y)), 1)
            pygame.draw.circle(screen, props["color"], (int(draw_x + 10), int(draw_y + 10)), 10)
        
        else:
            # Normal gem drawing
            pygame.draw.circle(screen, props["color"], (int(draw_x + 10), int(draw_y + 10)), 8)
        
        # Border
        pygame.draw.circle(screen, BLACK, (int(draw_x + 10), int(draw_y + 10)), 8, 1)
        
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
        
        # 🎮 EPIC NEW FEATURES - MOST FUN GAME EVER!
        self.achievements = {achievement: False for achievement in AchievementType}
        self.achievement_points = 0
        self.current_skin = CharacterSkin.MINER
        self.unlocked_skins = {CharacterSkin.MINER: True}
        self.minigame_scores = {}
        self.minigame_unlocked = {minigame: False for minigame in MiniGameType}
        self.minigame_unlocked[MiniGameType.RUBY_RUSH] = True  # Start with one minigame
        
        # 🏰 CASTLE BUILDING SYSTEM
        self.castle_level = 0
        self.castle_upgrades = {upgrade: 0 for upgrade in CastleUpgrade}
        self.castle_wealth_bonus = 1.0
        self.castle_production = {}
        
        # 🚀 SPACE EXPLORATION SYSTEM
        self.space_unlocked = False
        self.space_features = {feature: False for feature in SpaceFeature}
        self.space_wealth = 0
        self.alien_reputation = 0
        
        # 🎯 LEGENDARY POWERS
        self.rainbow_mode = False
        self.rainbow_timer = 0
        self.quantum_mode = False
        self.quantum_timer = 0
        self.infinity_mode = False
        self.infinity_timer = 0
        self.dragon_mode = False
        self.dragon_timer = 0
        
        # 🎪 MINI-GAME SYSTEM
        self.current_minigame = None
        self.minigame_timer = 0
        self.daily_bonus_claimed = False
        self.lucky_streak = 0
        self.treasure_hunt_clues = []
        
        # 🎨 VISUAL EFFECTS
        self.particle_effects = []
        self.screen_shake = 0
        self.rainbow_particles = []
        self.cosmic_particles = []
        self.celebration_timer = 0
        
        # 🎵 SOUND SYSTEM (simulated)
        self.sound_enabled = True
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.current_music = "menu"
        
        # 🏆 LEADERBOARD SYSTEM
        self.high_score = 0
        self.total_rubies_mined = 0
        self.total_bosses_defeated = 0
        self.play_time = 0
        self.session_start = pygame.time.get_ticks()
        
        # Mining
        self.pickaxe_power = 1
        self.mining_speed = 1
        self.auto_mine = False
        self.mine_progress = 0
        self.mining_multiplier = 1.0
        self.mining_combo = 0
        self.last_mine_time = 0
        
        # World
        self.world_width = 100  # Much bigger world!
        self.world_height = 80
        self.world_generator = WorldGenerator(self.world_width, self.world_height)
        self.world_generator.generate_world()
        self.blocks = self.world_generator.blocks
        self.biomes = self.world_generator.biomes
        self.structures = self.world_generator.structures
        self.cave_systems = self.world_generator.cave_systems
        self.ore_deposits = self.world_generator.ore_deposits
        self.treasure_chests = self.world_generator.treasure_chests
        self.dungeons = self.world_generator.dungeons
        self.volcanoes = self.world_generator.volcanoes
        self.mountains = self.world_generator.mountains
        
        # World features from INSANE WORLD GENERATION!
        self.current_biome = BiomeType.FOREST
        self.discovered_areas = set()
        self.mining_depth = 0
        self.underground_level = 0
        self.camera_x = 0
        self.camera_y = 0
        
        # 🌟 INSANE WORLD FEATURES!
        self.rainbow_bridges = self.world_generator.rainbow_bridges
        self.quantum_portals = self.world_generator.quantum_portals
        self.cosmic_observatories = self.world_generator.cosmic_observatories
        self.time_temples = self.world_generator.time_temples
        self.soul_altars = self.world_generator.soul_altars
        self.star_gates = self.world_generator.star_gates
        self.void_anchors = self.world_generator.void_anchors
        self.infinity_forges = self.world_generator.infinity_forges
        self.blood_altars = self.world_generator.blood_altars
        self.elemental_shrines = self.world_generator.elemental_shrines
        self.dimensional_rifts = self.world_generator.dimensional_rifts
        self.dragon_lairs = self.world_generator.dragon_lairs
        self.bitcoin_exchanges = self.world_generator.bitcoin_exchanges
        self.rainbow_valleys = self.world_generator.rainbow_valleys
        self.time_distorted_areas = self.world_generator.time_distorted_areas
        self.quantum_fields = self.world_generator.quantum_fields
        self.cosmic_realms = self.world_generator.cosmic_realms
        
        # Gems
        self.gems = []
        self.spawn_gems()
        
        # Particles
        self.particles = []
        
        # EPIC BOSS SYSTEM!
        self.bosses = []
        self.current_boss = None
        self.boss_battle_active = False
        self.boss_spawn_timer = 0
        self.boss_defeated_count = 0
        self.special_effects = []
        self.ultimate_mode = False
        self.ultimate_mode_timer = 0
        
        # Boss spawn conditions
        self.next_boss_spawn_wealth = 10000  # First boss at 10k wealth
        self.boss_difficulty_multiplier = 1.5
        
        # Boss notifications
        self.boss_notification = ""
        self.boss_notification_timer = 0
        
        # Player health
        self.player_health = 100
        self.player_max_health = 100
        
        # FUN VILLAGES AND SPECIAL LOCATIONS!
        self.villages = []
        self.ruby_hills = []
        self.bitcoin_mines = []
        self.generate_fun_locations()
        
        # Upgrades
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
        self.active_shop_tab = "tools"  # Track active shop tab
        
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
            
    def add_tunnel_entrances(self):
        """Add tunnel entrances to the world"""
        num_entrances = random.randint(3, 6)
        
        for _ in range(num_entrances):
            # Find suitable location for tunnel entrance
            attempts = 0
            while attempts < 50:
                x = random.randint(10, self.world_width - 10)
                y = random.randint(5, self.world_height - 5)
                
                # Check if location is suitable (on surface, not in water)
                if (self.blocks[x][y] == TerrainType.GRASS or 
                    self.blocks[x][y] == TerrainType.DIRT or
                    self.blocks[x][y] == TerrainType.STONE):
                    
                    # Check if area around is clear
                    suitable = True
                    for dx in range(-2, 3):
                        for dy in range(-1, 2):
                            check_x = x + dx
                            check_y = y + dy
                            if (0 <= check_x < self.world_width and 
                                0 <= check_y < self.world_height and
                                self.blocks[check_x][check_y] != TerrainType.AIR):
                                suitable = False
                                break
                                
                    if suitable:
                        # Place tunnel entrance
                        self.blocks[x][y] = TerrainType.CAVE_ENTRANCE
                        
                        # Add visual markers around entrance
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                marker_x = x + dx
                                marker_y = y + dy
                                if (0 <= marker_x < self.world_width and 
                                    0 <= marker_y < self.world_height and
                                    self.blocks[marker_x][marker_y] == TerrainType.AIR):
                                    # Add torch or marker
                                    if random.random() < 0.3:
                                        self.blocks[marker_x][marker_y] = 20  # Torch block
                        break
                        
                attempts += 1
                
    def generate_fun_locations(self):
        """Generate fun villages, ruby hills, and bitcoin mines"""
        # Generate FUN VILLAGES!
        num_villages = random.randint(4, 8)
        village_types = [VillageType.FUN_VILLAGE, VillageType.RUBY_VILLAGE, 
                        VillageType.BITCOIN_VILLAGE, VillageType.CRYSTAL_VILLAGE,
                        VillageType.DRAGON_VILLAGE, VillageType.RAINBOW_VILLAGE]
        
        for i in range(num_villages):
            x = random.randint(200, self.world_width * 40 - 200)
            y = random.randint(100, self.world_height * 40 - 200)
            village_type = random.choice(village_types)
            
            self.villages.append(Village(x, y, village_type))
            
        # Generate RUBY HILLS!
        num_ruby_hills = random.randint(3, 6)
        for i in range(num_ruby_hills):
            x = random.randint(150, self.world_width * 40 - 150)
            y = random.randint(150, self.world_height * 40 - 150)
            
            self.ruby_hills.append(RubyHill(x, y))
            
        # Generate BITCOIN MINES!
        num_bitcoin_mines = random.randint(2, 4)
        for i in range(num_bitcoin_mines):
            x = random.randint(200, self.world_width * 40 - 200)
            y = random.randint(200, self.world_height * 40 - 200)
            
            self.bitcoin_mines.append(BitcoinMine(x, y))
            
    def update_fun_locations(self):
        """Update all fun locations"""
        # Update villages
        for village in self.villages:
            village.update()
            
        # Update ruby hills
        for ruby_hill in self.ruby_hills:
            ruby_hill.update()
            
        # Update bitcoin mines
        for bitcoin_mine in self.bitcoin_mines:
            bitcoin_mine.update()
            
    def spawn_gems(self):
        # Spawn gems in the world with EPIC rarity system!
        for _ in range(30):  # More gems now!
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            
            # EPIC gem rarity system
            rand = random.random() * 100  # 0-100 scale
            
            if rand < 30:  # 30% - Ruby
                gem_type = GemType.RUBY
            elif rand < 50:  # 20% - Emerald  
                gem_type = GemType.EMERALD
            elif rand < 65:  # 15% - Diamond
                gem_type = GemType.DIAMOND
            elif rand < 75:  # 10% - Sapphire
                gem_type = GemType.SAPPHIRE
            elif rand < 82:  # 7% - Amethyst
                gem_type = GemType.AMETHYST
            elif rand < 87:  # 5% - Crystal
                gem_type = GemType.CRYSTAL
            elif rand < 91:  # 4% - Rare Crystal
                gem_type = GemType.RARE_CRYSTAL
            elif rand < 94:  # 3% - Ancient Gem
                gem_type = GemType.ANCIENT_GEM
            elif rand < 96:  # 2% - Rainbow Gem
                gem_type = GemType.RAINBOW_GEM
            elif rand < 98:  # 2% - Dragon Gem
                gem_type = GemType.DRAGON_GEM
            elif rand < 99.5:  # 1.5% - Cosmic Gem
                gem_type = GemType.COSMIC_GEM
            elif rand < 99.9:  # 0.4% - Quantum Gem
                gem_type = GemType.QUANTUM_GEM
            elif rand < 99.98:  # 0.08% - BITCOIN! (SUPER RARE!)
                gem_type = GemType.BITCOIN
            else:  # 0.02% - Infinity Gem (EXTREMELY RARE!)
                gem_type = GemType.INFINITY_GEM
                
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
        
    def generate_underground(self):
        """Generate underground mining tunnels"""
        if not self.underground:
            return
            
        # Create main tunnels
        for _ in range(3):
            start_x = random.randint(5, 35)
            start_y = random.randint(5, 25)
            
            # Dig tunnel
            current_x, current_y = start_x, start_y
            tunnel_length = random.randint(20, 40)
            
            for _ in range(tunnel_length):
                if 0 <= current_x < 40 and 0 <= current_y < 30:
                    # Clear tunnel area
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            tunnel_x = current_x + dx
                            tunnel_y = current_y + dy
                            if 0 <= tunnel_x < 40 and 0 <= tunnel_y < 30:
                                self.underground["blocks"][tunnel_x][tunnel_y] = 0
                                
                # Random tunnel direction
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                current_x += direction[0]
                current_y += direction[1]
                
        # Add ore deposits in tunnels
        for _ in range(15):
            ore_x = random.randint(5, 35)
            ore_y = random.randint(5, 25)
            
            if self.underground["blocks"][ore_x][ore_y] == 0:  # In tunnel
                ore_types = [
                    UndergroundBlock.RUBY_VEIN,
                    UndergroundBlock.EMERALD_VEIN,
                    UndergroundBlock.DIAMOND_VEIN,
                    UndergroundBlock.GOLD_VEIN
                ]
                ore_type = random.choice(ore_types)
                self.underground["blocks"][ore_x][ore_y] = ore_type.value
                
    def check_block_collision(self, x, y):
        """Check if player position would collide with blocks"""
        # Check player rectangle against blocks
        player_rect = pygame.Rect(x, y, self.player_width, self.player_height)
        
        # Check surrounding blocks
        start_x = max(0, int(x // 40) - 1)
        end_x = min(self.world_width, int((x + self.player_width) // 40) + 2)
        start_y = max(0, int(y // 40) - 1)
        end_y = min(self.world_height, int((y + self.player_height) // 40) + 2)
        
        for block_x in range(start_x, end_x):
            for block_y in range(start_y, end_y):
                block_type = self.blocks[block_x][block_y]
                if block_type != 0:  # Not air (0 is air, everything else is solid)
                    block_rect = pygame.Rect(block_x * 40, block_y * 40, 40, 40)
                    if player_rect.colliderect(block_rect):
                        return True
        return False
    
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
        """Handle shop button clicks"""
        # Check tab buttons first
        tools_tab = pygame.Rect(50, 180, 150, 50)
        weapons_tab = pygame.Rect(210, 180, 150, 50)
        items_tab = pygame.Rect(370, 180, 150, 50)
        bitcoin_tab = pygame.Rect(530, 180, 150, 50)
        
        # Check which tab was clicked
        if tools_tab.collidepoint(pos):
            self.active_shop_tab = "tools"
            return True
        elif weapons_tab.collidepoint(pos):
            self.active_shop_tab = "weapons"
            return True
        elif items_tab.collidepoint(pos):
            self.active_shop_tab = "items"
            return True
        elif bitcoin_tab.collidepoint(pos):
            self.active_shop_tab = "bitcoin"
            return True
            
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
                            self.pickaxe_power = 10
                        elif upgrade_type == UpgradeType.RUBY_MAGNET:
                            self.mining_multiplier = 3.0
                        elif upgrade_type == UpgradeType.LUCKY_CHARMS:
                            # Increase gem spawn rates
                            for _ in range(5):
                                self.spawn_gems()
                    return True
        
        # Check shop items based on active tab
        shop_y_offset = 400
        
        if self.active_shop_tab == "tools":
            for i, (tool_type, tool_info) in enumerate(self.tool_costs.items()):
                if tool_type != ToolType.BASIC_PICKAXE:  # Skip free one
                    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, shop_y_offset + i * 45, 500, 40)
                    if button_rect.collidepoint(pos):
                        if self.wealth >= tool_info["cost"] and self.level >= tool_info["level"]:
                            self.wealth -= tool_info["cost"]
                            self.owned_tools[tool_type] = True
                        return True
        elif self.active_shop_tab == "weapons":
            # Handle weapon purchases
            pass  # Add weapons later
        elif self.active_shop_tab == "items":
            # Handle item purchases
            pass  # Add items later
        elif self.active_shop_tab == "bitcoin":
            # Handle Bitcoin purchases
            pass  # Add Bitcoin items later
            
        return False
        
    def update_player(self, keys):
        """Handle player movement and actions"""
        # Store previous position for collision detection
        prev_x, prev_y = self.player_x, self.player_y
        
        # Ground walking movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_y += self.player_speed
            
        # Check if player is on ground level
        ground_y = self.get_ground_level(self.player_x)
        if self.player_y >= ground_y - 20:  # Near or on ground
            self.player_y = ground_y - 20  # Keep player on ground
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Underground mining tunnel entry (press E when near tunnel)
        if keys[pygame.K_e]:
            self.check_tunnel_entry()
            
        # Camera follow player
        self.camera_x = self.player_x - SCREEN_WIDTH // 2
        self.camera_y = self.player_y - SCREEN_HEIGHT // 2
        
        # Keep camera in bounds
        self.camera_x = max(0, min(self.camera_x, self.world_width * 40 - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world_height * 40 - SCREEN_HEIGHT))
        
    def get_ground_level(self, x):
        """Get ground level at given x position"""
        world_x = int(x // 40)
        if 0 <= world_x < self.world_width:
            for y in range(self.world_height):
                if self.blocks[world_x][y] != TerrainType.AIR:
                    return y * 40
        return self.world_height * 40  # Return bottom if no ground found
        
    def check_tunnel_entry(self):
        """Check if player can enter mining tunnel"""
        world_x = int(self.player_x // 40)
        world_y = int(self.player_y // 40)
        
        # Check for tunnel entrance (special blocks)
        if 0 <= world_x < self.world_width and 0 <= world_y < self.world_height:
            if self.blocks[world_x][world_y] == TerrainType.CAVE_ENTRANCE:
                self.enter_underground()
                
    def enter_underground(self):
        """Enter underground mining area"""
        if not self.underground:
            self.underground = {
                "level": 1,
                "blocks": [[0 for _ in range(30)] for _ in range(40)],
                "gems": [],
                "entrance_x": self.player_x // 40,
                "entrance_y": self.player_y // 40
            }
            self.generate_underground()
            # Move player to underground entrance
            self.player_x = 20 * 40  # Center of underground
            self.player_y = 15 * 40
            self.underground_level = 1
            
    def generate_underground(self):
        """Generate underground mining tunnels"""
        if not self.underground:
            return
            
        # Create main tunnels
        for _ in range(3):
            start_x = random.randint(5, 35)
            start_y = random.randint(5, 25)
            
            # Dig tunnel
            current_x, current_y = start_x, start_y
            tunnel_length = random.randint(20, 40)
            
            for _ in range(tunnel_length):
                if 0 <= current_x < 40 and 0 <= current_y < 30:
                    # Clear tunnel area
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            tunnel_x = current_x + dx
                            tunnel_y = current_y + dy
                            if 0 <= tunnel_x < 40 and 0 <= tunnel_y < 30:
                                self.underground["blocks"][tunnel_x][tunnel_y] = 0
                                
                # Random tunnel direction
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                current_x += direction[0]
                current_y += direction[1]
                
        # Add ore deposits in tunnels
        for _ in range(15):
            ore_x = random.randint(5, 35)
            ore_y = random.randint(5, 25)
            
            if self.underground["blocks"][ore_x][ore_y] == 0:  # In tunnel
                ore_types = [
                    UndergroundBlock.RUBY_VEIN,
                    UndergroundBlock.EMERALD_VEIN,
                    UndergroundBlock.DIAMOND_VEIN,
                    UndergroundBlock.GOLD_VEIN
                ]
                ore_type = random.choice(ore_types)
                self.underground["blocks"][ore_x][ore_y] = ore_type.value
        
    def update(self):
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            self.update_player(keys)
            
            # 🎮 UPDATE EPIC NEW FEATURES!
            self.update_legendary_powers()
            self.update_minigame()
            self.update_visual_effects()
            
            # Update boss battles
            self.update_boss_battle()
            
            # Update special effects
            self.update_special_effects()
            
            # Update ultimate mode
            self.update_ultimate_mode()
            
            # Update world systems
            self.update_world_systems()
            
            # Update mining depth
            self.update_mining_depth()
            
            # Generate fun locations
            self.generate_fun_locations()
            
            # Update fun locations
            self.update_fun_locations()
            
            # 🎯 CHECK FOR ACHIEVEMENTS!
            self.check_achievements()
            
            # 🏰 UPDATE CASTLE PRODUCTION
            self.update_castle_production()
            
            # 🚀 UPDATE SPACE FEATURES
            self.update_space_features()
            
            # 🏆 UPDATE PLAY TIME
            self.play_time = (pygame.time.get_ticks() - self.session_start) // 1000
            
            # Auto-mining
            if self.auto_mine:
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
                    # Earn wealth based on pickaxe power
                    base_earned = self.pickaxe_power * 25
                    total_earned = int(base_earned * self.mining_multiplier)
                    if self.mining_combo > 5:
                        total_earned *= 2
                        
                    self.wealth += total_earned
                    self.total_earned += total_earned
                    self.gain_experience(total_earned // 10)  # 1 exp per 10 wealth
                    self.last_mine_time = pygame.time.get_ticks()
                    
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
                            GOLD,
                            random.randint(5, 15),
                            random.randint(30, 60)
                        )
                        self.particles.append(particle)
                        
            # Update gems (enhanced with new gem types)
            for gem in self.gems[:]:
                gem.update()
                
                # Check collection
                gem_rect = pygame.Rect(gem.x - 10, gem.y - 10, 20, 20)
                player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
                if gem_rect.colliderect(player_rect) and not gem.collected:
                    gem.collected = True
                    props = gem.properties[gem.type]
                    
                    # Enhanced gem collection
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
                    elif gem.type == GemType.ANCIENT_GEM:
                        self.wealth += props["value"]
                        self.player_health = min(100, self.player_health + 20)  # Heal effect
                    elif gem.type == GemType.RAINBOW_GEM:
                        self.wealth += props["value"]
                        # Rainbow effect - spawn more gems
                        for _ in range(5):
                            self.spawn_gems()
                    elif gem.type == GemType.DRAGON_GEM:
                        self.wealth += props["value"]
                        # Fire effect - damage nearby enemies
                        if self.current_boss:
                            self.damage_boss(50)
                    elif gem.type == GemType.COSMIC_GEM:
                        self.wealth += props["value"]
                        # Cosmic effect - temporary invincibility
                        self.ultimate_mode = True
                        self.ultimate_mode_timer = 300
                    elif gem.type == GemType.QUANTUM_GEM:
                        self.wealth += props["value"]
                        # Quantum effect - instant mine boost
                        self.mining_speed = 100
                    elif gem.type == GemType.INFINITY_GEM:
                        self.wealth += props["value"]
                        # Infinity effect - massive wealth multiplier
                        self.wealth *= 2
                    elif gem.type == GemType.BITCOIN:
                        self.wealth += props["value"]
                        # BITCOIN effect - MASSIVE crypto wealth boost!
                        self.wealth += int(self.wealth * 0.5)  # 50% bonus!
                        self.boss_notification = "₿ BITCOIN MEGA BONUS! ₿"
                        self.boss_notification_timer = 300
                        
                    # Gain experience from gems
                    self.gain_experience(props["value"] // 5)
                    
                    # EPIC collection particles based on rarity
                    particle_count = 15 + props["rarity"] * 5
                    for _ in range(particle_count):
                        particle = Particle(
                            gem.x,
                            gem.y,
                            random.uniform(-6, 6),
                            random.uniform(-8, -2),
                            props["color"],
                            random.randint(3, 10),
                            random.randint(20, 40)
                        )
                        self.particles.append(particle)
                        
            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.life <= 0:
                    self.particles.remove(particle)
                    
    def gain_experience(self, amount):
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
            
            # Check for boss spawn
            self.check_boss_spawn()
            
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
                    
    def check_boss_spawn(self):
        """Check if conditions are met for boss spawn"""
        if not self.boss_battle_active and self.wealth >= self.next_boss_spawn_wealth:
            self.spawn_boss()
            
    def spawn_boss(self):
        """Spawn an epic boss based on player progress"""
        boss_types = ["crystal_golem", "shadow_dragon", "quantum_beast", "cosmic_titan", "infinity_warrior"]
        
        # Select boss based on wealth/progress
        if self.wealth < 25000:
            boss_type = "crystal_golem"
        elif self.wealth < 75000:
            boss_type = "shadow_dragon"
        elif self.wealth < 200000:
            boss_type = "quantum_beast"
        elif self.wealth < 1000000:
            boss_type = "cosmic_titan"
        else:
            boss_type = "infinity_warrior"
            
        # Spawn boss
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        self.current_boss = Boss(x, y, boss_type)
        self.boss_battle_active = True
        
        # Scale boss difficulty
        self.current_boss.health = int(self.current_boss.health * self.boss_difficulty_multiplier)
        self.current_boss.max_health = self.current_boss.health
        self.current_boss.damage = int(self.current_boss.damage * self.boss_difficulty_multiplier)
        
        # Create spawn effect
        self.special_effects.append(SpecialEffect(x, y, "explosion"))
        
        # Boss notification
        self.boss_notification = f"⚠️ EPIC BOSS BATTLE: {boss_type.replace('_', ' ').title()}! ⚠️"
        self.boss_notification_timer = 300
        
    def update_boss_battle(self):
        """Update boss battle mechanics"""
        if not self.boss_battle_active or not self.current_boss:
            return
            
        # Update boss
        self.current_boss.update(self.player_x, self.player_y)
        
        # Boss special attacks
        if self.current_boss.special_attack_cooldown == 0:
            self.execute_boss_special_attack()
            self.current_boss.special_attack_cooldown = 180  # 3 seconds at 60 FPS
            
        # Check collision with player
        boss_rect = pygame.Rect(self.current_boss.x - 40, self.current_boss.y - 40, 80, 80)
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        
        if boss_rect.colliderect(player_rect):
            if self.ultimate_mode:
                # Ultimate mode - damage boss instead
                self.damage_boss(100)
            else:
                # Take damage from boss
                self.player_health -= self.current_boss.damage
                if self.player_health <= 0:
                    self.player_health = 0
                    self.end_boss_battle(victory=False)
                    
        # Check if boss is defeated
        if self.current_boss and self.current_boss.health <= 0:
            self.end_boss_battle(victory=True)
            
    def execute_boss_special_attack(self):
        """Execute boss special attacks"""
        if not self.current_boss:
            return
            
        boss_type = self.current_boss.type
        
        if boss_type == "crystal_golem":
            # Crystal rain - falling crystals
            for _ in range(10):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(50, 200)
                self.special_effects.append(SpecialEffect(x, y, "explosion"))
                
        elif boss_type == "shadow_dragon":
            # Shadow breath - damaging area
            self.special_effects.append(SpecialEffect(self.current_boss.x, self.current_boss.y, "fire"))
            
        elif boss_type == "quantum_beast":
            # Quantum teleport - teleport around player
            for _ in range(5):
                x = self.player_x + random.randint(-200, 200)
                y = self.player_y + random.randint(-200, 200)
                self.special_effects.append(SpecialEffect(x, y, "teleport"))
                
        elif boss_type == "cosmic_titan":
            # Cosmic storm - multiple effects
            for _ in range(3):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
                self.special_effects.append(SpecialEffect(x, y, "lightning"))
                
        elif boss_type == "infinity_warrior":
            # Infinity blade - ultimate attack
            self.special_effects.append(SpecialEffect(self.current_boss.x, self.current_boss.y, "black_hole"))
            
    def damage_boss(self, damage):
        """Damage the current boss"""
        if self.current_boss:
            self.current_boss.health -= damage
            # Create damage effect
            self.special_effects.append(SpecialEffect(self.current_boss.x, self.current_boss.y, "explosion"))
            
    def end_boss_battle(self, victory):
        """End the boss battle"""
        if victory:
            # Victory rewards
            reward = self.current_boss.reward
            self.wealth += reward
            self.total_earned += reward
            self.boss_defeated_count += 1
            
            # Victory effects
            for _ in range(10):
                x = self.current_boss.x + random.randint(-50, 50)
                y = self.current_boss.y + random.randint(-50, 50)
                self.special_effects.append(SpecialEffect(x, y, "explosion"))
                
            # Notification
            self.boss_notification = f"🎉 VICTORY! Earned ${reward:,}! 🎉"
            self.boss_notification_timer = 300
            
            # Increase difficulty
            self.boss_difficulty_multiplier *= 1.2
            self.next_boss_spawn_wealth = int(self.next_boss_spawn_wealth * 1.5)
            
            # Unlock ultimate mode after certain victories
            if self.boss_defeated_count >= 3:
                self.ultimate_mode = True
                self.ultimate_mode_timer = 600  # 10 seconds
                self.boss_notification = "⚡ ULTIMATE MODE ACTIVATED! ⚡"
                self.boss_notification_timer = 300
                
        else:
            # Defeat penalty
            self.wealth = max(0, self.wealth // 2)  # Lose half wealth
            self.boss_notification = "💀 DEFEATED! Lost half wealth! 💀"
            self.boss_notification_timer = 300
            
        # Clean up
        self.current_boss = None
        self.boss_battle_active = False
        
    def update_special_effects(self):
        """Update all special effects"""
        for effect in self.special_effects[:]:
            effect.update()
            if effect.lifetime <= 0:
                self.special_effects.remove(effect)
                
    def update_ultimate_mode(self):
        """Update ultimate mode"""
        if self.ultimate_mode:
            self.ultimate_mode_timer -= 1
            if self.ultimate_mode_timer <= 0:
                self.ultimate_mode = False
                self.boss_notification = "⚡ Ultimate Mode Ended ⚡"
                self.boss_notification_timer = 180
    
    def update_world_systems(self):
        """Update world systems like volcanoes"""
        # Update volcanoes
        self.world_generator.update_volcanoes()
        
        # Update current biome based on player position
        player_grid_x = int(self.player_x // 40)
        if 0 <= player_grid_x < self.world_width:
            self.current_biome = self.biomes[player_grid_x][0]
            
        # Discover areas
        area_key = (player_grid_x // 10, self.underground_level)
        self.discovered_areas.add(area_key)
        
    def update_mining_depth(self):
        """Update mining depth and underground levels"""
        # Calculate current depth based on player Y position
        player_grid_y = int(self.player_y // 40)
        surface_level = self.get_surface_level(int(self.player_x // 40))
        
        if player_grid_y > surface_level:
            self.mining_depth = player_grid_y - surface_level
            
            # Update underground level
            self.underground_level = self.mining_depth // 20
            
            # Deeper levels = better rewards
            if self.underground_level > 0:
                depth_bonus = self.underground_level * 0.5
                self.mining_multiplier = 1.0 + depth_bonus
                
    def get_surface_level(self, x):
        """Get surface level at given X position"""
        if 0 <= x < self.world_width:
            for y in range(self.world_height):
                if self.blocks[x][y] != 0:
                    return y
        return self.world_height // 2
        
    def mine_block(self, x, y):
        """Mine a block with rewards based on type"""
        if 0 <= x < self.world_width and 0 <= y < self.world_height:
            block_type = self.blocks[x][y]
            
            if block_type != TerrainType.AIR:  # Not air
                # Base mining reward
                base_reward = 10
                gem_found = None
                
                # Special block rewards
                if block_type == TerrainType.STONE:
                    base_reward = 5
                elif block_type == TerrainType.RUBY_ORE:
                    gem_found = GemType.RUBY
                    base_reward = 100
                elif block_type == TerrainType.EMERALD_ORE:
                    gem_found = GemType.EMERALD
                    base_reward = 200
                elif block_type == TerrainType.DIAMOND_ORE:
                    gem_found = GemType.DIAMOND
                    base_reward = 500
                elif block_type == TerrainType.CRYSTAL_ORE:
                    gem_found = GemType.CRYSTAL
                    base_reward = 600
                elif block_type == TerrainType.DRAGON_ORE:
                    gem_found = GemType.DRAGON_GEM
                    base_reward = 10000
                elif block_type == TerrainType.QUANTUM_ORE:
                    gem_found = GemType.QUANTUM_GEM
                    base_reward = 50000
                elif block_type == TerrainType.LAVA:
                    # Mining lava is dangerous!
                    self.player_health -= 10
                    base_reward = 50
                elif block_type == TerrainType.MYSTICAL_ORE:
                    # Random rare gem
                    rare_gems = [GemType.ANCIENT_GEM, GemType.RAINBOW_GEM, GemType.COSMIC_GEM]
                    gem_found = random.choice(rare_gems)
                    base_reward = 5000
                    
                # Depth multiplier
                depth_multiplier = 1.0 + (self.underground_level * 0.5)
                total_reward = int(base_reward * depth_multiplier)
                
                self.wealth += total_reward
                self.total_earned += total_reward
                self.gain_experience(total_reward // 10)
                
                # Add gem if found
                if gem_found:
                    self.gems.append(Gem(x * 40, y * 40, gem_found))
                
                # Remove block
                self.blocks[x][y] = 0
                
                # Mining particles
                for _ in range(10):
                    particle = Particle(
                        x * 40 + 20,
                        y * 40 + 20,
                        random.uniform(-5, 5),
                        random.uniform(-8, -2),
                        (139, 69, 19),  # Brown
                        random.randint(3, 8),
                        random.randint(20, 40)
                    )
                    self.particles.append(particle)
                    
                # Return result for click handling
                if gem_found:
                    return {"type": gem_found.name.lower(), "value": total_reward}
                else:
                    return {"type": "stone", "value": total_reward}
        return False
        
    def open_treasure_chest(self, x, y):
        """Open a treasure chest"""
        for chest in self.treasure_chests[:]:
            if chest["x"] == x and chest["y"] == y and not chest["opened"]:
                chest["opened"] = True
                loot = chest["loot"]
                
                # Give rewards
                self.wealth += loot["wealth"]
                self.total_earned += loot["wealth"]
                
                # Add gems
                for _ in range(loot["gems"]):
                    gem_x = x * 40 + random.randint(-20, 20)
                    gem_y = y * 40 + random.randint(-20, 20)
                    
                    # Random gem based on chest rarity
                    if chest["rarity"] == "legendary":
                        gem_types = [GemType.INFINITY_GEM, GemType.QUANTUM_GEM, GemType.COSMIC_GEM]
                    elif chest["rarity"] == "epic":
                        gem_types = [GemType.DRAGON_GEM, GemType.RAINBOW_GEM, GemType.ANCIENT_GEM]
                    elif chest["rarity"] == "rare":
                        gem_types = [GemType.RARE_CRYSTAL, GemType.CRYSTAL, GemType.DIAMOND]
                    else:
                        gem_types = [GemType.RUBY, GemType.EMERALD, GemType.SAPPHIRE]
                        
                    self.gems.append(Gem(gem_x, gem_y, random.choice(gem_types)))
                    
                # Special item
                if loot["items"]:
                    # Could give special equipment
                    pass
                    
                # Create opening effect
                self.special_effects.append(SpecialEffect(x * 40 + 20, y * 40 + 20, "explosion"))
                
                # Notification
                self.boss_notification = f"💎 {chest['rarity'].title()} Chest Opened! +${loot['wealth']:,} 💎"
                self.boss_notification_timer = 180
                
                return True
        return False
    
    def draw_rainbow_bridge(self, screen, bridge):
        """Draw INSANE rainbow bridge!"""
        start_x = bridge["start_x"] * 40 - self.camera_x
        end_x = bridge["end_x"] * 40 - self.camera_x
        y = bridge["y"] * 40 - self.camera_y
        
        if -100 < start_x < SCREEN_WIDTH + 100 or -100 < end_x < SCREEN_WIDTH + 100:
            # Draw rainbow bridge with multiple colors
            bridge_width = 20
            for i, color in enumerate(bridge["colors"]):
                pygame.draw.line(screen, color, (start_x, y + i), (end_x, y + i), 3)
                
            # Sparkle effects
            for _ in range(5):
                sparkle_x = random.randint(int(start_x), int(end_x))
                sparkle_y = y + random.randint(-5, 25)
                pygame.draw.circle(screen, WHITE, (sparkle_x, sparkle_y), 2)
                
    def draw_quantum_portal(self, screen, portal):
        """Draw INSANE quantum portal!"""
        x = portal["x"] * 40 - self.camera_x
        y = portal["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Animated quantum portal
            time = pygame.time.get_ticks() // 100
            
            # Portal ring
            for i in range(5):
                radius = 20 + i * 5 + math.sin(time + i) * 3
                color = (100 + i * 30, 0, 200 - i * 30)
                pygame.draw.circle(screen, color, (int(x), int(y)), int(radius), 2)
                
            # Center glow
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 10)
            
            # Quantum particles
            for _ in range(8):
                angle = (time * 0.1 + _) * math.pi * 2 / 8
                particle_x = x + math.cos(angle) * 25
                particle_y = y + math.sin(angle) * 25
                pygame.draw.circle(screen, (0, 255, 255), (int(particle_x), int(particle_y)), 3)
                
    def draw_cosmic_observatory(self, screen, observatory):
        """Draw INSANE cosmic observatory!"""
        x = observatory["x"] * 40 - self.camera_x
        y = observatory["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Observatory dome
            pygame.draw.arc(screen, (100, 100, 200), (x - 30, y - 20, 60, 40), 0, math.pi, 3)
            pygame.draw.arc(screen, (200, 200, 255), (x - 25, y - 15, 50, 30), 0, math.pi, 2)
            
            # Telescope
            pygame.draw.rect(screen, (150, 150, 150), (x - 5, y - 10, 10, 20))
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y - 15)), 8)
            
            # Cosmic particles
            if observatory["active"]:
                for _ in range(5):
                    star_x = x + random.randint(-40, 40)
                    star_y = y + random.randint(-30, 10)
                    pygame.draw.circle(screen, (255, 255, 200), (int(star_x), int(star_y)), 1)
                    
    def draw_time_temple(self, screen, temple):
        """Draw INSANE time temple!"""
        x = temple["x"] * 40 - self.camera_x
        y = temple["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Temple building
            pygame.draw.rect(screen, (200, 150, 100), (x - 20, y - 15, 40, 30))
            pygame.draw.rect(screen, (255, 215, 0), (x - 20, y - 15, 40, 30), 3)
            
            # Time clock face
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 15)
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 15, 2)
            
            # Clock hands
            time = pygame.time.get_ticks() // 1000
            hour_angle = (time % 12) * math.pi / 6 - math.pi / 2
            minute_angle = (time % 60) * math.pi / 30 - math.pi / 2
            
            hour_x = x + math.cos(hour_angle) * 8
            hour_y = y + math.sin(hour_angle) * 8
            minute_x = x + math.cos(minute_angle) * 10
            minute_y = y + math.sin(minute_angle) * 10
            
            pygame.draw.line(screen, (0, 0, 0), (x, y), (int(hour_x), int(hour_y)), 3)
            pygame.draw.line(screen, (255, 0, 0), (x, y), (int(minute_x), int(minute_y)), 2)
            
            # Time particles
            if temple["active"]:
                for _ in range(3):
                    particle_x = x + random.randint(-25, 25)
                    particle_y = y + random.randint(-20, 20)
                    pygame.draw.circle(screen, (255, 215, 0), (int(particle_x), int(particle_y)), 2)
                    
    def draw_soul_altar(self, screen, altar):
        """Draw INSANE soul altar!"""
        x = altar["x"] * 40 - self.camera_x
        y = altar["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Altar base
            pygame.draw.rect(screen, (100, 0, 100), (x - 15, y - 10, 30, 20))
            pygame.draw.rect(screen, (200, 100, 200), (x - 15, y - 10, 30, 20), 3)
            
            # Soul crystal
            crystal_size = 10 + math.sin(pygame.time.get_ticks() * 0.001) * 3
            pygame.draw.polygon(screen, (255, 255, 255), [
                (x, y - crystal_size),
                (x - crystal_size, y),
                (x, y + crystal_size),
                (x + crystal_size, y)
            ])
            
            # Soul particles
            if altar["active"]:
                for _ in range(4):
                    soul_x = x + random.randint(-20, 20)
                    soul_y = y + random.randint(-15, 15)
                    pygame.draw.circle(screen, (255, 200, 255), (int(soul_x), int(soul_y)), 3)
                    
    def draw_star_gate(self, screen, gate):
        """Draw INSANE star gate!"""
        x = gate["x"] * 40 - self.camera_x
        y = gate["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Gate ring
            time = pygame.time.get_ticks() * 0.001
            for i in range(8):
                angle = time + i * math.pi / 4
                ring_x = x + math.cos(angle) * 25
                ring_y = y + math.sin(angle) * 25
                pygame.draw.circle(screen, (100, 200, 255), (int(ring_x), int(ring_y)), 8, 2)
                
            # Center portal
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 15)
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 15, 3)
            
            # Star particles
            if gate["active"]:
                for _ in range(6):
                    star_x = x + random.randint(-30, 30)
                    star_y = y + random.randint(-25, 25)
                    # Draw star shape
                    for i in range(5):
                        angle = i * math.pi * 2 / 5 - math.pi / 2
                        star_point_x = star_x + math.cos(angle) * 5
                        star_point_y = star_y + math.sin(angle) * 5
                        pygame.draw.circle(screen, (255, 255, 0), (int(star_point_x), int(star_point_y)), 2)
                        
    def draw_void_anchor(self, screen, anchor):
        """Draw INSANE void anchor!"""
        x = anchor["x"] * 40 - self.camera_x
        y = anchor["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Void anchor base
            pygame.draw.rect(screen, (50, 0, 50), (x - 20, y - 20, 40, 40))
            pygame.draw.rect(screen, (150, 0, 150), (x - 20, y - 20, 40, 40), 3)
            
            # Void core
            void_size = 15 + math.sin(pygame.time.get_ticks() * 0.002) * 5
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), int(void_size))
            pygame.draw.circle(screen, (200, 0, 200), (int(x), int(y)), int(void_size), 3)
            
            # Void particles
            if anchor["active"]:
                for _ in range(5):
                    void_x = x + random.randint(-25, 25)
                    void_y = y + random.randint(-20, 20)
                    pygame.draw.circle(screen, (100, 0, 100), (int(void_x), int(void_y)), 4)
                    
    def draw_infinity_forge(self, screen, forge):
        """Draw INSANE infinity forge!"""
        x = forge["x"] * 40 - self.camera_x
        y = forge["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Forge building
            pygame.draw.rect(screen, (200, 100, 0), (x - 25, y - 20, 50, 40))
            pygame.draw.rect(screen, (255, 165, 0), (x - 25, y - 20, 50, 40), 4)
            
            # Infinity symbol
            infinity_size = 20
            pygame.draw.ellipse(screen, (255, 255, 255), (x - infinity_size, y - 5, infinity_size * 2, 10), 3)
            
            # Forge particles
            if forge["active"]:
                for _ in range(8):
                    forge_x = x + random.randint(-30, 30)
                    forge_y = y + random.randint(-25, 25)
                    pygame.draw.circle(screen, (255, 200, 0), (int(forge_x), int(forge_y)), 3)
                    
    def draw_blood_altar(self, screen, altar):
        """Draw INSANE blood altar!"""
        x = altar["x"] * 40 - self.camera_x
        y = altar["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Altar base
            pygame.draw.rect(screen, (100, 0, 0), (x - 20, y - 15, 40, 30))
            pygame.draw.rect(screen, (200, 0, 0), (x - 20, y - 15, 40, 30), 3)
            
            # Blood pool
            pygame.draw.ellipse(screen, (150, 0, 0), (x - 15, y - 5, 30, 15))
            
            # Blood particles
            if altar["active"]:
                for _ in range(6):
                    blood_x = x + random.randint(-25, 25)
                    blood_y = y + random.randint(-20, 20)
                    pygame.draw.circle(screen, (200, 0, 0), (int(blood_x), int(blood_y)), 3)
                    
    def draw_elemental_shrine(self, screen, shrine):
        """Draw INSANE elemental shrine!"""
        x = shrine["x"] * 40 - self.camera_x
        y = shrine["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Elemental colors
            element_colors = {
                "fire": (255, 0, 0),
                "water": (0, 100, 255),
                "earth": (139, 69, 19),
                "air": (200, 200, 255),
                "lightning": (255, 255, 0),
                "ice": (200, 255, 255)
            }
            
            color = element_colors.get(shrine["element"], (255, 255, 255))
            
            # Shrine base
            pygame.draw.rect(screen, color, (x - 15, y - 15, 30, 30))
            pygame.draw.rect(screen, WHITE, (x - 15, y - 15, 30, 30), 2)
            
            # Elemental symbol
            pygame.draw.circle(screen, WHITE, (int(x), int(y)), 10)
            pygame.draw.circle(screen, color, (int(x), int(y)), 8)
            
            # Elemental particles
            if shrine["active"]:
                for _ in range(4):
                    element_x = x + random.randint(-20, 20)
                    element_y = y + random.randint(-15, 15)
                    pygame.draw.circle(screen, color, (int(element_x), int(element_y)), 2)
                    
    def draw_dimensional_rift(self, screen, rift):
        """Draw INSANE dimensional rift!"""
        x = rift["x"] * 40 - self.camera_x
        y = rift["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Rift effect
            time = pygame.time.get_ticks() * 0.001
            for i in range(6):
                offset = math.sin(time + i) * 10
                pygame.draw.ellipse(screen, (200, 0, 255), 
                                   (x - 25 + offset, y - 15 + offset, 50, 30), 2)
                
            # Portal center
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 20)
            pygame.draw.circle(screen, (255, 0, 255), (int(x), int(y)), 20, 3)
            
            # Dimensional particles
            if rift["active"]:
                for _ in range(8):
                    rift_x = x + random.randint(-30, 30)
                    rift_y = y + random.randint(-25, 25)
                    pygame.draw.circle(screen, (255, 0, 255), (int(rift_x), int(rift_y)), 3)
                    
    def draw_dragon_lair(self, screen, lair):
        """Draw INSANE dragon lair!"""
        x = lair["x"] * 40 - self.camera_x
        y = lair["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Dragon colors
            dragon_colors = {
                "fire": (255, 100, 0),
                "ice": (200, 200, 255),
                "lightning": (255, 255, 0),
                "shadow": (50, 50, 50),
                "cosmic": (200, 0, 200)
            }
            
            color = dragon_colors.get(lair["dragon_type"], (255, 100, 0))
            
            # Lair entrance
            pygame.draw.ellipse(screen, color, (x - 30, y - 20, 60, 40), 3)
            pygame.draw.ellipse(screen, (0, 0, 0), (x - 25, y - 15, 50, 30))
            
            # Dragon particles
            if lair["active"]:
                for _ in range(6):
                    dragon_x = x + random.randint(-35, 35)
                    dragon_y = y + random.randint(-25, 25)
                    pygame.draw.circle(screen, color, (int(dragon_x), int(dragon_y)), 4)
                    
    def draw_bitcoin_exchange(self, screen, exchange):
        """Draw INSANE bitcoin exchange!"""
        x = exchange["x"] * 40 - self.camera_x
        y = exchange["y"] * 40 - self.camera_y
        
        if -100 < x < SCREEN_WIDTH + 100 and -100 < y < SCREEN_HEIGHT + 100:
            # Exchange building
            pygame.draw.rect(screen, BITCOIN_ORANGE, (x - 25, y - 20, 50, 40))
            pygame.draw.rect(screen, BITCOIN_GOLD, (x - 25, y - 20, 50, 40), 4)
            
            # Bitcoin logo
            font = pygame.font.Font(None, 24)
            btc_text = font.render("₿", True, BLACK)
            screen.blit(btc_text, (x - 10, y - 10))
            
            # Trading particles
            if exchange["active"]:
                for _ in range(8):
                    btc_x = x + random.randint(-30, 30)
                    btc_y = y + random.randint(-25, 25)
                    pygame.draw.circle(screen, BITCOIN_GOLD, (int(btc_x), int(btc_y)), 3)
                    
    def draw_rainbow_valley(self, screen, valley):
        """Draw INSANE rainbow valley!"""
        start_x = valley["start_x"] * 40 - self.camera_x
        end_x = valley["end_x"] * 40 - self.camera_x
        y = valley["y"] * 40 - self.camera_y
        
        if -100 < start_x < SCREEN_WIDTH + 100 or -100 < end_x < SCREEN_WIDTH + 100:
            # Rainbow valley effect
            colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130)]
            
            for i, color in enumerate(colors):
                valley_y = y + i * 5
                pygame.draw.line(screen, color, (start_x, valley_y), (end_x, valley_y), 8)
                
            # Sparkle effects
            for _ in range(10):
                sparkle_x = random.randint(int(start_x), int(end_x))
                sparkle_y = y + random.randint(-10, 40)
                pygame.draw.circle(screen, WHITE, (sparkle_x, sparkle_y), 2)
                
    def draw_time_distorted_area(self, screen, area):
        """Draw INSANE time distorted area!"""
        x = area["x"] * 40 - self.camera_x
        y = area["y"] * 40 - self.camera_y
        radius = area["radius"] * 40
        
        if -radius < x < SCREEN_WIDTH + radius and -radius < y < SCREEN_HEIGHT + radius:
            # Time distortion effect
            time = pygame.time.get_ticks() * 0.001
            for i in range(5):
                distortion = math.sin(time + i) * 10
                pygame.draw.circle(screen, (200, 200, 255), 
                                 (int(x + distortion), int(y + distortion)), 
                                 radius // 2, 2)
                
            # Time particles
            if area["active"]:
                for _ in range(6):
                    time_x = x + random.randint(-radius, radius)
                    time_y = y + random.randint(-radius, radius)
                    pygame.draw.circle(screen, (255, 255, 255), (int(time_x), int(time_y)), 3)
                    
    def draw_quantum_field(self, screen, field):
        """Draw INSANE quantum field!"""
        x = field["x"] * 40 - self.camera_x
        y = field["y"] * 40 - self.camera_y
        radius = field["radius"] * 40
        
        if -radius < x < SCREEN_WIDTH + radius and -radius < y < SCREEN_HEIGHT + radius:
            # Quantum field effect
            time = pygame.time.get_ticks() * 0.002
            for i in range(8):
                angle = time + i * math.pi / 4
                quantum_x = x + math.cos(angle) * radius
                quantum_y = y + math.sin(angle) * radius
                pygame.draw.circle(screen, (0, 255, 255), (int(quantum_x), int(quantum_y)), 10, 2)
                
            # Quantum particles
            if field["active"]:
                for _ in range(12):
                    quantum_x = x + random.randint(-radius, radius)
                    quantum_y = y + random.randint(-radius, radius)
                    pygame.draw.circle(screen, (0, 255, 255), (int(quantum_x), int(quantum_y)), 4)
                    
    def draw_cosmic_realm(self, screen, realm):
        """Draw INSANE cosmic realm!"""
        x = realm["x"] * 40 - self.camera_x
        y = realm["y"] * 40 - self.camera_y
        radius = realm["radius"] * 40
        
        if -radius < x < SCREEN_WIDTH + radius and -radius < y < SCREEN_HEIGHT + radius:
            # Cosmic realm effect
            time = pygame.time.get_ticks() * 0.001
            for i in range(12):
                angle = time + i * math.pi / 6
                cosmic_x = x + math.cos(angle) * radius
                cosmic_y = y + math.sin(angle) * radius
                pygame.draw.circle(screen, (200, 0, 200), (int(cosmic_x), int(cosmic_y)), 15, 3)
                
            # Center cosmic core
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 20)
            pygame.draw.circle(screen, (200, 0, 200), (int(x), int(y)), 20, 5)
            
            # Cosmic particles
            if realm["active"]:
                for _ in range(15):
                    cosmic_x = x + random.randint(-radius, radius)
                    cosmic_y = y + random.randint(-radius, radius)
                    pygame.draw.circle(screen, (255, 255, 255), (int(cosmic_x), int(cosmic_y)), 3)
                    
    def draw_world(self, screen):
        """Draw the ultimate world with all features"""
        # Draw blocks with biome colors
        for x in range(self.world_width):
            for y in range(self.world_height):
                if self.blocks[x][y] > 0:
                    draw_x = x * 40 - self.camera_x
                    draw_y = y * 40 - self.camera_y
                    
                    if -40 < draw_x < SCREEN_WIDTH + 40 and -40 < draw_y < SCREEN_HEIGHT + 40:
                        block_type = self.blocks[x][y]
                        biome = self.biomes[x][y]
                        
                        # Get block color based on type and biome
                        color = self.get_block_color(block_type, biome)
                        
                        # Draw block
                        pygame.draw.rect(screen, color, (draw_x, draw_y, 40, 40))
                        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, 40, 40), 1)
                        
                        # Draw special features
                        if block_type == TerrainType.LAVA:
                            # Animated lava
                            lava_glow = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 50
                            pygame.draw.rect(screen, (255, int(100 + lava_glow), 0), (draw_x, draw_y, 40, 40))
                        elif block_type >= 14:  # Ore blocks
                            # Ore sparkles
                            if random.randint(1, 30) == 1:
                                pygame.draw.circle(screen, WHITE, (draw_x + 20, draw_y + 20), 2)
                                
        # Draw structures
        for structure in self.structures:
            self.draw_structure(screen, structure)
            
        # Draw FUN VILLAGES!
        for village in self.villages:
            village.draw(screen, self.camera_x, self.camera_y)
            
        # Draw RUBY HILLS!
        for ruby_hill in self.ruby_hills:
            ruby_hill.draw(screen, self.camera_x, self.camera_y)
            
        # Draw BITCOIN MINES!
        for bitcoin_mine in self.bitcoin_mines:
            bitcoin_mine.draw(screen, self.camera_x, self.camera_y)
            
        # 🌈 Draw INSANE RAINBOW BRIDGES!
        for bridge in self.rainbow_bridges:
            self.draw_rainbow_bridge(screen, bridge)
            
        # ⚛️ Draw INSANE QUANTUM PORTALS!
        for portal in self.quantum_portals:
            self.draw_quantum_portal(screen, portal)
            
        # 🔭 Draw INSANE COSMIC OBSERVATORIES!
        for observatory in self.cosmic_observatories:
            self.draw_cosmic_observatory(screen, observatory)
            
        # ⏰ Draw INSANE TIME TEMPLES!
        for temple in self.time_temples:
            self.draw_time_temple(screen, temple)
            
        # 👻 Draw INSANE SOUL ALTARS!
        for altar in self.soul_altars:
            self.draw_soul_altar(screen, altar)
            
        # 🌟 Draw INSANE STAR GATES!
        for gate in self.star_gates:
            self.draw_star_gate(screen, gate)
            
        # 🕳️ Draw INSANE VOID ANCHORS!
        for anchor in self.void_anchors:
            self.draw_void_anchor(screen, anchor)
            
        # ♾️ Draw INSANE INFINITY FORGES!
        for forge in self.infinity_forges:
            self.draw_infinity_forge(screen, forge)
            
        # 🩸 Draw INSANE BLOOD ALTARS!
        for altar in self.blood_altars:
            self.draw_blood_altar(screen, altar)
            
        # 🌪️ Draw INSANE ELEMENTAL SHRINES!
        for shrine in self.elemental_shrines:
            self.draw_elemental_shrine(screen, shrine)
            
        # 🌀 Draw INSANE DIMENSIONAL RIFTS!
        for rift in self.dimensional_rifts:
            self.draw_dimensional_rift(screen, rift)
            
        # 🐉 Draw INSANE DRAGON LAIRS!
        for lair in self.dragon_lairs:
            self.draw_dragon_lair(screen, lair)
            
        # ₿ Draw INSANE BITCOIN EXCHANGES!
        for exchange in self.bitcoin_exchanges:
            self.draw_bitcoin_exchange(screen, exchange)
            
        # 🌈 Draw INSANE RAINBOW VALLEYS!
        for valley in self.rainbow_valleys:
            self.draw_rainbow_valley(screen, valley)
            
        # ⏰ Draw INSANE TIME DISTORTED AREAS!
        for area in self.time_distorted_areas:
            self.draw_time_distorted_area(screen, area)
            
        # ⚛️ Draw INSANE QUANTUM FIELDS!
        for field in self.quantum_fields:
            self.draw_quantum_field(screen, field)
            
        # 🌌 Draw INSANE COSMIC REALMS!
        for realm in self.cosmic_realms:
            self.draw_cosmic_realm(screen, realm)
            
        # Draw treasure chests
        for chest in self.treasure_chests:
            if not chest["opened"]:
                draw_x = chest["x"] * 40 - self.camera_x
                draw_y = chest["y"] * 40 - self.camera_y
                
                if -40 < draw_x < SCREEN_WIDTH + 40 and -40 < draw_y < SCREEN_HEIGHT + 40:
                    # Chest color based on rarity
                    rarity_colors = {
                        "common": (139, 69, 19),
                        "uncommon": (0, 128, 0),
                        "rare": (0, 0, 139),
                        "epic": (128, 0, 128),
                        "legendary": (255, 215, 0)
                    }
                    color = rarity_colors.get(chest["rarity"], (139, 69, 19))
                    
                    pygame.draw.rect(screen, color, (draw_x, draw_y, 40, 40))
                    pygame.draw.rect(screen, BLACK, (draw_x, draw_y, 40, 40), 2)
                    
                    # Chest lock
                    pygame.draw.circle(screen, YELLOW, (draw_x + 20, draw_y + 20), 5)
                    
    def get_block_color(self, block_type, biome):
        """Get block color based on type and biome"""
        # Base colors for terrain types
        terrain_colors = {
            TerrainType.GRASS: (34, 139, 34),
            TerrainType.DIRT: (139, 69, 19),
            TerrainType.STONE: (128, 128, 128),
            TerrainType.SAND: (238, 203, 173),
            TerrainType.SNOW: (255, 250, 250),
            TerrainType.LAVA: (255, 69, 0),
            TerrainType.ICE: (176, 224, 230),
            TerrainType.CRYSTAL: (255, 255, 255),
            TerrainType.OBSIDIAN: (47, 47, 47),
            TerrainType.BEDROCK: (64, 64, 64),
            TerrainType.MOUNTAIN_STONE: (105, 105, 105),
            TerrainType.VOLCANIC_ROCK: (139, 90, 43),
            TerrainType.MYSTICAL_ORE: (148, 0, 211)
        }
        
        # Ore colors
        ore_colors = {
            14: (220, 20, 60),    # Ruby ore
            15: (0, 100, 0),      # Emerald ore
            16: (185, 242, 255),  # Diamond ore
            17: (255, 255, 255),  # Crystal ore
            18: (255, 140, 0),    # Dragon ore
            19: (0, 255, 255)     # Quantum ore
        }
        
        # Biome modifications
        biome_modifiers = {
            BiomeType.DESERT: lambda c: (min(255, c[0] + 30), max(0, c[1] - 20), max(0, c[2] - 30)),
            BiomeType.SNOW: lambda c: (min(255, c[0] + 40), min(255, c[1] + 40), min(255, c[2] + 60)),
            BiomeType.SWAMP: lambda c: (max(0, c[0] - 20), min(255, c[1] + 30), max(0, c[2] - 10)),
            BiomeType.VOLCANIC: lambda c: (min(255, c[0] + 50), max(0, c[1] - 30), max(0, c[2] - 30))
        }
        
        # Get base color
        if block_type in ore_colors:
            color = ore_colors[block_type]
        else:
            color = terrain_colors.get(block_type, (128, 128, 128))
            
        # Apply biome modification
        if biome in biome_modifiers:
            color = biome_modifiers[biome](color)
            
        return color
        
    def draw_structure(self, screen, structure):
        """Draw world structures"""
        draw_x = structure["x"] * 40 - self.camera_x
        draw_y = structure["y"] * 40 - self.camera_y
        
        if -160 < draw_x < SCREEN_WIDTH + 160 and -160 < draw_y < SCREEN_HEIGHT + 160:
            struct_type = structure["type"]
            width = structure["width"] * 40
            height = structure["height"] * 40
            
            if struct_type == StructureType.HOUSE:
                # House walls
                pygame.draw.rect(screen, (139, 90, 43), (draw_x, draw_y, width, height))
                pygame.draw.rect(screen, BLACK, (draw_x, draw_y, width, height), 2)
                
                # Roof
                pygame.draw.polygon(screen, (178, 34, 34), [
                    (draw_x - 10, draw_y),
                    (draw_x + width // 2, draw_y - 20),
                    (draw_x + width + 10, draw_y)
                ])
                
                # Door
                pygame.draw.rect(screen, (101, 67, 33), (draw_x + width // 2 - 10, draw_y + height - 30, 20, 30))
                
            elif struct_type == StructureType.SHOP:
                # Shop walls
                pygame.draw.rect(screen, (255, 215, 0), (draw_x, draw_y, width, height))
                pygame.draw.rect(screen, BLACK, (draw_x, draw_y, width, height), 2)
                
                # Shop sign
                pygame.draw.rect(screen, WHITE, (draw_x + width // 2 - 20, draw_y - 10, 40, 15))
                font = pygame.font.Font(None, 12)
                text = font.render("SHOP", True, BLACK)
                screen.blit(text, (draw_x + width // 2 - 15, draw_y - 8))
                
            elif struct_type == StructureType.TEMPLE:
                # Temple walls
                pygame.draw.rect(screen, (218, 165, 32), (draw_x, draw_y, width, height))
                pygame.draw.rect(screen, BLACK, (draw_x, draw_y, width, height), 3)
                
                # Pillars
                for i in range(2):
                    pillar_x = draw_x + 10 + i * (width - 20)
                    pygame.draw.rect(screen, (184, 134, 11), (pillar_x, draw_y, 8, height))
                    
            elif struct_type == StructureType.MOUNTAIN_PEAK:
                # Mountain peak flag
                pygame.draw.line(screen, BLACK, (draw_x + 20, draw_y), (draw_x + 20, draw_y - 30), 2)
                pygame.draw.rect(screen, RED, (draw_x + 20, draw_y - 30, 15, 10))
                
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
        # VIBRANT SHOP BACKGROUND!
        self.screen.fill((20, 20, 40))  # Dark blue background
        
        # Animated rainbow border
        border_time = pygame.time.get_ticks() // 100
        border_colors = RAINBOW_COLORS[border_time % len(RAINBOW_COLORS)]
        pygame.draw.rect(self.screen, border_colors, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)
        
        # Sparkle effects
        for _ in range(20):
            sparkle_x = random.randint(0, SCREEN_WIDTH)
            sparkle_y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (sparkle_x, sparkle_y), 1)
        
        # EPIC TITLE with rainbow effect!
        title_text = self.font_large.render("🌟 MEGA FUN SHOP 🌟", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        
        # Rainbow glow behind title
        for i in range(5):
            glow_color = RAINBOW_COLORS[(border_time + i) % len(RAINBOW_COLORS)]
            glow_rect = title_rect.inflate(i * 10, i * 5)
            pygame.draw.rect(self.screen, glow_color, glow_rect, 2)
        
        self.screen.blit(title_text, title_rect)
        
        # FUN stats display with colors!
        stats_bg = pygame.Rect(40, 70, 300, 90)
        pygame.draw.rect(self.screen, (50, 50, 100), stats_bg)
        pygame.draw.rect(self.screen, GOLD, stats_bg, 3)
        
        level_text = self.font_medium.render(f"⭐ LEVEL {self.level} ⭐", True, YELLOW)
        self.screen.blit(level_text, (50, 80))
        
        wealth_text = self.font_medium.render(f"💰 WEALTH: ${self.wealth:,} 💰", True, GOLD)
        self.screen.blit(wealth_text, (50, 105))
        
        exp_text = self.font_small.render(f"📈 EXP: {self.experience}/{self.exp_to_next_level}", True, LIME)
        self.screen.blit(exp_text, (50, 130))
        
        # FUN TAB BUTTONS!
        tools_tab = pygame.Rect(50, 180, 150, 50)
        weapons_tab = pygame.Rect(210, 180, 150, 50)
        items_tab = pygame.Rect(370, 180, 150, 50)
        bitcoin_tab = pygame.Rect(530, 180, 150, 50)  # NEW BITCOIN TAB!
        
        # Rainbow tab colors
        tab_colors = [RAINBOW_COLORS[0], RAINBOW_COLORS[3], RAINBOW_COLORS[6], BITCOIN_ORANGE]
        tabs = [tools_tab, weapons_tab, items_tab, bitcoin_tab]
        tab_names = ["TOOLS", "WEAPONS", "ITEMS", "₿ BITCOIN ₿"]
        
        for i, (tab, name, color) in enumerate(zip(tabs, tab_names, tab_colors)):
            # Gradient effect
            pygame.draw.rect(self.screen, color, tab)
            pygame.draw.rect(self.screen, WHITE, tab, 3)
            
            # Tab text
            text_color = WHITE if name != "₿ BITCOIN ₿" else BLACK
            tab_text = self.font_medium.render(name, True, text_color)
            text_rect = tab_text.get_rect(center=tab.center)
            self.screen.blit(tab_text, text_rect)
        
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
        
    # 🎮 EPIC NEW METHODS - LEGENDARY FEATURES!
    
    def unlock_achievement(self, achievement_type):
        """Unlock an achievement with rewards!"""
        if not self.achievements[achievement_type]:
            self.achievements[achievement_type] = True
            self.achievement_points += 100
            
            # Give rewards based on achievement
            rewards = {
                AchievementType.FIRST_RUBY: (500, "First Ruby! 🎉"),
                AchievementType.RICH_MINER: (5000, "Rich Miner! 💰"),
                AchievementType.BOSS_HUNTER: (10000, "Boss Hunter! 🐉"),
                AchievementType.EXPLORER: (3000, "Explorer! 🗺️"),
                AchievementType.SPEED_MINER: (2000, "Speed Miner! ⚡"),
                AchievementType.LUCKY_FIND: (7777, "Lucky Find! 🍀"),
                AchievementType.MEGA_WEALTH: (50000, "MEGA WEALTH! 🏆"),
                AchievementType.DRAGON_SLAYER: (25000, "Dragon Slayer! 🔥"),
                AchievementType.BITCOIN_MINER: (100000, "Bitcoin Miner! ₿"),
                AchievementType.LEGENDARY_STATUS: (1000000, "LEGENDARY STATUS! 👑")
            }
            
            if achievement_type in rewards:
                wealth_bonus, message = rewards[achievement_type]
                self.wealth += wealth_bonus
                self.create_celebration(message)
                
                # Unlock new features
                if achievement_type == AchievementType.RICH_MINER:
                    self.minigame_unlocked[MiniGameType.LUCKY_SLOTS] = True
                elif achievement_type == AchievementType.BOSS_HUNTER:
                    self.minigame_unlocked[MiniGameType.BOSS_BATTLE] = True
                elif achievement_type == AchievementType.EXPLORER:
                    self.minigame_unlocked[MiniGameType.TREASURE_HUNT] = True
                elif achievement_type == AchievementType.MEGA_WEALTH:
                    self.space_unlocked = True
                elif achievement_type == AchievementType.LEGENDARY_STATUS:
                    self.infinity_mode = True
                    self.infinity_timer = 1000
    
    def create_celebration(self, message):
        """Create amazing celebration effects!"""
        self.celebration_timer = 180  # 3 seconds at 60 FPS
        self.screen_shake = 20
        
        # Create rainbow particles
        for _ in range(50):
            particle = Particle(
                self.player_x + self.player_width // 2,
                self.player_y + self.player_height // 2,
                random.uniform(-10, 10),
                random.uniform(-15, -5),
                random.choice(RAINBOW_COLORS),
                random.randint(3, 8),
                random.randint(60, 120)
            )
            self.particle_effects.append(particle)
    
    def update_legendary_powers(self):
        """Update all legendary power modes!"""
        # Rainbow Mode - Colorful mining with bonus wealth
        if self.rainbow_mode:
            self.rainbow_timer -= 1
            self.mining_multiplier = 3.0
            if self.rainbow_timer <= 0:
                self.rainbow_mode = False
                self.mining_multiplier = 1.0
        
        # Quantum Mode - Super fast mining with quantum effects
        if self.quantum_mode:
            self.quantum_timer -= 1
            self.mining_speed = 10
            self.pickaxe_power = 10
            if self.quantum_timer <= 0:
                self.quantum_mode = False
                self.mining_speed = 1
                self.pickaxe_power = 1
        
        # Infinity Mode - Ultimate power!
        if self.infinity_mode:
            self.infinity_timer -= 1
            self.mining_multiplier = 10.0
            self.mining_speed = 20
            self.pickaxe_power = 20
            if self.infinity_timer <= 0:
                self.infinity_mode = False
                self.mining_multiplier = 1.0
                self.mining_speed = 1
                self.pickaxe_power = 1
        
        # Dragon Mode - Fire breathing mining!
        if self.dragon_mode:
            self.dragon_timer -= 1
            self.mining_multiplier = 5.0
            # Create fire particles
            if random.random() < 0.3:
                particle = Particle(
                    self.player_x + self.player_width // 2,
                    self.player_y + self.player_height // 2,
                    random.uniform(-5, 5),
                    random.uniform(-8, -2),
                    random.choice([RED, ORANGE, YELLOW]),
                    random.randint(4, 10),
                    random.randint(30, 60)
                )
                self.particle_effects.append(particle)
            
            if self.dragon_timer <= 0:
                self.dragon_mode = False
                self.mining_multiplier = 1.0
    
    def start_minigame(self, minigame_type):
        """Start an epic mini-game!"""
        if not self.minigame_unlocked[minigame_type]:
            return False
        
        self.current_minigame = minigame_type
        self.minigame_timer = 600  # 10 seconds
        
        # Set up minigame-specific variables
        if minigame_type == MiniGameType.RUBY_RUSH:
            self.minigame_target = 20  # Mine 20 rubies
            self.minigame_progress = 0
        elif minigame_type == MiniGameType.LUCKY_SLOTS:
            self.minigame_credits = 10
            self.minigame_winnings = 0
        elif minigame_type == MiniGameType.BOSS_BATTLE:
            self.minigame_boss_health = 100
            self.minigame_player_health = 100
        
        return True
    
    def update_minigame(self):
        """Update current mini-game"""
        if self.current_minigame is None:
            return
        
        self.minigame_timer -= 1
        
        if self.minigame_timer <= 0:
            # Minigame ended - calculate rewards
            self.complete_minigame()
            return
        
        # Update specific minigame logic
        if self.current_minigame == MiniGameType.RUBY_RUSH:
            # Already handled in mining logic
            pass
        elif self.current_minigame == MiniGameType.LUCKY_SLOTS:
            # Auto-play slots
            if self.minigame_timer % 60 == 0 and self.minigame_credits > 0:
                self.minigame_credits -= 1
                if random.random() < 0.3:  # 30% win chance
                    winnings = random.randint(100, 1000)
                    self.minigame_winnings += winnings
                    self.wealth += winnings
    
    def complete_minigame(self):
        """Complete mini-game and give rewards"""
        if self.current_minigame == MiniGameType.RUBY_RUSH:
            if self.minigame_progress >= self.minigame_target:
                reward = 5000
                self.wealth += reward
                self.create_celebration("Ruby Rush Complete! 💎")
        elif self.current_minigame == MiniGameType.LUCKY_SLOTS:
            if self.minigame_winnings > 0:
                self.create_celebration(f"Lucky Slots! Won ${self.minigame_winnings}! 🍀")
        elif self.current_minigame == MiniGameType.BOSS_BATTLE:
            if self.minigame_boss_health <= 0:
                reward = 10000
                self.wealth += reward
                self.total_bosses_defeated += 1
                self.create_celebration("Boss Defeated! 🐉")
        
        self.current_minigame = None
    
    def upgrade_castle(self, upgrade_type):
        """Upgrade castle with amazing benefits!"""
        cost = (self.castle_upgrades[upgrade_type] + 1) * 5000
        
        if self.wealth >= cost:
            self.wealth -= cost
            self.castle_upgrades[upgrade_type] += 1
            
            # Apply upgrade benefits
            if upgrade_type == CastleUpgrade.TREASURY:
                self.castle_wealth_bonus += 0.5
            elif upgrade_type == CastleUpgrade.WORKSHOP:
                self.mining_speed += 1
            elif upgrade_type == CastleUpgrade.OBSERVATORY:
                self.space_unlocked = True
            
            return True
        return False
    
    def explore_space(self, feature_type):
        """Explore space features for cosmic rewards!"""
        if not self.space_unlocked:
            return False
        
        if self.space_features[feature_type]:
            return True  # Already unlocked
        
        costs = {
            SpaceFeature.ROCKET: 50000,
            SpaceFeature.MOON_BASE: 100000,
            SpaceFeature.SPACE_STATION: 250000,
            SpaceFeature.ASTEROID_MINE: 500000,
            SpaceFeature.ALIEN_TRADING: 750000,
            SpaceFeature.BLACK_HOLE: 1000000,
            SpaceFeature.NEBULA: 1500000,
            SpaceFeature.COSMIC_PORTAL: 2000000
        }
        
        cost = costs.get(feature_type, 100000)
        
        if self.wealth >= cost:
            self.wealth -= cost
            self.space_features[feature_type] = True
            
            # Give space rewards
            if feature_type == SpaceFeature.ASTEROID_MINE:
                self.space_wealth += 1000  # Passive income
            elif feature_type == SpaceFeature.ALIEN_TRADING:
                self.alien_reputation += 100
            elif feature_type == SpaceFeature.COSMIC_PORTAL:
                self.quantum_mode = True
                self.quantum_timer = 500
            
            return True
        return False
    
    def change_character_skin(self, skin_type):
        """Change character appearance with cool skins!"""
        if self.unlocked_skins.get(skin_type, False):
            self.current_skin = skin_type
            return True
        return False
    
    def unlock_skin(self, skin_type):
        """Unlock new character skins!"""
        costs = {
            CharacterSkin.NINJA: 10000,
            CharacterSkin.ROBOT: 25000,
            CharacterSkin.WIZARD: 50000,
            CharacterSkin.DRAGON: 100000,
            CharacterSkin.ASTRONAUT: 75000,
            CharacterSkin.PIRATE: 30000,
            CharacterSkin.SUPERHERO: 200000
        }
        
        cost = costs.get(skin_type, 50000)
        
        if self.wealth >= cost and not self.unlocked_skins.get(skin_type, False):
            self.wealth -= cost
            self.unlocked_skins[skin_type] = True
            self.create_celebration(f"New Skin Unlocked! {skin_type.name} 🎨")
            return True
        return False
    
    def update_visual_effects(self):
        """Update all amazing visual effects!"""
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # Update celebration timer
        if self.celebration_timer > 0:
            self.celebration_timer -= 1
            # Create celebration particles
            if self.celebration_timer % 5 == 0:
                particle = Particle(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                    random.uniform(-2, 2),
                    random.uniform(-5, -1),
                    random.choice(RAINBOW_COLORS),
                    random.randint(2, 6),
                    random.randint(30, 60)
                )
                self.particle_effects.append(particle)
        
        # Update particles
        for particle in self.particle_effects[:]:
            particle.update()
            if particle.life <= 0:
                self.particle_effects.remove(particle)
        
        # Update rainbow particles in rainbow mode
        if self.rainbow_mode:
            if random.random() < 0.5:
                particle = Particle(
                    self.player_x + random.randint(-20, 20),
                    self.player_y + random.randint(-20, 20),
                    random.uniform(-3, 3),
                    random.uniform(-5, -1),
                    random.choice(RAINBOW_COLORS),
                    random.randint(3, 8),
                    random.randint(40, 80)
                )
                self.rainbow_particles.append(particle)
        
        # Update rainbow particles
        for particle in self.rainbow_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.rainbow_particles.remove(particle)
        
        # Update cosmic particles in space
        if self.space_unlocked:
            if random.random() < 0.1:
                particle = Particle(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                    random.uniform(-1, 1),
                    random.uniform(-2, 0),
                    random.choice([PURPLE, CYAN, WHITE]),
                    random.randint(1, 4),
                    random.randint(60, 120)
                )
                self.cosmic_particles.append(particle)
        
        # Update cosmic particles
        for particle in self.cosmic_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.cosmic_particles.remove(particle)
    
    def apply_screen_shake(self, surface):
        """Apply screen shake effect for epic moments!"""
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
            
            # Create a temporary surface with shake
            temp_surface = surface.copy()
            surface.fill(BLACK)
            surface.blit(temp_surface, (shake_x, shake_y))
    
    def check_achievements(self):
        """Check and unlock achievements based on player progress!"""
        # First Ruby
        if self.rubies >= 1 and not self.achievements[AchievementType.FIRST_RUBY]:
            self.unlock_achievement(AchievementType.FIRST_RUBY)
        
        # Rich Miner
        if self.wealth >= 10000 and not self.achievements[AchievementType.RICH_MINER]:
            self.unlock_achievement(AchievementType.RICH_MINER)
        
        # Boss Hunter
        if self.total_bosses_defeated >= 5 and not self.achievements[AchievementType.BOSS_HUNTER]:
            self.unlock_achievement(AchievementType.BOSS_HUNTER)
        
        # Explorer
        if len(self.discovered_areas) >= 20 and not self.achievements[AchievementType.EXPLORER]:
            self.unlock_achievement(AchievementType.EXPLORER)
        
        # Speed Miner
        if self.mining_combo >= 50 and not self.achievements[AchievementType.SPEED_MINER]:
            self.unlock_achievement(AchievementType.SPEED_MINER)
        
        # Lucky Find
        if self.total_rubies_mined >= 100 and not self.achievements[AchievementType.LUCKY_FIND]:
            self.unlock_achievement(AchievementType.LUCKY_FIND)
        
        # Mega Wealth
        if self.wealth >= 100000 and not self.achievements[AchievementType.MEGA_WEALTH]:
            self.unlock_achievement(AchievementType.MEGA_WEALTH)
        
        # Dragon Slayer
        if self.total_bosses_defeated >= 20 and not self.achievements[AchievementType.DRAGON_SLAYER]:
            self.unlock_achievement(AchievementType.DRAGON_SLAYER)
        
        # Bitcoin Miner
        if self.total_rubies_mined >= 500 and not self.achievements[AchievementType.BITCOIN_MINER]:
            self.unlock_achievement(AchievementType.BITCOIN_MINER)
        
        # Legendary Status
        if self.wealth >= 1000000 and not self.achievements[AchievementType.LEGENDARY_STATUS]:
            self.unlock_achievement(AchievementType.LEGENDARY_STATUS)
    
    def update_castle_production(self):
        """Update castle wealth production!"""
        # Treasury generates passive wealth
        if self.castle_upgrades[CastleUpgrade.TREASURY] > 0:
            production_rate = self.castle_upgrades[CastleUpgrade.TREASURY] * 10
            self.wealth += production_rate * self.castle_wealth_bonus
        
        # Workshop can produce random items
        if self.castle_upgrades[CastleUpgrade.WORKSHOP] > 0:
            if random.random() < 0.01 * self.castle_upgrades[CastleUpgrade.WORKSHOP]:
                # Random bonus wealth
                bonus = random.randint(100, 1000) * self.castle_upgrades[CastleUpgrade.WORKSHOP]
                self.wealth += bonus
    
    def update_space_features(self):
        """Update space exploration features!"""
        if not self.space_unlocked:
            return
        
        # Asteroid mine generates space wealth
        if self.space_features[SpaceFeature.ASTEROID_MINE]:
            self.space_wealth += 50  # Passive space income
            self.wealth += self.space_wealth // 100  # Convert some to regular wealth
        
        # Alien trading can give random bonuses
        if self.space_features[SpaceFeature.ALIEN_TRADING]:
            if random.random() < 0.005 * (self.alien_reputation // 100):
                alien_bonus = random.randint(1000, 10000)
                self.wealth += alien_bonus
                self.alien_reputation += 10
                self.create_celebration("Alien Trade Bonus! 👽")
        
        # Black hole can give massive random rewards
        if self.space_features[SpaceFeature.BLACK_HOLE]:
            if random.random() < 0.001:  # Very rare
                black_hole_bonus = random.randint(50000, 500000)
                self.wealth += black_hole_bonus
                self.create_celebration("BLACK HOLE BONUS! 🌌")
                self.screen_shake = 30
    
    def mine_block_with_effects(self, x, y):
        """Mine block with epic visual effects and achievements!"""
        # Original mining logic
        world_x = (x + self.camera_x) // 40
        world_y = (y + self.camera_y) // 40
        
        if 0 <= world_x < self.world_width and 0 <= world_y < self.world_height:
            if self.blocks[world_x][world_y] > 0:
                block_type = self.blocks[world_x][world_y]
                
                # Check for gems
                for gem in self.gems[:]:
                    if not gem.collected:
                        gem_rect = pygame.Rect(gem.x - 10, gem.y - 10, 20, 20)
                        mouse_rect = pygame.Rect(x, y, 1, 1)
                        if gem_rect.collidepoint(mouse_rect):
                            gem.collected = True
                            props = gem.properties[gem.type]
                            
                            # Apply mining multiplier
                            final_value = int(props["value"] * self.mining_multiplier * self.castle_wealth_bonus)
                            self.wealth += final_value
                            self.total_earned += final_value
                            self.experience += props["rarity"] * 10
                            
                            # Track specific gems
                            if gem.type == GemType.RUBY:
                                self.rubies += 1
                                self.total_rubies_mined += 1
                            elif gem.type == GemType.EMERALD:
                                self.emeralds += 1
                            elif gem.type == GemType.DIAMOND:
                                self.diamonds += 1
                            elif gem.type == GemType.GOLD:
                                self.gold += 1
                            
                            # 🎮 TRIGGER LEGENDARY POWERS based on gem effects!
                            if props["effect"] == "rainbow":
                                self.rainbow_mode = True
                                self.rainbow_timer = 300
                                self.create_celebration("RAINBOW MODE ACTIVATED! 🌈")
                            elif props["effect"] == "quantum":
                                self.quantum_mode = True
                                self.quantum_timer = 400
                                self.create_celebration("QUANTUM MODE ACTIVATED! ⚛️")
                            elif props["effect"] == "infinity":
                                self.infinity_mode = True
                                self.infinity_timer = 600
                                self.create_celebration("INFINITY MODE ACTIVATED! ♾️")
                            elif props["effect"] == "fire":
                                self.dragon_mode = True
                                self.dragon_timer = 500
                                self.create_celebration("DRAGON MODE ACTIVATED! 🔥")
                            elif props["effect"] == "bitcoin":
                                self.create_celebration("BITCOIN FOUND! ₿💰")
                                self.screen_shake = 25
                            
                            # Create mining particles
                            for _ in range(10):
                                particle = Particle(
                                    gem.x, gem.y,
                                    random.uniform(-5, 5),
                                    random.uniform(-8, -2),
                                    props["color"],
                                    random.randint(3, 8),
                                    random.randint(30, 60)
                                )
                                self.particle_effects.append(particle)
                            
                            # 🎯 UPDATE MINIGAME PROGRESS
                            if self.current_minigame == MiniGameType.RUBY_RUSH and gem.type == GemType.RUBY:
                                self.minigame_progress += 1
                            
                            # Check level up
                            if self.experience >= self.exp_to_next_level:
                                self.level_up()
                            
                            self.gems.remove(gem)
                            return True
                
                # Mine regular block
                self.blocks[world_x][world_y] = 0
                self.experience += 1
                
                # Create block particles
                for _ in range(5):
                    particle = Particle(
                        world_x * 40 + 20,
                        world_y * 40 + 20,
                        random.uniform(-3, 3),
                        random.uniform(-6, -1),
                        GRAY,
                        random.randint(2, 5),
                        random.randint(20, 40)
                    )
                    self.particle_effects.append(particle)
                
                return True
        
        return False
    
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
