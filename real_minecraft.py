#!/usr/bin/env python3
"""
REAL Minecraft Game - Not Trash Version
Actually like Minecraft with 3D graphics, crafting, survival, and proper mechanics
"""

import pygame
import random
import math
import noise
from enum import Enum
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Real Minecraft Colors
class BlockType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4
    LEAVES = 5
    SAND = 6
    WATER = 7
    COAL = 8
    IRON = 9
    GOLD = 10
    DIAMOND = 11
    CRAFTING_TABLE = 12
    FURNACE = 13
    PLANKS = 14
    STICKS = 15
    TORCH = 16
    COBBLESTONE = 17
    BEDROCK = 18
    LOG = 19

# Weapon types
class WeaponType(Enum):
    FIST = 0
    WOODEN_SWORD = 1
    STONE_SWORD = 2
    IRON_SWORD = 3
    GOLDEN_SWORD = 4
    DIAMOND_SWORD = 5
    BOW = 6

# Animal types
class AnimalType(Enum):
    COW = 0
    PIG = 1
    CHICKEN = 2
    SHEEP = 3
    RABBIT = 4
    RALPH_FOX = 5
    FRANK_FOX = 6

# Food types
class FoodType(Enum):
    BEEF = 0
    PORK = 1
    CHICKEN_MEAT = 2
    MUTTON = 3
    RABBIT_MEAT = 4
    FOX_MEAT = 5

# Realistic block colors with shading
BLOCK_COLORS = {
    BlockType.AIR: (0, 0, 0, 0),
    BlockType.GRASS: (124, 169, 69),
    BlockType.DIRT: (139, 90, 43),
    BlockType.STONE: (136, 140, 141),
    BlockType.WOOD: (101, 67, 33),
    BlockType.LEAVES: (34, 139, 34),
    BlockType.SAND: (238, 203, 173),
    BlockType.WATER: (64, 164, 223),
    BlockType.COAL: (54, 54, 54),
    BlockType.IRON: (192, 192, 192),
    BlockType.GOLD: (255, 215, 0),
    BlockType.DIAMOND: (185, 242, 255),
    BlockType.CRAFTING_TABLE: (139, 90, 43),
    BlockType.FURNACE: (105, 105, 105),
    BlockType.PLANKS: (160, 82, 45),
    BlockType.STICKS: (101, 67, 33),
    BlockType.TORCH: (255, 255, 100),
    BlockType.COBBLESTONE: (128, 128, 128),
    BlockType.BEDROCK: (64, 64, 64),
    BlockType.LOG: (101, 67, 33)
}

# Weapon stats (damage, durability)
WEAPON_STATS = {
    WeaponType.FIST: {"damage": 1, "durability": -1, "color": (139, 69, 19)},
    WeaponType.WOODEN_SWORD: {"damage": 4, "durability": 60, "color": (101, 67, 33)},
    WeaponType.STONE_SWORD: {"damage": 5, "durability": 132, "color": (136, 140, 141)},
    WeaponType.IRON_SWORD: {"damage": 6, "durability": 251, "color": (192, 192, 192)},
    WeaponType.GOLDEN_SWORD: {"damage": 4, "durability": 33, "color": (255, 215, 0)},
    WeaponType.DIAMOND_SWORD: {"damage": 7, "durability": 1562, "color": (185, 242, 255)},
    WeaponType.BOW: {"damage": 3, "durability": 384, "color": (160, 82, 45)}
}

# Animal properties
ANIMAL_PROPERTIES = {
    AnimalType.COW: {"health": 10, "size": 40, "speed": 0.5, "color": (139, 90, 43), "food": FoodType.BEEF, "food_amount": 3},
    AnimalType.PIG: {"health": 8, "size": 30, "speed": 0.8, "color": (255, 192, 203), "food": FoodType.PORK, "food_amount": 2},
    AnimalType.CHICKEN: {"health": 4, "size": 20, "speed": 1.2, "color": (255, 255, 255), "food": FoodType.CHICKEN_MEAT, "food_amount": 1},
    AnimalType.SHEEP: {"health": 8, "size": 35, "speed": 0.6, "color": (255, 255, 255), "food": FoodType.MUTTON, "food_amount": 2},
    AnimalType.RABBIT: {"health": 3, "size": 15, "speed": 1.5, "color": (192, 192, 192), "food": FoodType.RABBIT_MEAT, "food_amount": 1},
    AnimalType.RALPH_FOX: {"health": 12, "size": 35, "speed": 2.0, "color": (255, 140, 0), "food": FoodType.FOX_MEAT, "food_amount": 2, "name": "Ralph"},
    AnimalType.FRANK_FOX: {"health": 12, "size": 35, "speed": 1.8, "color": (255, 100, 50), "food": FoodType.FOX_MEAT, "food_amount": 2, "name": "Frank"}
}

# Food properties (hunger restored)
FOOD_PROPERTIES = {
    FoodType.BEEF: {"hunger": 8, "color": (139, 69, 43)},
    FoodType.PORK: {"hunger": 8, "color": (255, 192, 203)},
    FoodType.CHICKEN_MEAT: {"hunger": 6, "color": (255, 255, 224)},
    FoodType.MUTTON: {"hunger": 6, "color": (245, 245, 220)},
    FoodType.RABBIT_MEAT: {"hunger": 5, "color": (192, 192, 192)},
    FoodType.FOX_MEAT: {"hunger": 10, "color": (255, 120, 60)}
}

# Crafting recipes
CRAFTING_RECIPES = {
    BlockType.PLANKS: [(BlockType.WOOD, 1)],
    BlockType.STICKS: [(BlockType.PLANKS, 1)],
    BlockType.CRAFTING_TABLE: [(BlockType.PLANKS, 4)],
    BlockType.FURNACE: [(BlockType.COBBLESTONE, 8)],
    BlockType.TORCH: [(BlockType.STICKS, 1), (BlockType.COAL, 1)],
    WeaponType.WOODEN_SWORD: [(BlockType.PLANKS, 2), (BlockType.STICKS, 1)],
    WeaponType.STONE_SWORD: [(BlockType.COBBLESTONE, 2), (BlockType.STICKS, 1)],
    WeaponType.IRON_SWORD: [(BlockType.IRON, 2), (BlockType.STICKS, 1)],
    WeaponType.GOLDEN_SWORD: [(BlockType.GOLD, 2), (BlockType.STICKS, 1)],
    WeaponType.DIAMOND_SWORD: [(BlockType.DIAMOND, 2), (BlockType.STICKS, 1)],
    WeaponType.BOW: [(BlockType.STICKS, 3), (BlockType.WOOD, 3)]  # Use wood instead of string
}

class Animal:
    def __init__(self, x, y, animal_type):
        self.x = x
        self.y = y
        self.type = animal_type
        self.properties = ANIMAL_PROPERTIES[animal_type]
        self.health = self.properties["health"]
        self.max_health = self.properties["health"]
        self.size = self.properties["size"]
        self.speed = self.properties["speed"]
        self.color = self.properties["color"]
        self.direction = random.uniform(0, 2 * math.pi)
        self.move_timer = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.alive = True
        
    def update(self, world):
        if not self.alive:
            return
            
        self.move_timer += 1
        
        # Random movement
        if self.move_timer > random.randint(30, 90):
            self.direction = random.uniform(0, 2 * math.pi)
            self.move_timer = 0
            
        # Move animal
        new_x = self.x + math.cos(self.direction) * self.speed
        new_y = self.y + math.sin(self.direction) * self.speed
        
        # Check bounds and collisions
        if 0 <= new_x <= world.width * TILE_SIZE - self.size:
            if 0 <= new_y <= world.height * TILE_SIZE - self.size:
                # Check if not in a block
                tile_x = int((new_x + self.size // 2) // TILE_SIZE)
                tile_y = int((new_y + self.size // 2) // TILE_SIZE)
                
                if (0 <= tile_x < world.width and 0 <= tile_y < world.height and 
                    world.blocks[tile_x][tile_y] == BlockType.AIR):
                    self.x = new_x
                    self.y = new_y
                    self.rect.x = self.x
                    self.rect.y = self.y
                else:
                    # Hit something, change direction
                    self.direction = random.uniform(0, 2 * math.pi)
            else:
                self.direction = random.uniform(0, 2 * math.pi)
        else:
            self.direction = random.uniform(0, 2 * math.pi)
            
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True  # Animal died
        return False
        
    def draw(self, screen, camera_x, camera_y):
        if not self.alive:
            return
            
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if self.type == AnimalType.COW:
            # Draw cow body
            body_rect = pygame.Rect(draw_x, draw_y + 10, self.size, self.size - 10)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
            
            # Draw head
            head_rect = pygame.Rect(draw_x - 5, draw_y, 15, 15)
            pygame.draw.rect(screen, self.color, head_rect)
            pygame.draw.rect(screen, BLACK, head_rect, 2)
            
            # Draw legs
            for i in range(4):
                leg_x = draw_x + 5 + i * 8
                pygame.draw.rect(screen, self.color, (leg_x, draw_y + self.size - 5, 4, 10))
                
        elif self.type == AnimalType.PIG:
            # Draw pig body
            body_rect = pygame.Rect(draw_x, draw_y + 5, self.size, self.size - 5)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
            
            # Draw snout
            pygame.draw.circle(screen, (255, 182, 193), (draw_x + 5, draw_y + 10), 4)
            
            # Draw legs
            for i in range(4):
                leg_x = draw_x + 4 + i * 7
                pygame.draw.rect(screen, self.color, (leg_x, draw_y + self.size - 3, 3, 8))
                
        elif self.type == AnimalType.CHICKEN:
            # Draw chicken body
            pygame.draw.circle(screen, self.color, (draw_x + self.size // 2, draw_y + self.size // 2), self.size // 2)
            pygame.draw.circle(screen, BLACK, (draw_x + self.size // 2, draw_y + self.size // 2), self.size // 2, 2)
            
            # Draw beak
            pygame.draw.polygon(screen, (255, 165, 0), 
                              [(draw_x + 5, draw_y + self.size // 2),
                               (draw_x, draw_y + self.size // 2 - 3),
                               (draw_x, draw_y + self.size // 2 + 3)])
                               
        elif self.type == AnimalType.SHEEP:
            # Draw sheep body (woolly)
            body_rect = pygame.Rect(draw_x, draw_y + 8, self.size, self.size - 8)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
            
            # Draw head
            head_rect = pygame.Rect(draw_x - 3, draw_y + 5, 12, 12)
            pygame.draw.rect(screen, (200, 200, 200), head_rect)
            pygame.draw.rect(screen, BLACK, head_rect, 2)
            
            # Draw legs
            for i in range(4):
                leg_x = draw_x + 4 + i * 7
                pygame.draw.rect(screen, BLACK, (leg_x, draw_y + self.size - 4, 3, 8))
                
        elif self.type == AnimalType.RABBIT:
            # Draw rabbit body
            body_rect = pygame.Rect(draw_x, draw_y + 5, self.size - 5, self.size - 5)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
            
            # Draw ears
            pygame.draw.ellipse(screen, self.color, (draw_x + 8, draw_y - 5, 4, 10))
            pygame.draw.ellipse(screen, self.color, (draw_x + 13, draw_y - 5, 4, 10))
            
        elif self.type == AnimalType.RALPH_FOX:
            # Draw Ralph the Fox (orange fox)
            # Body
            body_rect = pygame.Rect(draw_x, draw_y + 8, self.size - 5, self.size - 8)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
            
            # Head
            head_rect = pygame.Rect(draw_x - 3, draw_y + 2, 20, 15)
            pygame.draw.rect(screen, self.color, head_rect)
            pygame.draw.rect(screen, BLACK, head_rect, 2)
            
            # Ears (pointed)
            pygame.draw.polygon(screen, self.color, 
                              [(draw_x + 2, draw_y), 
                               (draw_x, draw_y - 8),
                               (draw_x + 6, draw_y)])
            pygame.draw.polygon(screen, self.color, 
                              [(draw_x + 14, draw_y), 
                               (draw_x + 18, draw_y - 8),
                               (draw_x + 18, draw_y)])
            
            # Tail (bushy)
            pygame.draw.ellipse(screen, self.color, 
                             (draw_x + self.size - 5, draw_y + 15, 12, 8))
            
            # Eyes (green)
            pygame.draw.circle(screen, BLACK, (draw_x + 5, draw_y + 8), 2)
            pygame.draw.circle(screen, BLACK, (draw_x + 15, draw_y + 8), 2)
            
            # Name tag
            font = pygame.font.Font(None, 16)
            name_text = font.render("Ralph", True, WHITE)
            screen.blit(name_text, (draw_x - 5, draw_y - 15))
            
        elif self.type == AnimalType.FRANK_FOX:
            # Draw Frank the Fox (brownish fox)
            # Body
            body_rect = pygame.Rect(draw_x, draw_y + 8, self.size - 5, self.size - 8)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
            
            # Head
            head_rect = pygame.Rect(draw_x - 3, draw_y + 2, 20, 15)
            pygame.draw.rect(screen, self.color, head_rect)
            pygame.draw.rect(screen, BLACK, head_rect, 2)
            
            # Ears (rounded)
            pygame.draw.ellipse(screen, self.color, 
                             (draw_x + 2, draw_y - 2, 6, 8))
            pygame.draw.ellipse(screen, self.color, 
                             (draw_x + 14, draw_y - 2, 6, 8))
            
            # Tail (fluffy)
            pygame.draw.ellipse(screen, self.color, 
                             (draw_x + self.size - 8, draw_y + 18, 15, 6))
            
            # Eyes (blue)
            pygame.draw.circle(screen, BLACK, (draw_x + 5, draw_y + 8), 2)
            pygame.draw.circle(screen, BLACK, (draw_x + 15, draw_y + 8), 2)
            
            # Name tag
            font = pygame.font.Font(None, 16)
            name_text = font.render("Frank", True, WHITE)
            screen.blit(name_text, (draw_x - 5, draw_y - 15))
            
        # Draw health bar if damaged
        if self.health < self.max_health:
            health_rect = pygame.Rect(draw_x, draw_y - 10, self.size, 4)
            pygame.draw.rect(screen, RED, health_rect)
            health_fill = pygame.Rect(draw_x, draw_y - 10, 
                                    int(self.size * self.health / self.max_health), 4)
            pygame.draw.rect(screen, GREEN, health_fill)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
        self.jump_power = 12
        self.gravity = 0.8
        self.max_fall_speed = 15
        
        # Survival mechanics
        self.health = 20
        self.max_health = 20
        self.hunger = 20
        self.max_hunger = 20
        self.armor = 0
        self.oxygen = 20
        
        # Combat system
        self.current_weapon = WeaponType.FIST
        self.weapon_durability = {}
        self.attack_cooldown = 0
        self.attack_damage = WEAPON_STATS[WeaponType.FIST]["damage"]
        
        # Inventory with proper stacking
        self.inventory = defaultdict(int)
        self.food_inventory = defaultdict(int)
        self.weapon_inventory = defaultdict(int)
        self.hotbar = [BlockType.DIRT, BlockType.STONE, BlockType.WOOD, BlockType.GRASS, 
                      BlockType.SAND, BlockType.COAL, BlockType.IRON, BlockType.PLANKS, BlockType.STICKS]
        self.selected_slot = 0
        self.selected_block = self.hotbar[0]
        
        # Give starting items
        self.inventory[BlockType.WOOD] = 64
        self.inventory[BlockType.STONE] = 64
        self.inventory[BlockType.DIRT] = 64
        self.inventory[BlockType.GRASS] = 64
        self.inventory[BlockType.SAND] = 32
        self.inventory[BlockType.COAL] = 16
        self.inventory[BlockType.IRON] = 8
        self.inventory[BlockType.PLANKS] = 32
        self.inventory[BlockType.STICKS] = 16
        
        # Give starting weapons
        self.weapon_inventory[WeaponType.WOODEN_SWORD] = 1
        self.weapon_inventory[WeaponType.STONE_SWORD] = 1
        self.weapon_durability[WeaponType.WOODEN_SWORD] = WEAPON_STATS[WeaponType.WOODEN_SWORD]["durability"]
        self.weapon_durability[WeaponType.STONE_SWORD] = WEAPON_STATS[WeaponType.STONE_SWORD]["durability"]
        
        # Give starting food
        self.food_inventory[FoodType.BEEF] = 5
        self.food_inventory[FoodType.PORK] = 3
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def equip_weapon(self, weapon_type):
        if weapon_type in self.weapon_inventory and self.weapon_inventory[weapon_type] > 0:
            self.current_weapon = weapon_type
            self.attack_damage = WEAPON_STATS[weapon_type]["damage"]
            
    def attack(self, target):
        if self.attack_cooldown <= 0:
            damage = self.attack_damage
            
            # Reduce weapon durability
            if (self.current_weapon != WeaponType.FIST and 
                self.current_weapon in self.weapon_durability):
                self.weapon_durability[self.current_weapon] -= 1
                
                # Check if weapon broke
                if self.weapon_durability[self.current_weapon] <= 0:
                    del self.weapon_inventory[self.current_weapon]
                    del self.weapon_durability[self.current_weapon]
                    self.current_weapon = WeaponType.FIST
                    self.attack_damage = WEAPON_STATS[WeaponType.FIST]["damage"]
                    
            self.attack_cooldown = 20  # 1/3 second at 60 FPS
            return damage
        return 0
        
    def eat_food(self, food_type):
        if food_type in self.food_inventory and self.food_inventory[food_type] > 0:
            if self.hunger < self.max_hunger:
                self.food_inventory[food_type] -= 1
                hunger_restored = FOOD_PROPERTIES[food_type]["hunger"]
                self.hunger = min(self.max_hunger, self.hunger + hunger_restored)
                return True
        return False
        
    def update(self, world, keys):
        # Movement
        target_vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            target_vel_x = -self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            target_vel_x = self.speed
        
        self.vel_x += (target_vel_x - self.vel_x) * 0.9
        
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -self.jump_power
            
        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed
                
        # Move and resolve collisions
        self.rect.x += self.vel_x
        self.resolve_collisions_x(world)
        
        self.rect.y += self.vel_y
        self.on_ground = False
        self.resolve_collisions_y(world)
        
        # Update position
        self.x = self.rect.x
        self.y = self.rect.y
        
        # Keep in bounds
        self.rect.x = max(0, min(self.rect.x, world.width * TILE_SIZE - self.width))
        self.rect.y = max(0, min(self.rect.y, world.height * TILE_SIZE - self.height))
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Update survival stats
        if random.random() < 0.002:  # Hunger decreases over time
            self.hunger = max(0, self.hunger - 1)
            
    def resolve_collisions_x(self, world):
        left_tile = max(0, self.rect.left // TILE_SIZE)
        right_tile = min(world.width - 1, self.rect.right // TILE_SIZE)
        top_tile = max(0, self.rect.top // TILE_SIZE)
        bottom_tile = min(world.height - 1, self.rect.bottom // TILE_SIZE)
        
        for x in range(left_tile, right_tile + 1):
            for y in range(top_tile, bottom_tile + 1):
                if world.blocks[x][y] != BlockType.AIR:
                    block_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if self.rect.colliderect(block_rect):
                        overlap_left = self.rect.right - block_rect.left
                        overlap_right = block_rect.right - self.rect.left
                        
                        if overlap_left < overlap_right:
                            self.rect.right = block_rect.left
                        else:
                            self.rect.left = block_rect.right
                        self.vel_x = 0
                        return
                        
    def resolve_collisions_y(self, world):
        left_tile = max(0, self.rect.left // TILE_SIZE)
        right_tile = min(world.width - 1, self.rect.right // TILE_SIZE)
        top_tile = max(0, self.rect.top // TILE_SIZE)
        bottom_tile = min(world.height - 1, self.rect.bottom // TILE_SIZE)
        
        for x in range(left_tile, right_tile + 1):
            for y in range(top_tile, bottom_tile + 1):
                if world.blocks[x][y] != BlockType.AIR:
                    block_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if self.rect.colliderect(block_rect):
                        overlap_top = self.rect.bottom - block_rect.top
                        overlap_bottom = block_rect.bottom - self.rect.top
                        
                        if overlap_top < overlap_bottom:
                            self.rect.bottom = block_rect.top
                            self.on_ground = True
                        else:
                            self.rect.top = block_rect.bottom
                        self.vel_y = 0
                        return
                        
    def draw_3d(self, screen, camera_x, camera_y):
        # Draw player with 3D effect
        
        # Draw equipped weapon/hand in bottom center
        if self.current_weapon == WeaponType.FIST:
            # Draw hand
            hand_color = (255, 220, 177)  # Skin color
            hand_rect = pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 120, 40, 60)
            pygame.draw.rect(screen, hand_color, hand_rect)
            pygame.draw.rect(screen, BLACK, hand_rect, 2)
            
        elif self.current_weapon == WeaponType.WOODEN_SWORD:
            # Draw wooden sword
            sword_color = WEAPON_STATS[WeaponType.WOODEN_SWORD]["color"]
            # Handle
            handle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 140, 10, 80)
            pygame.draw.rect(screen, (101, 67, 33), handle_rect)  # Brown wood
            pygame.draw.rect(screen, BLACK, handle_rect, 2)
            # Blade
            blade_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 160, 30, 60)
            pygame.draw.rect(screen, sword_color, blade_rect)
            pygame.draw.rect(screen, BLACK, blade_rect, 2)
            
        elif self.current_weapon == WeaponType.STONE_SWORD:
            # Draw stone sword
            sword_color = WEAPON_STATS[WeaponType.STONE_SWORD]["color"]
            # Handle
            handle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 140, 10, 80)
            pygame.draw.rect(screen, (101, 67, 33), handle_rect)  # Wood handle
            pygame.draw.rect(screen, BLACK, handle_rect, 2)
            # Blade
            blade_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 160, 30, 60)
            pygame.draw.rect(screen, sword_color, blade_rect)
            pygame.draw.rect(screen, BLACK, blade_rect, 2)
            
        elif self.current_weapon == WeaponType.IRON_SWORD:
            # Draw iron sword
            sword_color = WEAPON_STATS[WeaponType.IRON_SWORD]["color"]
            # Handle
            handle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 140, 10, 80)
            pygame.draw.rect(screen, (101, 67, 33), handle_rect)  # Wood handle
            pygame.draw.rect(screen, BLACK, handle_rect, 2)
            # Blade
            blade_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 160, 30, 60)
            pygame.draw.rect(screen, sword_color, blade_rect)
            pygame.draw.rect(screen, BLACK, blade_rect, 2)
            
        elif self.current_weapon == WeaponType.GOLDEN_SWORD:
            # Draw golden sword
            sword_color = WEAPON_STATS[WeaponType.GOLDEN_SWORD]["color"]
            # Handle
            handle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 140, 10, 80)
            pygame.draw.rect(screen, (101, 67, 33), handle_rect)  # Wood handle
            pygame.draw.rect(screen, BLACK, handle_rect, 2)
            # Blade
            blade_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 160, 30, 60)
            pygame.draw.rect(screen, sword_color, blade_rect)
            pygame.draw.rect(screen, BLACK, blade_rect, 2)
            
        elif self.current_weapon == WeaponType.DIAMOND_SWORD:
            # Draw diamond sword
            sword_color = WEAPON_STATS[WeaponType.DIAMOND_SWORD]["color"]
            # Handle
            handle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 140, 10, 80)
            pygame.draw.rect(screen, (101, 67, 33), handle_rect)  # Wood handle
            pygame.draw.rect(screen, BLACK, handle_rect, 2)
            # Blade
            blade_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 160, 30, 60)
            pygame.draw.rect(screen, sword_color, blade_rect)
            pygame.draw.rect(screen, BLACK, blade_rect, 2)
            
        elif self.current_weapon == WeaponType.BOW:
            # Draw bow
            bow_color = WEAPON_STATS[WeaponType.BOW]["color"]
            bow_rect = pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 140, 40, 80)
            pygame.draw.rect(screen, bow_color, bow_rect)
            pygame.draw.rect(screen, BLACK, bow_rect, 2)
            # Bowstring
            pygame.draw.line(screen, BLACK, 
                         (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100),
                         (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT - 100), 3)
            
        # Draw crosshair in center (Minecraft style!)
        crosshair_size = 15
        crosshair_color = WHITE
        # Horizontal line
        pygame.draw.line(screen, crosshair_color, 
                     (SCREEN_WIDTH // 2 - crosshair_size, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 + crosshair_size, SCREEN_HEIGHT // 2), 2)
        # Vertical line  
        pygame.draw.line(screen, crosshair_color,
                     (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - crosshair_size),
                     (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + crosshair_size), 2)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blocks = [[BlockType.AIR for _ in range(height)] for _ in range(width)]
        self.animals = []
        self.generate_world()
        self.spawn_animals()
        
    def spawn_animals(self):
        # Spawn animals on surface
        for _ in range(12):  # Spawn regular animals
            animal_type = random.choice([AnimalType.COW, AnimalType.PIG, AnimalType.CHICKEN, AnimalType.SHEEP, AnimalType.RABBIT])
            x = random.randint(50, self.width * TILE_SIZE - 50)
            
            # Find surface height for this x position
            tile_x = x // TILE_SIZE
            surface_y = self.find_surface(tile_x) - 1
            
            if surface_y > 0:
                y = surface_y * TILE_SIZE - 20  # Place animal on ground
                animal = Animal(x, y, animal_type)
                self.animals.append(animal)
        
        # Spawn Ralph and Frank (special foxes)
        ralph_x = random.randint(100, self.width * TILE_SIZE - 100)
        ralph_tile_x = ralph_x // TILE_SIZE
        ralph_surface_y = self.find_surface(ralph_tile_x) - 1
        if ralph_surface_y > 0:
            ralph_y = ralph_surface_y * TILE_SIZE - 20
            ralph = Animal(ralph_x, ralph_y, AnimalType.RALPH_FOX)
            self.animals.append(ralph)
            
        frank_x = random.randint(100, self.width * TILE_SIZE - 100)
        frank_tile_x = frank_x // TILE_SIZE
        frank_surface_y = self.find_surface(frank_tile_x) - 1
        if frank_surface_y > 0:
            frank_y = frank_surface_y * TILE_SIZE - 20
            frank = Animal(frank_x, frank_y, AnimalType.FRANK_FOX)
            self.animals.append(frank)
                
    def update_animals(self):
        for animal in self.animals[:]:
            animal.update(self)
            # Remove dead animals
            if not animal.alive:
                self.animals.remove(animal)
        
    def generate_world(self):
        # Generate bedrock layer
        for x in range(self.width):
            self.blocks[x][self.height - 1] = BlockType.BEDROCK
            
        # Generate terrain with realistic height variation
        ground_height = int(self.height * 0.6)
        
        for x in range(self.width):
            # Multiple octaves of noise for realistic terrain
            height_variation = int(
                math.sin(x * 0.01) * 15 +  # Large hills
                math.sin(x * 0.03) * 8 +   # Medium features
                math.sin(x * 0.1) * 3 +    # Small details
                random.randint(-2, 2)       # Random variation
            )
            surface_y = ground_height + height_variation
            
            # Generate layers properly
            for y in range(surface_y, self.height - 1):  # Don't overwrite bedrock
                depth = y - surface_y
                
                if depth == 0:
                    self.blocks[x][y] = BlockType.GRASS
                elif depth < 3:
                    self.blocks[x][y] = BlockType.DIRT
                elif depth < 8:
                    # Mix of dirt and stone
                    if random.random() < 0.8:
                        self.blocks[x][y] = BlockType.STONE
                    else:
                        self.blocks[x][y] = BlockType.DIRT
                else:
                    self.blocks[x][y] = BlockType.STONE
                    
            # Generate caves
            if random.random() < 0.08:
                cave_y = surface_y + random.randint(5, 20)
                self.generate_cave(x, cave_y)
                
            # Generate ore veins properly
            for y in range(surface_y + 5, self.height - 2):
                depth = y - surface_y
                
                # Coal veins (common, all depths)
                if random.random() < 0.1:
                    self.generate_ore_vein(x, y, BlockType.COAL, 3, 6)
                    
                # Iron veins (medium depth)
                elif depth > 10 and random.random() < 0.06:
                    self.generate_ore_vein(x, y, BlockType.IRON, 2, 4)
                    
                # Gold veins (deep)
                elif depth > 20 and random.random() < 0.03:
                    self.generate_ore_vein(x, y, BlockType.GOLD, 2, 3)
                    
                # Diamond veins (very deep)
                elif depth > 30 and random.random() < 0.01:
                    self.generate_ore_vein(x, y, BlockType.DIAMOND, 1, 2)
                    
        # Generate forests
        for x in range(20, self.width - 20, random.randint(10, 20)):
            if random.random() < 0.7:
                surface_y = self.find_surface(x)
                if surface_y < self.height - 15:
                    self.generate_tree(x, surface_y - 1)
                    
        # Generate water features
        self.generate_water_features()
        
    def generate_cave(self, start_x, start_y):
        cave_length = random.randint(5, 15)
        for i in range(cave_length):
            x = start_x + i
            y = start_y + random.randint(-2, 2)
            
            if 0 <= x < self.width and 5 <= y < self.height - 2:
                # Make cave wider
                for dy in range(-1, 2):
                    for dx in range(-1, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 5 <= ny < self.height - 2:
                            if self.blocks[nx][ny] != BlockType.BEDROCK:
                                self.blocks[nx][ny] = BlockType.AIR
                                
    def generate_ore_vein(self, start_x, start_y, ore_type, min_size, max_size):
        vein_size = random.randint(min_size, max_size)
        for _ in range(vein_size):
            x = start_x + random.randint(-2, 2)
            y = start_y + random.randint(-2, 2)
            
            if 0 <= x < self.width and 5 <= y < self.height - 2:
                if self.blocks[x][y] == BlockType.STONE:
                    self.blocks[x][y] = ore_type
                    
    def generate_tree(self, x, y):
        # Generate proper tree with logs
        trunk_height = random.randint(5, 8)
        
        # Tree trunk (logs)
        for i in range(trunk_height):
            if y - i >= 0:
                self.blocks[x][y - i] = BlockType.LOG
                
        # Tree leaves in proper pattern
        leaf_radius = 3
        for dx in range(-leaf_radius, leaf_radius + 1):
            for dy in range(-leaf_radius, leaf_radius + 1):
                if abs(dx) + abs(dy) <= leaf_radius:
                    nx, ny = x + dx, y - trunk_height - dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.blocks[nx][ny] == BlockType.AIR:
                            self.blocks[nx][ny] = BlockType.LEAVES
                            
    def generate_water_features(self):
        # Generate lakes
        for _ in range(4):
            lake_x = random.randint(30, self.width - 30)
            lake_y = self.find_surface(lake_x) + 1
            lake_radius = random.randint(4, 8)
            
            for dx in range(-lake_radius, lake_radius + 1):
                for dy in range(-lake_radius, lake_radius + 1):
                    if dx*dx + dy*dy <= lake_radius*lake_radius:
                        nx, ny = lake_x + dx, lake_y + dy
                        if 0 <= nx < self.width and ny < self.height - 1:
                            if self.blocks[nx][ny] != BlockType.BEDROCK:
                                self.blocks[nx][ny] = BlockType.WATER
                                
    def find_surface(self, x):
        for y in range(self.height):
            if self.blocks[x][y] != BlockType.AIR:
                return y
        return self.height - 2
        
    def break_block(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            block_type = self.blocks[x][y]
            if block_type != BlockType.AIR and block_type != BlockType.BEDROCK:
                self.blocks[x][y] = BlockType.AIR
                return block_type
        return None
        
    def place_block(self, x, y, block_type):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.blocks[x][y] == BlockType.AIR:
                self.blocks[x][y] = block_type
                return True
        return False
        
    def draw_3d(self, screen, camera_x, camera_y):
        # First-person world rendering - like Minecraft!
        
        # Calculate visible range
        start_x = max(0, camera_x // TILE_SIZE)
        end_x = min(self.width, (camera_x + SCREEN_WIDTH) // TILE_SIZE + 1)
        start_y = max(0, camera_y // TILE_SIZE)
        end_y = min(self.height, (camera_y + SCREEN_HEIGHT) // TILE_SIZE + 1)
        
        # Draw blocks from back to front for proper depth
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.blocks[x][y] != BlockType.AIR:
                    screen_x = x * TILE_SIZE - camera_x
                    screen_y = y * TILE_SIZE - camera_y
                    
                    # Calculate distance from player for depth shading
                    world_x = x * TILE_SIZE + TILE_SIZE // 2
                    world_y = y * TILE_SIZE + TILE_SIZE // 2
                    distance = math.sqrt((world_x - (camera_x + SCREEN_WIDTH // 2))**2 + 
                                       (world_y - (camera_y + SCREEN_HEIGHT // 2))**2)
                    
                    # Apply distance-based shading
                    base_color = BLOCK_COLORS[self.blocks[x][y]]
                    if distance > 200:
                        # Far blocks - darker
                        color = tuple(max(0, c - 80) for c in base_color[:3])
                    elif distance > 100:
                        # Medium distance - slightly darker
                        color = tuple(max(0, c - 40) for c in base_color[:3])
                    else:
                        # Near blocks - full color
                        color = base_color
                    
                    # Draw block with 3D-style shading
                    block_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, block_rect)
                    
                    # Draw top and left edges for 3D effect (lighting)
                    if distance < 150:  # Only for nearby blocks
                        # Top edge (brightest)
                        top_color = tuple(min(255, c + 50) for c in color[:3])
                        pygame.draw.line(screen, top_color, 
                                     (screen_x, screen_y), 
                                     (screen_x + TILE_SIZE, screen_y), 3)
                        # Left edge (bright)
                        left_color = tuple(min(255, c + 30) for c in color[:3])
                        pygame.draw.line(screen, left_color, 
                                     (screen_x, screen_y), 
                                     (screen_x, screen_y + TILE_SIZE), 3)
                    
                    # Draw block outline for definition
                    pygame.draw.rect(screen, tuple(max(0, c - 100) for c in color[:3]), block_rect, 1)

class CraftingSystem:
    def __init__(self):
        self.recipes = CRAFTING_RECIPES
        self.is_open = False
        
    def can_craft(self, item_type, inventory):
        if item_type not in self.recipes:
            return False
            
        for ingredient, count in self.recipes[item_type]:
            if inventory.get(ingredient, 0) < count:
                return False
        return True
        
    def craft(self, item_type, inventory):
        if not self.can_craft(item_type, inventory):
            return False
            
        # Remove ingredients
        for ingredient, count in self.recipes[item_type]:
            inventory[ingredient] -= count
            if inventory[ingredient] <= 0:
                del inventory[ingredient]
                
        # Add crafted item
        inventory[item_type] += 1
        return True

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("REAL Minecraft - With Weapons & Animals!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.world = World(300, 150)
        self.player = Player(SCREEN_WIDTH // 2, 200)
        self.crafting = CraftingSystem()
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # UI
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.show_inventory = False
        self.show_weapons = False
        self.show_food = False
        self.time_of_day = 0
        
        # Particles
        self.particles = []
        
        # Combat
        self.last_attack_time = 0
        
    def add_explosion_particles(self, x, y, block_type):
        if block_type == BlockType.AIR:
            return
            
        color = BLOCK_COLORS.get(block_type, WHITE)
        block_center_x = x * TILE_SIZE + TILE_SIZE // 2
        block_center_y = y * TILE_SIZE + TILE_SIZE // 2
        
        # EPIC explosion with tons of particles
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 12)
            
            particle = {
                'x': block_center_x,
                'y': block_center_y,
                'vel_x': math.cos(angle) * speed,
                'vel_y': math.sin(angle) * speed - random.uniform(3, 8),
                'color': color,
                'life': random.randint(50, 80),
                'size': random.randint(4, 10),
                'gravity': 0.5
            }
            self.particles.append(particle)
            
        # Add debris
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 6)
            
            particle = {
                'x': block_center_x + random.randint(-10, 10),
                'y': block_center_y + random.randint(-10, 10),
                'vel_x': math.cos(angle) * speed,
                'vel_y': math.sin(angle) * speed - random.uniform(1, 4),
                'color': color,
                'life': random.randint(30, 50),
                'size': random.randint(2, 5),
                'gravity': 0.3
            }
            self.particles.append(particle)
            
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['vel_y'] += particle.get('gravity', 0.3)
            particle['vel_x'] *= 0.98
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self):
        for particle in self.particles:
            alpha = particle['life'] / 80
            size = int(particle['size'] * alpha)
            if size > 0:
                screen_x = int(particle['x'] - self.camera_x)
                screen_y = int(particle['y'] - self.camera_y)
                
                # EPIC particle effects
                if size > 6:
                    glow_color = tuple(min(255, c + 80) for c in particle['color'][:3])
                    pygame.draw.circle(self.screen, glow_color, (screen_x, screen_y), size + 3)
                
                pygame.draw.circle(self.screen, particle['color'], (screen_x, screen_y), size)
                
                if size > 3 and alpha > 0.5:
                    bright_color = tuple(min(255, c + 120) for c in particle['color'][:3])
                    pygame.draw.circle(self.screen, bright_color, (screen_x, screen_y), max(1, size // 2))
        
    def update_camera(self):
        # First-person camera - always centered on player
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Keep camera in world bounds
        self.camera_x = max(0, min(self.camera_x, self.world.width * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world.height * TILE_SIZE - SCREEN_HEIGHT))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show_inventory = not self.show_inventory
                    self.show_weapons = False
                    self.show_food = False
                elif event.key == pygame.K_q:
                    self.show_weapons = not self.show_weapons
                    self.show_inventory = False
                    self.show_food = False
                elif event.key == pygame.K_f:
                    self.show_food = not self.show_food
                    self.show_inventory = False
                    self.show_weapons = False
                elif event.key == pygame.K_c:
                    self.crafting.is_open = not self.crafting.is_open
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    slot = event.key - pygame.K_1
                    if slot < len(self.player.hotbar):
                        self.player.selected_slot = slot
                        self.player.selected_block = self.player.hotbar[slot]
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check hotbar clicks
                hotbar_y = SCREEN_HEIGHT - 80
                if hotbar_y <= mouse_y <= hotbar_y + 60:
                    for i in range(9):
                        slot_x = SCREEN_WIDTH // 2 - 180 + i * 40
                        if slot_x <= mouse_x <= slot_x + 35:
                            if i < len(self.player.hotbar):
                                self.player.selected_slot = i
                                self.player.selected_block = self.player.hotbar[i]
                            break
                
                # Check weapon clicks
                elif self.show_weapons:
                    self.handle_weapon_click(mouse_x, mouse_y)
                
                # Check food clicks
                elif self.show_food:
                    self.handle_food_click(mouse_x, mouse_y)
                
                # Check crafting clicks
                elif self.crafting.is_open:
                    self.handle_crafting_click(mouse_x, mouse_y)
                
                # World interactions (first-person!)
                else:
                    world_x = int((SCREEN_WIDTH // 2 + self.camera_x) // TILE_SIZE)
                    world_y = int((SCREEN_HEIGHT // 2 + self.camera_y) // TILE_SIZE)
                    
                    if event.button == 1:  # Left click - MINE or ATTACK!
                        # Check if looking at animal first
                        clicked_animal = False
                        for animal in self.world.animals:
                            if animal.alive:
                                # Check if crosshair is on animal
                                animal_screen_rect = pygame.Rect(
                                    animal.x - self.camera_x,
                                    animal.y - self.camera_y,
                                    animal.size, animal.size
                                )
                                
                                # Check if crosshair (center) is on animal
                                crosshair_rect = pygame.Rect(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, 20, 20)
                                if animal_screen_rect.colliderect(crosshair_rect):
                                    # Attack the animal!
                                    damage = self.player.attack(animal)
                                    died = animal.take_damage(damage)
                                    
                                    if died:
                                        # Animal died, drop food
                                        food_type = animal.properties["food"]
                                        food_amount = animal.properties["food_amount"]
                                        self.player.food_inventory[food_type] += food_amount
                                        
                                        # Death particles
                                        self.add_blood_particles(animal.x + animal.size // 2, 
                                                                animal.y + animal.size // 2)
                                    
                                    clicked_animal = True
                                    break
                        
                        # If not looking at animal, mine block
                        if not clicked_animal:
                            block = self.world.break_block(world_x, world_y)
                            if block and block != BlockType.AIR:
                                self.add_explosion_particles(world_x, world_y, block)
                                self.player.inventory[block] += 1
                                
                    elif event.button == 3:  # Right click - PLACE BLOCKS
                        # Place block at crosshair position
                        block_rect = pygame.Rect(world_x * TILE_SIZE, world_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        
                        # Check if not placing on player
                        player_world_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
                        if not block_rect.colliderect(player_world_rect):
                            if self.player.selected_block in self.player.inventory:
                                if self.player.inventory[self.player.selected_block] > 0:
                                    if self.world.place_block(world_x, world_y, self.player.selected_block):
                                        self.player.inventory[self.player.selected_block] -= 1
                                        
    def handle_weapon_click(self, mouse_x, mouse_y):
        # Weapon selection interface
        weapon_x = SCREEN_WIDTH // 2 - 150
        weapon_y = SCREEN_HEIGHT // 2 - 100
        
        weapons = list(self.player.weapon_inventory.keys())
        for i, weapon in enumerate(weapons):
            item_y = weapon_y + 30 + i * 35
            if weapon_x <= mouse_x <= weapon_x + 300 and item_y <= mouse_y <= item_y + 30:
                self.player.equip_weapon(weapon)
                break
                
    def handle_food_click(self, mouse_x, mouse_y):
        # Food eating interface
        food_x = SCREEN_WIDTH // 2 - 150
        food_y = SCREEN_HEIGHT // 2 - 100
        
        foods = list(self.player.food_inventory.keys())
        for i, food in enumerate(foods):
            if self.player.food_inventory[food] > 0:
                item_y = food_y + 30 + i * 35
                if food_x <= mouse_x <= food_x + 300 and item_y <= mouse_y <= item_y + 30:
                    self.player.eat_food(food)
                    break
                    
    def add_blood_particles(self, x, y):
        # Blood particles when animal dies
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            
            particle = {
                'x': x,
                'y': y,
                'vel_x': math.cos(angle) * speed,
                'vel_y': math.sin(angle) * speed - random.uniform(1, 4),
                'color': (200, 0, 0),  # Red blood
                'life': random.randint(20, 40),
                'size': random.randint(2, 5),
                'gravity': 0.3
            }
            self.particles.append(particle)
            
    def handle_crafting_click(self, mouse_x, mouse_y):
        # Simple crafting grid
        craft_x = SCREEN_WIDTH // 2 - 150
        craft_y = SCREEN_HEIGHT // 2 - 100
        
        # Check recipe clicks
        recipes = list(CRAFTING_RECIPES.keys())
        for i, recipe in enumerate(recipes):
            item_y = craft_y + 30 + i * 40
            if craft_x <= mouse_x <= craft_x + 300 and item_y <= mouse_y <= item_y + 35:
                if self.crafting.can_craft(recipe, self.player.inventory):
                    self.crafting.craft(recipe, self.player.inventory)
                    
    def draw_sky(self):
        # Dynamic sky with day/night cycle
        day_progress = (self.time_of_day % 1000) / 1000
        
        for y in range(SCREEN_HEIGHT // 2):
            if day_progress < 0.25:  # Morning
                color = (135 + int(120 * day_progress * 4), 206, 235)
            elif day_progress < 0.5:  # Day
                color = (135, 206, 235)
            elif day_progress < 0.75:  # Evening
                color = (135 - int(100 * (day_progress - 0.5) * 4), 206 - int(50 * (day_progress - 0.5) * 4), 235)
            else:  # Night
                color = (35, 106, 135)
                
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # Sun/Moon
        if day_progress < 0.5:
            # Sun
            sun_x = int(SCREEN_WIDTH * day_progress * 2)
            sun_y = 50 + int(30 * math.sin(day_progress * math.pi * 2))
            pygame.draw.circle(self.screen, (255, 255, 0), (sun_x, sun_y), 30)
        else:
            # Moon
            moon_x = int(SCREEN_WIDTH * (day_progress - 0.5) * 2)
            moon_y = 50 + int(30 * math.sin(day_progress * math.pi * 2))
            pygame.draw.circle(self.screen, (240, 240, 240), (moon_x, moon_y), 25)
            
        # Clouds
        for i in range(5):
            cloud_x = int((i * 250 + self.time_of_day * 0.2) % (SCREEN_WIDTH + 100) - 50)
            cloud_y = 80 + i * 40
            for j in range(4):
                pygame.draw.circle(self.screen, (255, 255, 255), 
                                 (cloud_x + j * 25, cloud_y), 20)
                                 
    def draw_ui(self):
        # Hotbar
        hotbar_y = SCREEN_HEIGHT - 80
        hotbar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, hotbar_y, 360, 60)
        pygame.draw.rect(self.screen, (50, 50, 50), hotbar_rect)
        pygame.draw.rect(self.screen, WHITE, hotbar_rect, 3)
        
        # Hotbar slots
        for i in range(9):
            slot_x = SCREEN_WIDTH // 2 - 170 + i * 40
            slot_rect = pygame.Rect(slot_x, hotbar_y + 5, 35, 35)
            
            if i == self.player.selected_slot:
                pygame.draw.rect(self.screen, WHITE, slot_rect, 4)
            else:
                pygame.draw.rect(self.screen, WHITE, slot_rect, 2)
                
            # Draw block
            if i < len(self.player.hotbar):
                block_type = self.player.hotbar[i]
                if block_type in BLOCK_COLORS:
                    color = BLOCK_COLORS[block_type]
                    pygame.draw.rect(self.screen, color, 
                                   (slot_x + 5, hotbar_y + 10, 25, 25))
                    pygame.draw.rect(self.screen, BLACK, 
                                   (slot_x + 5, hotbar_y + 10, 25, 25), 1)
                                   
            # Draw quantity
            if i < len(self.player.hotbar):
                block_type = self.player.hotbar[i]
                count = self.player.inventory.get(block_type, 0)
                if count > 0:
                    count_text = self.font.render(str(count), True, WHITE)
                    self.screen.blit(count_text, (slot_x + 2, hotbar_y + 30))
                    
        # Health and Hunger bars
        self.draw_status_bars()
        
        # Current weapon display
        weapon_name = self.player.current_weapon.name.replace('_', ' ').title()
        weapon_damage = self.player.attack_damage
        weapon_text = self.font.render(f"Weapon: {weapon_name} (DMG: {weapon_damage})", True, WHITE)
        self.screen.blit(weapon_text, (10, SCREEN_HEIGHT - 150))
        
        if self.player.current_weapon in self.player.weapon_durability:
            durability = self.player.weapon_durability[self.player.current_weapon]
            max_dur = WEAPON_STATS[self.player.current_weapon]["durability"]
            if max_dur > 0:
                dur_text = self.font.render(f"Durability: {durability}/{max_dur}", True, WHITE)
                self.screen.blit(dur_text, (10, SCREEN_HEIGHT - 125))
        
        # Controls
        controls = [
            "WASD: Move | Space: Jump",
            "Left Click: Mine/Attack | Right Click: Place",
            "1-9: Select | E: Inventory | Q: Weapons | F: Food | C: Crafting"
        ]
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, WHITE)
            self.screen.blit(control_text, (10, 10 + i * 25))
            
        # Selected item
        selected_name = self.player.selected_block.name.replace('_', ' ').title()
        selected_text = self.big_font.render(f"Selected: {selected_name}", True, WHITE)
        self.screen.blit(selected_text, (10, SCREEN_HEIGHT - 120))
        
        # Inventory
        if self.show_inventory:
            self.draw_inventory()
            
        # Weapons
        if self.show_weapons:
            self.draw_weapons()
            
        # Food
        if self.show_food:
            self.draw_food()
            
        # Crafting
        if self.crafting.is_open:
            self.draw_crafting()
            
    def draw_status_bars(self):
        # Health bar
        health_rect = pygame.Rect(SCREEN_WIDTH - 220, 20, 200, 20)
        pygame.draw.rect(self.screen, (100, 0, 0), health_rect)
        health_fill = pygame.Rect(SCREEN_WIDTH - 220, 20, 
                                 int(200 * self.player.health / self.player.max_health), 20)
        pygame.draw.rect(self.screen, (255, 0, 0), health_fill)
        pygame.draw.rect(self.screen, WHITE, health_rect, 2)
        
        health_text = self.font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (SCREEN_WIDTH - 210, 22))
        
        # Hunger bar
        hunger_rect = pygame.Rect(SCREEN_WIDTH - 220, 50, 200, 20)
        pygame.draw.rect(self.screen, (100, 50, 0), hunger_rect)
        hunger_fill = pygame.Rect(SCREEN_WIDTH - 220, 50, 
                                int(200 * self.player.hunger / self.player.max_hunger), 20)
        pygame.draw.rect(self.screen, (255, 165, 0), hunger_fill)
        pygame.draw.rect(self.screen, WHITE, hunger_rect, 2)
        
        hunger_text = self.font.render(f"Hunger: {self.player.hunger}/{self.player.max_hunger}", True, WHITE)
        self.screen.blit(hunger_text, (SCREEN_WIDTH - 210, 52))
        
    def draw_inventory(self):
        # Inventory background
        inv_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 200, 500, 400)
        pygame.draw.rect(self.screen, (40, 40, 40), inv_rect)
        pygame.draw.rect(self.screen, WHITE, inv_rect, 3)
        
        # Title
        title_text = self.big_font.render("INVENTORY", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170))
        self.screen.blit(title_text, title_rect)
        
        # Draw items
        y_offset = SCREEN_HEIGHT // 2 - 130
        for i, (block_type, count) in enumerate(self.player.inventory.items()):
            if count > 0:
                name = block_type.name.replace('_', ' ').title()
                item_text = self.font.render(f"{name}: {count}", True, WHITE)
                self.screen.blit(item_text, (SCREEN_WIDTH // 2 - 230, y_offset + i * 30))
        
    def draw_weapons(self):
        # Weapons background
        weapon_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        pygame.draw.rect(self.screen, (40, 40, 40), weapon_rect)
        pygame.draw.rect(self.screen, WHITE, weapon_rect, 3)
        
        # Title
        title_text = self.big_font.render("WEAPONS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)
        
        # Draw weapons
        y_offset = SCREEN_HEIGHT // 2 - 80
        for i, (weapon_type, count) in enumerate(self.player.weapon_inventory.items()):
            if count > 0:
                name = weapon_type.name.replace('_', ' ').title()
                damage = WEAPON_STATS[weapon_type]["damage"]
                durability = self.player.weapon_durability.get(weapon_type, 0)
                max_dur = WEAPON_STATS[weapon_type]["durability"]
                
                # Highlight equipped weapon
                if weapon_type == self.player.current_weapon:
                    color = (0, 255, 0)
                else:
                    color = WHITE
                    
                weapon_text = self.font.render(f"{name} - DMG: {damage} - Dur: {durability}/{max_dur}", True, color)
                self.screen.blit(weapon_text, (SCREEN_WIDTH // 2 - 190, y_offset + i * 35))
                
    def draw_food(self):
        # Food background
        food_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        pygame.draw.rect(self.screen, (40, 40, 40), food_rect)
        pygame.draw.rect(self.screen, WHITE, food_rect, 3)
        
        # Title
        title_text = self.big_font.render("FOOD", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        inst_text = self.font.render("Click food to eat (restores hunger)", True, (200, 200, 200))
        self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 90))
        
        # Draw food items
        y_offset = SCREEN_HEIGHT // 2 - 60
        for i, (food_type, count) in enumerate(self.player.food_inventory.items()):
            if count > 0:
                name = food_type.name.replace('_', ' ').title()
                hunger_restore = FOOD_PROPERTIES[food_type]["hunger"]
                color = FOOD_PROPERTIES[food_type]["color"]
                
                # Draw food icon
                pygame.draw.circle(self.screen, color, 
                                 (SCREEN_WIDTH // 2 - 170, y_offset + i * 35 + 10), 8)
                
                food_text = self.font.render(f"{name} x{count} (Restores {hunger_restore} hunger)", True, WHITE)
                self.screen.blit(food_text, (SCREEN_WIDTH // 2 - 150, y_offset + i * 35))
                
    def draw_crafting(self):
        # Crafting background
        craft_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        pygame.draw.rect(self.screen, (40, 40, 40), craft_rect)
        pygame.draw.rect(self.screen, WHITE, craft_rect, 3)
        
        # Title
        title_text = self.big_font.render("CRAFTING", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)
        
        # Recipes
        y_offset = SCREEN_HEIGHT // 2 - 80
        for i, (item_type, ingredients) in enumerate(CRAFTING_RECIPES.items()):
            name = item_type.name.replace('_', ' ').title()
            
            # Check if can craft
            can_craft = self.crafting.can_craft(item_type, self.player.inventory)
            color = (0, 255, 0) if can_craft else (255, 0, 0)
            
            recipe_text = f"{name}: "
            for ingredient, count in ingredients:
                recipe_text += f"{ingredient.name.replace('_', ' ').title()} x{count} "
                
            text = self.font.render(recipe_text, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 190, y_offset + i * 35))
            
    def run(self):
        while self.running:
            self.handle_events()
            
            # Update
            keys = pygame.key.get_pressed()
            self.player.update(self.world, keys)
            self.world.update_animals()
            self.update_camera()
            self.update_particles()
            self.time_of_day += 1
            
            # Draw
            self.draw_sky()
            self.world.draw_3d(self.screen, self.camera_x, self.camera_y)
            
            # Draw animals
            for animal in self.world.animals:
                animal.draw(self.screen, self.camera_x, self.camera_y)
            
            self.player.draw_3d(self.screen, self.camera_x, self.camera_y)
            self.draw_particles()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
