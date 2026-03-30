#!/usr/bin/env python3
"""
Minecraft-like Game
A simple 2D Minecraft-inspired game with mining, crafting, and building
"""

import pygame
import random
import math
import noise
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TILE_SIZE = 32

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
SUN_YELLOW = (255, 255, 0)
CLOUD_WHITE = (255, 255, 255)

# Block colors and types
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

BLOCK_COLORS = {
    BlockType.AIR: (0, 0, 0, 0),
    BlockType.GRASS: (34, 139, 34),
    BlockType.DIRT: (139, 69, 19),
    BlockType.STONE: (128, 128, 128),
    BlockType.WOOD: (160, 82, 45),
    BlockType.LEAVES: (0, 128, 0),
    BlockType.SAND: (238, 203, 173),
    BlockType.WATER: (64, 164, 223),
    BlockType.COAL: (54, 54, 54),
    BlockType.IRON: (192, 192, 192),
    BlockType.GOLD: (255, 215, 0),
    BlockType.DIAMOND: (185, 242, 255),
    BlockType.CRAFTING_TABLE: (139, 90, 43),
    BlockType.FURNACE: (105, 105, 105)
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 48
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.speed = 4
        self.jump_power = 10
        self.gravity = 0.5
        self.max_fall_speed = 12
        self.inventory = {
            BlockType.DIRT: 64,
            BlockType.STONE: 64,
            BlockType.WOOD: 32,
            BlockType.GRASS: 64,
            BlockType.SAND: 32,
            BlockType.COAL: 16,
            BlockType.IRON: 8,
            BlockType.WATER: 16
        }
        self.selected_block = BlockType.DIRT
        self.health = 100
        self.hunger = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, world, keys):
        # Store old position for collision resolution
        old_rect = self.rect.copy()
        
        # Horizontal movement
        target_vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            target_vel_x = -self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            target_vel_x = self.speed
        
        # Smooth acceleration
        self.vel_x += (target_vel_x - self.vel_x) * 0.8
        
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -self.jump_power
            
        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed
                
        # Move horizontally and check collisions
        self.rect.x += self.vel_x
        self.resolve_collisions_x(world)
        
        # Move vertically and check collisions
        self.rect.y += self.vel_y
        self.on_ground = False
        self.resolve_collisions_y(world)
        
        # Update position for compatibility
        self.x = self.rect.x
        self.y = self.rect.y
        
        # Keep player in bounds
        self.rect.x = max(0, min(self.rect.x, world.width * TILE_SIZE - self.width))
        self.rect.y = max(0, min(self.rect.y, world.height * TILE_SIZE - self.height))
        
    def resolve_collisions_x(self, world):
        # Get player bounds in tile coordinates
        left_tile = max(0, self.rect.left // TILE_SIZE)
        right_tile = min(world.width - 1, self.rect.right // TILE_SIZE)
        top_tile = max(0, self.rect.top // TILE_SIZE)
        bottom_tile = min(world.height - 1, self.rect.bottom // TILE_SIZE)
        
        for x in range(left_tile, right_tile + 1):
            for y in range(top_tile, bottom_tile + 1):
                if world.blocks[x][y] != BlockType.AIR:
                    block_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if self.rect.colliderect(block_rect):
                        # Calculate overlap on each side
                        overlap_left = self.rect.right - block_rect.left
                        overlap_right = block_rect.right - self.rect.left
                        
                        # Push out the side with less overlap
                        if overlap_left < overlap_right:
                            self.rect.right = block_rect.left
                        else:
                            self.rect.left = block_rect.right
                        self.vel_x = 0
                        return
                        
    def resolve_collisions_y(self, world):
        # Get player bounds in tile coordinates
        left_tile = max(0, self.rect.left // TILE_SIZE)
        right_tile = min(world.width - 1, self.rect.right // TILE_SIZE)
        top_tile = max(0, self.rect.top // TILE_SIZE)
        bottom_tile = min(world.height - 1, self.rect.bottom // TILE_SIZE)
        
        for x in range(left_tile, right_tile + 1):
            for y in range(top_tile, bottom_tile + 1):
                if world.blocks[x][y] != BlockType.AIR:
                    block_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if self.rect.colliderect(block_rect):
                        # Calculate overlap on each side
                        overlap_top = self.rect.bottom - block_rect.top
                        overlap_bottom = block_rect.bottom - self.rect.top
                        
                        # Push out the side with less overlap
                        if overlap_top < overlap_bottom:
                            self.rect.bottom = block_rect.top
                            self.on_ground = True
                        else:
                            self.rect.top = block_rect.bottom
                        self.vel_y = 0
                        return
                            
    def draw(self, screen, camera_x, camera_y):
        # Draw player body (better proportions)
        body_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y + 8, self.width, self.height - 8)
        pygame.draw.rect(screen, (0, 100, 200), body_rect)
        pygame.draw.rect(screen, BLACK, body_rect, 2)
        
        # Draw player head
        head_rect = pygame.Rect(self.rect.x - camera_x + 2, self.rect.y - camera_y, self.width - 4, 16)
        pygame.draw.rect(screen, (255, 220, 177), head_rect)
        pygame.draw.rect(screen, BLACK, head_rect, 1)
        
        # Draw eyes
        eye_y = self.rect.y - camera_y + 5
        pygame.draw.circle(screen, BLACK, (self.rect.x - camera_x + 8, eye_y), 2)
        pygame.draw.circle(screen, BLACK, (self.rect.x - camera_x + 16, eye_y), 2)
        
        # Draw legs (simple animation when moving)
        if abs(self.vel_x) > 0.5:
            leg_offset = int(pygame.time.get_ticks() / 100) % 2 * 2
            pygame.draw.rect(screen, (0, 50, 150), 
                           (self.rect.x - camera_x + 4, self.rect.y - camera_y + self.height - 12, 6, 12))
            pygame.draw.rect(screen, (0, 50, 150), 
                           (self.rect.x - camera_x + 14, self.rect.y - camera_y + self.height - 12 + leg_offset, 6, 12))
        else:
            pygame.draw.rect(screen, (0, 50, 150), 
                           (self.rect.x - camera_x + 4, self.rect.y - camera_y + self.height - 12, 6, 12))
            pygame.draw.rect(screen, (0, 50, 150), 
                           (self.rect.x - camera_x + 14, self.rect.y - camera_y + self.height - 12, 6, 12))

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blocks = [[BlockType.AIR for _ in range(height)] for _ in range(width)]
        self.generate_world()
        
    def generate_world(self):
        # Generate more interesting terrain
        ground_height = int(self.height * 0.6)
        
        for x in range(self.width):
            # Create more varied terrain with multiple noise layers
            height_variation = int(
                math.sin(x * 0.02) * 8 +  # Large hills
                math.sin(x * 0.05) * 4 +  # Medium variations  
                math.sin(x * 0.1) * 2 +   # Small details
                random.randint(-1, 1)      # Random noise
            )
            surface_y = ground_height + height_variation
            
            # Generate layers
            for y in range(surface_y, self.height):
                depth = y - surface_y
                
                if depth == 0:
                    self.blocks[x][y] = BlockType.GRASS
                elif depth < 3:
                    self.blocks[x][y] = BlockType.DIRT
                elif depth < 8:
                    # Mix of dirt and stone in transition layer
                    if random.random() < 0.7:
                        self.blocks[x][y] = BlockType.STONE
                    else:
                        self.blocks[x][y] = BlockType.DIRT
                else:
                    self.blocks[x][y] = BlockType.STONE
                    
            # Add caves (simple horizontal caves)
            if random.random() < 0.05:
                cave_y = surface_y + random.randint(5, 15)
                cave_length = random.randint(3, 8)
                for i in range(cave_length):
                    cave_x = x + i
                    if 0 <= cave_x < self.width and cave_y < self.height:
                        self.blocks[cave_x][cave_y] = BlockType.AIR
                        # Sometimes make caves bigger
                        if random.random() < 0.3:
                            if cave_y + 1 < self.height:
                                self.blocks[cave_x][cave_y + 1] = BlockType.AIR
                                
            # Add ore deposits (more realistic distribution)
            for y in range(surface_y + 5, self.height):
                depth = y - surface_y
                
                # Coal - common, found at all depths
                if random.random() < 0.08:
                    self.create_ore_vein(x, y, BlockType.COAL, 2, 4)
                    
                # Iron - medium rarity, found deeper
                elif depth > 10 and random.random() < 0.04:
                    self.create_ore_vein(x, y, BlockType.IRON, 2, 3)
                    
                # Gold - rare, found deep
                elif depth > 20 and random.random() < 0.02:
                    self.create_ore_vein(x, y, BlockType.GOLD, 1, 2)
                    
                # Diamond - very rare, found very deep
                elif depth > 30 and random.random() < 0.008:
                    self.create_ore_vein(x, y, BlockType.DIAMOND, 1, 2)
                    
        # Generate better forests
        for x in range(15, self.width - 15, random.randint(8, 15)):
            if random.random() < 0.6:
                surface_y = self.find_surface(x)
                if surface_y < self.height - 10:  # Don't build trees too low
                    self.generate_tree(x, surface_y - 1)
                    
        # Add rivers and lakes
        self.create_water_features()
        
    def create_ore_vein(self, start_x, start_y, ore_type, min_size, max_size):
        """Create a small vein of ore"""
        vein_size = random.randint(min_size, max_size)
        for _ in range(vein_size):
            # Random walk from starting position
            x = start_x + random.randint(-1, 1)
            y = start_y + random.randint(-1, 1)
            
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.blocks[x][y] == BlockType.STONE:
                    self.blocks[x][y] = ore_type
                    
    def create_water_features(self):
        """Create rivers and lakes"""
        # Create a few lakes
        for _ in range(3):
            lake_x = random.randint(20, self.width - 20)
            lake_y = self.find_surface(lake_x) + 1
            lake_radius = random.randint(3, 6)
            
            for dx in range(-lake_radius, lake_radius + 1):
                for dy in range(-lake_radius, lake_radius + 1):
                    if dx*dx + dy*dy <= lake_radius*lake_radius:
                        nx, ny = lake_x + dx, lake_y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.blocks[nx][ny] != BlockType.AIR:
                                self.blocks[nx][ny] = BlockType.WATER
                                
        # Create a simple river
        river_y = self.find_surface(self.width // 2) + 2
        for x in range(0, self.width, 3):
            if random.random() < 0.7:
                # Make river meander slightly
                y_offset = int(math.sin(x * 0.02) * 3)
                for y in range(river_y + y_offset, min(river_y + y_offset + 3, self.height)):
                    if 0 <= x < self.width:
                        self.blocks[x][y] = BlockType.WATER
            
    def find_surface(self, x):
        for y in range(self.height):
            if self.blocks[x][y] != BlockType.AIR:
                return y
        return self.height - 1
        
    def generate_tree(self, x, y):
        # Tree trunk
        trunk_height = random.randint(4, 7)
        for i in range(trunk_height):
            if y - i >= 0:
                self.blocks[x][y - i] = BlockType.WOOD
                
        # Tree leaves
        leaf_radius = 3
        for dx in range(-leaf_radius, leaf_radius + 1):
            for dy in range(-leaf_radius, leaf_radius + 1):
                if abs(dx) + abs(dy) <= leaf_radius:
                    nx, ny = x + dx, y - trunk_height - dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.blocks[nx][ny] == BlockType.AIR:
                            self.blocks[nx][ny] = BlockType.LEAVES
                            
    def create_water_patch(self, x, y):
        radius = random.randint(2, 4)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.blocks[nx][ny] == BlockType.AIR:
                            self.blocks[nx][ny] = BlockType.WATER
                            
    def break_block(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            block_type = self.blocks[x][y]
            if block_type != BlockType.AIR:
                self.blocks[x][y] = BlockType.AIR
                return block_type
        return None
        
    def place_block(self, x, y, block_type):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.blocks[x][y] == BlockType.AIR:
                self.blocks[x][y] = block_type
                return True
        return False
        
    def draw(self, screen, camera_x, camera_y):
        # Calculate visible blocks
        start_x = max(0, int(camera_x // TILE_SIZE))
        end_x = min(self.width, int((camera_x + SCREEN_WIDTH) // TILE_SIZE) + 1)
        start_y = max(0, int(camera_y // TILE_SIZE))
        end_y = min(self.height, int((camera_y + SCREEN_HEIGHT) // TILE_SIZE) + 1)
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                block_type = self.blocks[x][y]
                if block_type != BlockType.AIR:
                    color = BLOCK_COLORS[block_type]
                    if len(color) == 4 and color[3] == 0:
                        continue
                        
                    rect = pygame.Rect(x * TILE_SIZE - camera_x, 
                                      y * TILE_SIZE - camera_y, 
                                      TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, rect)
                    
                    # Draw block borders for better visibility
                    pygame.draw.rect(screen, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft-like Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.world = World(200, 100)
        self.world.game = self  # Set reference for block breaking animation
        self.player = Player(SCREEN_WIDTH // 2, 200)
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # UI
        self.font = pygame.font.Font(None, 24)
        self.show_inventory = False
        self.time_of_day = 0
        
        # Particle effects
        self.particles = []
        
    def add_explosion_particles(self, x, y, block_type):
        """Add explosion particles when block is clicked"""
        if block_type == BlockType.AIR:
            return
            
        color = BLOCK_COLORS.get(block_type, WHITE)
        block_center_x = x * TILE_SIZE + TILE_SIZE // 2
        block_center_y = y * TILE_SIZE + TILE_SIZE // 2
        
        # Create explosion with many particles flying in all directions
        for _ in range(20):  # More particles for explosion
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)  # Faster particles for explosion
            
            particle = {
                'x': block_center_x,
                'y': block_center_y,
                'vel_x': math.cos(angle) * speed,
                'vel_y': math.sin(angle) * speed - random.uniform(2, 6),  # Upward bias
                'color': color,
                'life': random.randint(40, 60),  # Longer life for explosion
                'size': random.randint(3, 8),  # Bigger particles
                'gravity': 0.4
            }
            self.particles.append(particle)
            
        # Add some smaller debris particles
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            
            particle = {
                'x': block_center_x + random.randint(-8, 8),
                'y': block_center_y + random.randint(-8, 8),
                'vel_x': math.cos(angle) * speed,
                'vel_y': math.sin(angle) * speed - random.uniform(1, 3),
                'color': color,
                'life': random.randint(20, 40),
                'size': random.randint(1, 4),
                'gravity': 0.3
            }
            self.particles.append(particle)
            
    def update_particles(self):
        """Update particle positions and remove dead particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['vel_y'] += particle.get('gravity', 0.3)  # Use individual gravity
            particle['vel_x'] *= 0.98  # Air resistance
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self):
        """Draw all particles with explosion effect"""
        for particle in self.particles:
            # Calculate alpha based on life
            max_life = 60
            alpha = particle['life'] / max_life
            
            # Particle size decreases over time
            size = int(particle['size'] * alpha)
            if size > 0:
                screen_x = int(particle['x'] - self.camera_x)
                screen_y = int(particle['y'] - self.camera_y)
                
                # Draw particle with glow effect for explosions
                if size > 4:
                    # Draw glow for larger particles
                    glow_color = tuple(min(255, c + 50) for c in particle['color'][:3])
                    pygame.draw.circle(self.screen, glow_color, (screen_x, screen_y), size + 2)
                
                # Draw main particle
                pygame.draw.circle(self.screen, particle['color'], (screen_x, screen_y), size)
                
                # Add bright center for explosion particles
                if size > 2 and alpha > 0.5:
                    bright_color = tuple(min(255, c + 100) for c in particle['color'][:3])
                    pygame.draw.circle(self.screen, bright_color, (screen_x, screen_y), max(1, size // 2))
        
    def update_camera(self):
        # Follow player
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Keep camera in bounds
        self.camera_x = max(0, min(self.camera_x, self.world.width * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world.height * TILE_SIZE - SCREEN_HEIGHT))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show_inventory = not self.show_inventory
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if clicking on inventory hotbar
                hotbar_y = SCREEN_HEIGHT - 60
                if hotbar_y <= mouse_y <= hotbar_y + 50:
                    # Check which hotbar slot was clicked
                    for i in range(9):
                        slot_x = SCREEN_WIDTH // 2 - 170 + i * 40
                        if slot_x <= mouse_x <= slot_x + 35:
                            # Select this block type
                            block_types = list(BlockType)
                            if i + 1 < len(block_types):
                                self.player.selected_block = block_types[i + 1]
                            break
                
                # Check if clicking on world blocks
                else:
                    world_x = int((mouse_x + self.camera_x) // TILE_SIZE)
                    world_y = int((mouse_y + self.camera_y) // TILE_SIZE)
                    
                    if event.button == 1:  # Left click - pick up block with EXPLOSION!
                        block = self.world.break_block(world_x, world_y)
                        if block and block != BlockType.AIR:
                            self.add_explosion_particles(world_x, world_y, block)
                            if block in self.player.inventory:
                                self.player.inventory[block] += 1
                            else:
                                self.player.inventory[block] = 1
                                
                    elif event.button == 3:  # Right click - place block
                        # Don't place blocks on the player
                        block_rect = pygame.Rect(world_x * TILE_SIZE, world_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if not self.player.rect.colliderect(block_rect):
                            if self.player.selected_block in self.player.inventory:
                                if self.player.inventory[self.player.selected_block] > 0:
                                    if self.world.place_block(world_x, world_y, self.player.selected_block):
                                        self.player.inventory[self.player.selected_block] -= 1
                                
    def draw_sky(self):
        # Draw gradient sky
        for y in range(SCREEN_HEIGHT // 2):
            color_ratio = y / (SCREEN_HEIGHT // 2)
            color = (
                int(135 * (1 - color_ratio) + 255 * color_ratio),
                int(206 * (1 - color_ratio) + 255 * color_ratio),
                int(235 * (1 - color_ratio) + 255 * color_ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # Draw sun
        sun_x = int(SCREEN_WIDTH * 0.8)
        sun_y = int(50 + math.sin(self.time_of_day * 0.01) * 20)
        pygame.draw.circle(self.screen, SUN_YELLOW, (sun_x, sun_y), 30)
        
        # Draw clouds
        for i in range(3):
            cloud_x = int((i * 300 + self.time_of_day * 0.1) % SCREEN_WIDTH)
            cloud_y = 50 + i * 30
            for j in range(3):
                pygame.draw.circle(self.screen, CLOUD_WHITE, 
                                 (cloud_x + j * 20, cloud_y), 15)
                                 
    def draw_ui(self):
        # Draw hotbar
        hotbar_y = SCREEN_HEIGHT - 60
        hotbar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, hotbar_y, 360, 50)
        pygame.draw.rect(self.screen, (50, 50, 50), hotbar_rect)
        pygame.draw.rect(self.screen, WHITE, hotbar_rect, 2)
        
        # Draw inventory slots
        for i in range(9):
            slot_x = SCREEN_WIDTH // 2 - 170 + i * 40
            slot_rect = pygame.Rect(slot_x, hotbar_y + 5, 35, 35)
            
            # Highlight selected slot
            block_types = list(BlockType)
            if i + 1 < len(block_types) and self.player.selected_block == block_types[i + 1]:
                pygame.draw.rect(self.screen, WHITE, slot_rect, 3)
            else:
                pygame.draw.rect(self.screen, WHITE, slot_rect, 1)
                
            # Draw block in slot
            if i + 1 < len(block_types):
                block_type = block_types[i + 1]
                if block_type in BLOCK_COLORS:
                    color = BLOCK_COLORS[block_type]
                    pygame.draw.rect(self.screen, color, 
                                   (slot_x + 5, hotbar_y + 10, 25, 25))
                                   
            # Draw quantity
            if i + 1 < len(block_types):
                block_type = block_types[i + 1]
                if block_type in self.player.inventory:
                    count = self.player.inventory[block_type]
                    if count > 0:
                        count_text = self.font.render(str(count), True, WHITE)
                        self.screen.blit(count_text, (slot_x + 2, hotbar_y + 25))
                        
        # Draw selected block name
        selected_name = self.player.selected_block.name.replace('_', ' ').title()
        selected_text = self.font.render(f"Selected: {selected_name}", True, WHITE)
        self.screen.blit(selected_text, (10, 10))
        
        # Draw controls
        controls = [
            "WASD/Arrows: Move",
            "Space: Jump", 
            "Left Click: Pick Up Block",
            "Right Click: Place Block",
            "Click Hotbar: Select Block",
            "E: Inventory"
        ]
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, WHITE)
            self.screen.blit(control_text, (10, 40 + i * 25))
            
        # Draw inventory if open
        if self.show_inventory:
            self.draw_inventory()
            
    def draw_inventory(self):
        # Draw inventory background
        inv_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        pygame.draw.rect(self.screen, (50, 50, 50), inv_rect)
        pygame.draw.rect(self.screen, WHITE, inv_rect, 3)
        
        # Title
        title_text = self.font.render("INVENTORY", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title_text, title_rect)
        
        # Draw items
        y_offset = SCREEN_HEIGHT // 2 - 80
        for i, (block_type, count) in enumerate(self.player.inventory.items()):
            if count > 0:
                name = block_type.name.replace('_', ' ').title()
                item_text = self.font.render(f"{name}: {count}", True, WHITE)
                self.screen.blit(item_text, (SCREEN_WIDTH // 2 - 180, y_offset + i * 25))
                
    def run(self):
        while self.running:
            self.handle_events()
            
            # Update
            keys = pygame.key.get_pressed()
            self.player.update(self.world, keys)
            self.update_camera()
            self.update_particles()
            self.time_of_day += 1
            
            # Draw
            self.draw_sky()
            self.world.draw(self.screen, self.camera_x, self.camera_y)
            self.player.draw(self.screen, self.camera_x, self.camera_y)
            self.draw_particles()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
