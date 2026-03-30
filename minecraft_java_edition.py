#!/usr/bin/env python3
"""
REAL MINECRAFT JAVA EDITION - True Minecraft Experience!
Keyboard-based movement like real Minecraft Java Edition
No mouse movement - proper WASD/Arrow controls!
"""

import pygame
import math
import random
import sys
from enum import Enum
from collections import defaultdict

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 40
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
SKY_BLUE = (135, 206, 235)
SKY_NIGHT = (35, 106, 135)

# Block types
class BlockType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4
    LEAVES = 5
    SAND = 6
    COAL = 7
    IRON = 8
    GOLD = 9
    DIAMOND = 10
    PLANKS = 11
    STICKS = 12
    COBBLESTONE = 13
    LOG = 14
    CRAFTING_TABLE = 15
    FURNACE = 16
    TORCH = 17
    BEDROCK = 18

# Block colors
BLOCK_COLORS = {
    BlockType.AIR: (0, 0, 0, 0),
    BlockType.GRASS: (124, 169, 69),
    BlockType.DIRT: (139, 90, 43),
    BlockType.STONE: (136, 140, 141),
    BlockType.WOOD: (101, 67, 33),
    BlockType.LEAVES: (34, 139, 34),
    BlockType.SAND: (238, 203, 173),
    BlockType.COAL: (54, 54, 54),
    BlockType.IRON: (216, 216, 216),
    BlockType.GOLD: (255, 215, 0),
    BlockType.DIAMOND: (185, 242, 255),
    BlockType.PLANKS: (160, 120, 80),
    BlockType.STICKS: (101, 67, 33),
    BlockType.COBBLESTONE: (128, 128, 128),
    BlockType.LOG: (101, 67, 33),
    BlockType.CRAFTING_TABLE: (139, 90, 43),
    BlockType.FURNACE: (176, 176, 176),
    BlockType.TORCH: (255, 255, 200),
    BlockType.BEDROCK: (64, 64, 64)
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 12
        self.gravity = 0.8
        self.max_fall_speed = 15
        self.on_ground = False
        
        # Looking direction (like Minecraft!)
        self.yaw = 0  # Left/right rotation
        self.pitch = 0  # Up/down rotation
        
        # Inventory
        self.inventory = defaultdict(int)
        self.selected_block = BlockType.DIRT
        self.selected_slot = 0
        self.hotbar = [BlockType.DIRT, BlockType.STONE, BlockType.WOOD, BlockType.PLANKS, 
                      BlockType.COBBLESTONE, BlockType.LOG, BlockType.SAND, BlockType.CRAFTING_TABLE]
        
        # Give starting items
        for block_type in self.hotbar:
            self.inventory[block_type] = 64
            
    def update(self, world, keys):
        # Keyboard-based movement (NO MOUSE!)
        target_vel_x = 0
        target_vel_z = 0  # Forward/backward
        
        # WASD/Arrow movement (Minecraft-style)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            target_vel_z = -self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            target_vel_z = self.speed
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            target_vel_x = -self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            target_vel_x = self.speed
            
        # Apply movement based on yaw (Minecraft-style!)
        if target_vel_x != 0 or target_vel_z != 0:
            # Convert movement to world coordinates based on yaw
            move_x = target_vel_x * math.cos(math.radians(self.yaw)) - target_vel_z * math.sin(math.radians(self.yaw))
            move_y = target_vel_x * math.sin(math.radians(self.yaw)) + target_vel_z * math.cos(math.radians(self.yaw))
            
            self.vel_x = move_x
            self.vel_y = move_y
        else:
            # Apply friction
            self.vel_x *= 0.8
            self.vel_y *= 0.8
            
        # Gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed
                
        # Move and collide
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # World collision
        self.resolve_collisions(world)
        
        # Keep in bounds
        self.rect.x = max(0, min(self.rect.x, world.width * TILE_SIZE - self.width))
        self.rect.y = max(0, min(self.rect.y, world.height * TILE_SIZE - self.height))
        
        self.x = self.rect.x
        self.y = self.rect.y
        
    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            
    def resolve_collisions(self, world):
        # Ground collision
        self.on_ground = False
        
        # Check ground collision
        for x in range(self.rect.left // TILE_SIZE, self.rect.right // TILE_SIZE + 1):
            for y in range(self.rect.top // TILE_SIZE, self.rect.bottom // TILE_SIZE + 1):
                if 0 <= x < world.width and 0 <= y < world.height:
                    if world.blocks[x][y] != BlockType.AIR:
                        block_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if self.rect.colliderect(block_rect):
                            # Resolve collision
                            if self.vel_y > 0:  # Falling
                                self.rect.bottom = block_rect.top
                                self.on_ground = True
                                self.vel_y = 0
                            elif self.vel_y < 0:  # Jumping into ceiling
                                self.rect.top = block_rect.bottom
                                self.vel_y = 0
                            elif self.vel_x > 0:  # Moving right
                                self.rect.right = block_rect.left
                                self.vel_x = 0
                            elif self.vel_x < 0:  # Moving left
                                self.rect.left = block_rect.right
                                self.vel_x = 0
                            return
                            
    def draw_first_person(self, screen):
        # Draw first-person view (hand/weapon)
        # Draw equipped item in bottom center
        if self.selected_block == BlockType.TORCH:
            # Draw torch in hand
            torch_color = BLOCK_COLORS[BlockType.TORCH]
            handle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT - 140, 10, 80)
            pygame.draw.rect(screen, (101, 67, 33), handle_rect)
            pygame.draw.rect(screen, BLACK, handle_rect, 2)
            flame_rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 160, 30, 60)
            pygame.draw.rect(screen, (255, 255, 200), flame_rect)
            pygame.draw.rect(screen, (255, 165, 0), flame_rect, 2)
        else:
            # Draw hand
            hand_color = (255, 220, 177)
            hand_rect = pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 120, 40, 60)
            pygame.draw.rect(screen, hand_color, hand_rect)
            pygame.draw.rect(screen, BLACK, hand_rect, 2)
            
        # Draw crosshair (Minecraft style!)
        crosshair_size = 15
        pygame.draw.line(screen, WHITE, 
                     (SCREEN_WIDTH // 2 - crosshair_size, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 + crosshair_size, SCREEN_HEIGHT // 2), 2)
        pygame.draw.line(screen, WHITE,
                     (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - crosshair_size),
                     (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + crosshair_size), 2)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blocks = [[BlockType.AIR for _ in range(height)] for _ in range(width)]
        self.generate_world()
        
    def generate_world(self):
        # Generate terrain
        for x in range(self.width):
            # Generate height map
            height = int(10 + 5 * math.sin(x * 0.1) + random.randint(-2, 2))
            
            for y in range(self.height):
                if y >= self.height - height:
                    if y == self.height - height:
                        self.blocks[x][y] = BlockType.GRASS
                    else:
                        self.blocks[x][y] = BlockType.DIRT
                elif y >= self.height - height - 3:
                    self.blocks[x][y] = BlockType.STONE
                else:
                    self.blocks[x][y] = BlockType.AIR
                    
        # Add ores
        for _ in range(50):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 20)
            ore = random.choice([BlockType.COAL, BlockType.IRON, BlockType.GOLD, BlockType.DIAMOND])
            self.blocks[x][y] = ore
            
    def get_block_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.blocks[x][y]
        return BlockType.AIR
        
    def set_block_at(self, x, y, block_type):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.blocks[x][y] == BlockType.AIR:
                self.blocks[x][y] = block_type
                return True
        return False
        
    def remove_block_at(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            block = self.blocks[x][y]
            if block != BlockType.AIR:
                self.blocks[x][y] = BlockType.AIR
                return block
        return None
        
    def draw_3d(self, screen, camera_x, camera_y):
        # Calculate visible range
        start_x = max(0, camera_x // TILE_SIZE)
        end_x = min(self.width, (camera_x + SCREEN_WIDTH) // TILE_SIZE + 1)
        start_y = max(0, camera_y // TILE_SIZE)
        end_y = min(self.height, (camera_y + SCREEN_HEIGHT) // TILE_SIZE + 1)
        
        # Draw blocks with depth shading
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.blocks[x][y] != BlockType.AIR:
                    screen_x = x * TILE_SIZE - camera_x
                    screen_y = y * TILE_SIZE - camera_y
                    
                    # Calculate distance for shading
                    center_x = x * TILE_SIZE + TILE_SIZE // 2
                    center_y = y * TILE_SIZE + TILE_SIZE // 2
                    distance = math.sqrt((center_x - (camera_x + SCREEN_WIDTH // 2))**2 + 
                                       (center_y - (camera_y + SCREEN_HEIGHT // 2))**2)
                    
                    # Distance-based shading
                    base_color = BLOCK_COLORS[self.blocks[x][y]]
                    if distance > 200:
                        color = tuple(max(0, c - 80) for c in base_color[:3])
                    elif distance > 100:
                        color = tuple(max(0, c - 40) for c in base_color[:3])
                    else:
                        color = base_color
                    
                    # Draw block
                    block_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, block_rect)
                    
                    # 3D edges for nearby blocks
                    if distance < 150:
                        top_color = tuple(min(255, c + 50) for c in color[:3])
                        left_color = tuple(min(255, c + 30) for c in color[:3])
                        pygame.draw.line(screen, top_color, (screen_x, screen_y), (screen_x + TILE_SIZE, screen_y), 3)
                        pygame.draw.line(screen, left_color, (screen_x, screen_y), (screen_x, screen_y + TILE_SIZE), 3)
                        pygame.draw.rect(screen, tuple(max(0, c - 100) for c in color[:3]), block_rect, 1)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("REAL MINECRAFT JAVA EDITION - True Minecraft Experience!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Game objects
        self.world = World(100, 50)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Camera (first-person)
        self.camera_x = 0
        self.camera_y = 0
        
        # UI state
        self.show_inventory = False
        self.show_hotbar = True
        
        # Mouse state
        pygame.mouse.set_visible(False)  # Hide cursor for crosshair
        self.mouse_sensitivity = 0.5
        self.mouse_captured = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump(self)
                elif event.key == pygame.K_e:
                    self.show_inventory = not self.show_inventory
                elif event.key == pygame.K_TAB:
                    # Toggle mouse capture
                    self.mouse_captured = not self.mouse_captured
                    pygame.mouse.set_visible(not self.mouse_captured)
                    pygame.event.set_grab(self.mouse_captured)
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    # Hotbar selection
                    slot = event.key - pygame.K_1
                    if slot < len(self.player.hotbar):
                        self.player.selected_slot = slot
                        self.player.selected_block = self.player.hotbar[slot]
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_captured:
                    if event.button == 1:  # Left click - mine/place
                        # Get block at crosshair
                        world_x = int((self.camera_x + SCREEN_WIDTH // 2) // TILE_SIZE)
                        world_y = int((self.camera_y + SCREEN_HEIGHT // 2) // TILE_SIZE)
                        
                        if event.button == 1:  # Left click - mine
                            block = self.world.remove_block_at(world_x, world_y)
                            if block:
                                self.player.inventory[block] += 1
                                
                    elif event.button == 3:  # Right click - place
                        world_x = int((self.camera_x + SCREEN_WIDTH // 2) // TILE_SIZE)
                        world_y = int((self.camera_y + SCREEN_HEIGHT // 2) // TILE_SIZE)
                        
                        if self.world.set_block_at(world_x, world_y, self.player.selected_block):
                            self.player.inventory[self.player.selected_block] -= 1
                            
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_captured:
                    # Mouse look (Minecraft-style!)
                    rel_x, rel_y = event.rel
                    self.player.yaw += rel_x * self.mouse_sensitivity
                    self.player.pitch -= rel_y * self.mouse_sensitivity
                    
                    # Clamp pitch
                    self.player.pitch = max(-89, min(89, self.player.pitch))
                    
    def update_camera(self):
        # First-person camera - always centered
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Keep in bounds
        self.camera_x = max(0, min(self.camera_x, self.world.width * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world.height * TILE_SIZE - SCREEN_HEIGHT))
        
    def draw_sky(self):
        # Simple sky gradient
        for y in range(SCREEN_HEIGHT // 2):
            color_value = int(135 + 120 * (y / (SCREEN_HEIGHT // 2)))
            color = (color_value, 206, 235)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
    def draw_ui(self):
        if self.show_hotbar:
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
                        
        # Inventory
        if self.show_inventory:
            inv_width = 600
            inv_height = 400
            inv_x = SCREEN_WIDTH // 2 - inv_width // 2
            inv_y = SCREEN_HEIGHT // 2 - inv_height // 2
            
            # Background
            inv_rect = pygame.Rect(inv_x, inv_y, inv_width, inv_height)
            pygame.draw.rect(self.screen, (40, 40, 40), inv_rect)
            pygame.draw.rect(self.screen, WHITE, inv_rect, 3)
            
            # Title
            title_text = self.big_font.render("INVENTORY", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, inv_y + 30))
            self.screen.blit(title_text, title_rect)
            
            # Items
            y_offset = inv_y + 80
            for i, (block_type, count) in enumerate(self.player.inventory.items()):
                if count > 0:
                    name = block_type.name.replace('_', ' ').title()
                    item_text = self.font.render(f"{name}: {count}", True, WHITE)
                    self.screen.blit(item_text, (inv_x + 20, y_offset + i * 30))
                    
        # Controls help
        controls = [
            "WASD/Arrows: Move | Space: Jump",
            "Mouse: Look Around (TAB to capture)",
            "Left Click: Mine | Right Click: Place",
            "1-9: Hotbar | E: Inventory | ESC: Quit"
        ]
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, WHITE)
            self.screen.blit(control_text, (10, 10 + i * 25))
            
        # Mouse capture status
        if self.mouse_captured:
            capture_text = self.font.render("MOUSE CAPTURED - Use TAB to release", True, GREEN)
        else:
            capture_text = self.font.render("MOUSE FREE - Press TAB to capture", True, YELLOW)
        self.screen.blit(capture_text, (10, SCREEN_HEIGHT - 30))
        
    def run(self):
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update
            keys = pygame.key.get_pressed()
            self.player.update(self.world, keys)
            self.update_camera()
            
            # Draw
            self.draw_sky()
            self.world.draw_3d(self.screen, self.camera_x, self.camera_y)
            self.player.draw_first_person(self.screen)
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
