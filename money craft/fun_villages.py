# FUN VILLAGES AND RUBY HILLS SYSTEM!
import pygame
import random
import math
from enum import Enum

# Import colors from main game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
RUBY_RED = (220, 20, 60)
EMERALD_GREEN = (0, 100, 0)
DIAMOND_BLUE = (185, 242, 255)
SAPPHIRE_BLUE = (15, 82, 186)
AMETHYST_PURPLE = (153, 102, 204)
CRYSTAL_WHITE = (255, 255, 255)
BITCOIN_ORANGE = (247, 147, 26)
BITCOIN_GOLD = (255, 203, 0)
LIME = (50, 205, 50)
GOLD = (255, 215, 0)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
MOUNTAIN_BROWN = (139, 90, 43)
WATER_BLUE = (64, 164, 223)

# Screen settings for drawing
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

class VillageType(Enum):
    FUN_VILLAGE = 0
    RUBY_VILLAGE = 1
    BITCOIN_VILLAGE = 2
    CRYSTAL_VILLAGE = 3
    DRAGON_VILLAGE = 4
    RAINBOW_VILLAGE = 5

class Village:
    def __init__(self, x, y, village_type):
        self.x = x
        self.y = y
        self.type = village_type
        self.houses = []
        self.villagers = []
        self.shops = []
        self.decorations = []
        self.generate_village()
        
    def generate_village(self):
        """Generate village buildings and features"""
        village_colors = {
            VillageType.FUN_VILLAGE: [(255, 255, 0), (255, 165, 0), (255, 192, 203)],  # Bright fun colors
            VillageType.RUBY_VILLAGE: [(220, 20, 60), (255, 69, 0), (178, 34, 34)],  # Ruby reds
            VillageType.BITCOIN_VILLAGE: [(247, 147, 26), (255, 203, 0), (255, 215, 0)],  # Bitcoin golds
            VillageType.CRYSTAL_VILLAGE: [(255, 255, 255), (230, 230, 250), (176, 224, 230)],  # Crystal whites
            VillageType.DRAGON_VILLAGE: [(139, 69, 19), (160, 82, 45), (205, 133, 63)],  # Dragon browns
            VillageType.RAINBOW_VILLAGE: [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130)]  # Rainbow!
        }
        
        colors = village_colors[self.type]
        
        # Generate houses
        num_houses = random.randint(5, 12)
        for i in range(num_houses):
            house_x = self.x + random.randint(-60, 60)
            house_y = self.y + random.randint(-30, 30)
            house_color = random.choice(colors)
            
            self.houses.append({
                "x": house_x,
                "y": house_y,
                "width": random.randint(3, 5) * 40,
                "height": random.randint(4, 7) * 40,
                "color": house_color,
                "roof_color": random.choice([(255, 0, 0), (139, 69, 19), (0, 128, 0)]),
                "has_lights": random.random() < 0.7
            })
            
        # Generate shops
        num_shops = random.randint(2, 4)
        for i in range(num_shops):
            shop_x = self.x + random.randint(-50, 50)
            shop_y = self.y + random.randint(-20, 20)
            
            self.shops.append({
                "x": shop_x,
                "y": shop_y,
                "type": random.choice(["general", "gems", "tools", "food", "magic"]),
                "color": random.choice(colors)
            })
            
        # Generate villagers
        num_villagers = random.randint(8, 20)
        for i in range(num_villagers):
            villager_x = self.x + random.randint(-80, 80)
            villager_y = self.y + random.randint(-40, 40)
            
            self.villagers.append({
                "x": villager_x,
                "y": villager_y,
                "color": random.choice([(255, 220, 177), (139, 69, 19), (255, 192, 203)]),
                "speed": random.uniform(0.5, 2.0),
                "direction": random.uniform(0, 2 * math.pi),
                "personality": random.choice(["happy", "grumpy", "excited", "sleepy", "dancing"])
            })
            
        # Generate decorations
        num_decorations = random.randint(10, 25)
        for i in range(num_decorations):
            deco_x = self.x + random.randint(-100, 100)
            deco_y = self.y + random.randint(-50, 50)
            
            self.decorations.append({
                "x": deco_x,
                "y": deco_y,
                "type": random.choice(["tree", "fountain", "statue", "flower", "lamp", "banner"]),
                "color": random.choice(colors)
            })
            
    def update(self):
        """Update village animations and villagers"""
        # Update villagers
        for villager in self.villagers:
            # Random movement
            villager["direction"] += random.uniform(-0.2, 0.2)
            villager["x"] += math.cos(villager["direction"]) * villager["speed"]
            villager["y"] += math.sin(villager["direction"]) * villager["speed"] * 0.5
            
            # Keep villagers near village
            if abs(villager["x"] - self.x) > 100:
                villager["direction"] = math.atan2(self.y - villager["y"], self.x - villager["x"])
            if abs(villager["y"] - self.y) > 60:
                villager["direction"] = math.atan2(self.y - villager["y"], self.x - villager["x"])
                
    def draw(self, screen, camera_x, camera_y):
        """Draw the village"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if -200 < draw_x < SCREEN_WIDTH + 200 and -200 < draw_y < SCREEN_HEIGHT + 200:
            # Draw decorations first (background)
            for deco in self.decorations:
                self.draw_decoration(screen, deco, camera_x, camera_y)
                
            # Draw houses
            for house in self.houses:
                self.draw_house(screen, house, camera_x, camera_y)
                
            # Draw shops
            for shop in self.shops:
                self.draw_shop(screen, shop, camera_x, camera_y)
                
            # Draw villagers
            for villager in self.villagers:
                self.draw_villager(screen, villager, camera_x, camera_y)
                
    def draw_house(self, screen, house, camera_x, camera_y):
        """Draw a house"""
        draw_x = house["x"] - camera_x
        draw_y = house["y"] - camera_y
        
        if -100 < draw_x < SCREEN_WIDTH + 100 and -100 < draw_y < SCREEN_HEIGHT + 100:
            # House walls
            pygame.draw.rect(screen, house["color"], (draw_x, draw_y, house["width"], house["height"]))
            pygame.draw.rect(screen, BLACK, (draw_x, draw_y, house["width"], house["height"]), 2)
            
            # Roof
            roof_points = [
                (draw_x - 10, draw_y),
                (draw_x + house["width"] // 2, draw_y - house["height"] // 3),
                (draw_x + house["width"] + 10, draw_y)
            ]
            pygame.draw.polygon(screen, house["roof_color"], roof_points)
            
            # Door
            door_width = 20
            door_height = 30
            door_x = draw_x + house["width"] // 2 - door_width // 2
            door_y = draw_y + house["height"] - door_height
            pygame.draw.rect(screen, (101, 67, 33), (door_x, door_y, door_width, door_height))
            
            # Windows
            if house["has_lights"]:
                window_color = (255, 255, 200)  # Warm light
            else:
                window_color = (135, 206, 235)  # Dark blue
                
            # Left window
            pygame.draw.rect(screen, window_color, (draw_x + 10, draw_y + 20, 15, 15))
            # Right window
            pygame.draw.rect(screen, window_color, (draw_x + house["width"] - 25, draw_y + 20, 15, 15))
            
    def draw_shop(self, screen, shop, camera_x, camera_y):
        """Draw a shop"""
        draw_x = shop["x"] - camera_x
        draw_y = shop["y"] - camera_y
        
        if -60 < draw_x < SCREEN_WIDTH + 60 and -60 < draw_y < SCREEN_HEIGHT + 60:
            # Shop building
            pygame.draw.rect(screen, shop["color"], (draw_x, draw_y, 120, 80))
            pygame.draw.rect(screen, BLACK, (draw_x, draw_y, 120, 80), 3)
            
            # Shop sign
            sign_colors = {
                "general": (255, 255, 0),
                "gems": (185, 242, 255),
                "tools": (139, 69, 19),
                "food": (255, 165, 0),
                "magic": (148, 0, 211)
            }
            sign_color = sign_colors.get(shop["type"], WHITE)
            
            pygame.draw.rect(screen, sign_color, (draw_x + 20, draw_y - 20, 80, 20))
            pygame.draw.rect(screen, BLACK, (draw_x + 20, draw_y - 20, 80, 20), 2)
            
            # Shop text
            font = pygame.font.Font(None, 16)
            text = font.render(shop["type"].upper(), True, BLACK)
            screen.blit(text, (draw_x + 25, draw_y - 17))
            
            # Open sign
            pygame.draw.rect(screen, GREEN, (draw_x + 45, draw_y + 60, 30, 15))
            font_small = pygame.font.Font(None, 12)
            open_text = font_small.render("OPEN", True, WHITE)
            screen.blit(open_text, (draw_x + 50, draw_y + 62))
            
    def draw_villager(self, screen, villager, camera_x, camera_y):
        """Draw a villager"""
        draw_x = villager["x"] - camera_x
        draw_y = villager["y"] - camera_y
        
        if -20 < draw_x < SCREEN_WIDTH + 20 and -20 < draw_y < SCREEN_HEIGHT + 20:
            # Body
            pygame.draw.ellipse(screen, villager["color"], (draw_x - 8, draw_y - 15, 16, 20))
            
            # Head
            pygame.draw.circle(screen, (255, 220, 177), (int(draw_x), int(draw_y - 20)), 8)
            
            # Personality-based features
            if villager["personality"] == "happy":
                # Smile
                pygame.draw.arc(screen, BLACK, (draw_x - 4, draw_y - 22, 8, 8), 0, math.pi, 2)
            elif villager["personality"] == "dancing":
                # Arms up
                pygame.draw.line(screen, villager["color"], (draw_x - 8, draw_y - 10), (draw_x - 15, draw_y - 20), 3)
                pygame.draw.line(screen, villager["color"], (draw_x + 8, draw_y - 10), (draw_x + 15, draw_y - 20), 3)
            elif villager["personality"] == "excited":
                # Jumping effect
                draw_y -= 5
                pygame.draw.circle(screen, YELLOW, (int(draw_x), int(draw_y - 25)), 3)
                
    def draw_decoration(self, screen, deco, camera_x, camera_y):
        """Draw village decoration"""
        draw_x = deco["x"] - camera_x
        draw_y = deco["y"] - camera_y
        
        if -30 < draw_x < SCREEN_WIDTH + 30 and -30 < draw_y < SCREEN_HEIGHT + 30:
            if deco["type"] == "tree":
                # Tree trunk
                pygame.draw.rect(screen, (139, 69, 19), (draw_x - 5, draw_y - 20, 10, 20))
                # Tree leaves
                pygame.draw.circle(screen, (34, 139, 34), (int(draw_x), int(draw_y - 25)), 15)
                
            elif deco["type"] == "fountain":
                # Fountain base
                pygame.draw.circle(screen, (135, 206, 235), (int(draw_x), int(draw_y)), 20)
                pygame.draw.circle(screen, WHITE, (int(draw_x), int(draw_y)), 15)
                # Water spout
                pygame.draw.rect(screen, (135, 206, 235), (draw_x - 2, draw_y - 10, 4, 10))
                
            elif deco["type"] == "statue":
                # Statue base
                pygame.draw.rect(screen, (128, 128, 128), (draw_x - 8, draw_y - 5, 16, 5))
                # Statue figure
                pygame.draw.ellipse(screen, (192, 192, 192), (draw_x - 5, draw_y - 20, 10, 15))
                
            elif deco["type"] == "flower":
                # Stem
                pygame.draw.line(screen, (34, 139, 34), (draw_x, draw_y), (draw_x, draw_y - 10), 2)
                # Flower
                pygame.draw.circle(screen, deco["color"], (int(draw_x), int(draw_y - 12)), 5)
                
            elif deco["type"] == "lamp":
                # Lamp post
                pygame.draw.rect(screen, (64, 64, 64), (draw_x - 2, draw_y - 25, 4, 25))
                # Lamp
                pygame.draw.circle(screen, (255, 255, 200), (int(draw_x), int(draw_y - 25)), 8)
                
            elif deco["type"] == "banner":
                # Banner pole
                pygame.draw.rect(screen, (139, 69, 19), (draw_x - 1, draw_y - 30, 2, 30))
                # Banner
                pygame.draw.polygon(screen, deco["color"], [
                    (draw_x + 1, draw_y - 30),
                    (draw_x + 20, draw_y - 25),
                    (draw_x + 20, draw_y - 15),
                    (draw_x + 1, draw_y - 20)
                ])

import pygame
import random
import math

from ultimate_world_generation import RAINBOW_COLORS

class Villager:
    def __init__(self, x, y, job):
        self.x = x
        self.y = y
        self.job = job  # "toolmaker", "farmer", "miner", "trader", "baker"
        self.animation_frame = 0
        self.direction = random.choice(["left", "right", "up", "down"])
        self.working = True
        self.product = None
        self.work_progress = 0
        
        # Job-specific colors
        self.job_colors = {
            "toolmaker": (139, 69, 19),  # Brown
            "farmer": (34, 139, 34),      # Green
            "miner": (105, 105, 105),      # Gray
            "trader": (255, 215, 0),       # Gold
            "baker": (255, 182, 193)       # Pink
        }
        
    def update(self):
        """Update villager animation and work"""
        self.animation_frame += 1
        
        # Work animation
        if self.working:
            self.work_progress += 2
            
            # Create products based on job
            if self.work_progress >= 100:
                self.create_product()
                self.work_progress = 0
                
        # Random movement
        if random.random() < 0.02:
            self.direction = random.choice(["left", "right", "up", "down"])
            
        # Move slightly
        if self.animation_frame % 30 == 0:
            if self.direction == "left":
                self.x -= 5
            elif self.direction == "right":
                self.x += 5
            elif self.direction == "up":
                self.y -= 5
            elif self.direction == "down":
                self.y += 5
                
    def create_product(self):
        """Create product based on job"""
        products = {
            "toolmaker": ["pickaxe", "sword", "hammer", "axe"],
            "farmer": ["bread", "wheat", "vegetables", "fruit"],
            "miner": ["coal", "iron", "copper", "stone"],
            "trader": ["coins", "gems", "rare_items", "maps"],
            "baker": ["bread", "cake", "pie", "cookies"]
        }
        
        job_products = products.get(self.job, ["item"])
        self.product = random.choice(job_products)
        
    def draw(self, screen, camera_x, camera_y):
        """Draw animated villager"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if -50 < draw_x < SCREEN_WIDTH + 50 and -50 < draw_y < SCREEN_HEIGHT + 50:
            color = self.job_colors.get(self.job, WHITE)
            
            # Draw body
            pygame.draw.circle(screen, color, (int(draw_x), int(draw_y)), 8)
            
            # Draw head
            pygame.draw.circle(screen, (255, 220, 177), (int(draw_x), int(draw_y - 12)), 5)
            
            # Draw work indicator
            if self.working:
                # Work animation
                work_offset = math.sin(self.animation_frame * 0.1) * 3
                pygame.draw.circle(screen, (255, 255, 0), 
                               (int(draw_x + 15), int(draw_y + work_offset)), 3)
                
                # Progress bar
                bar_width = 20
                bar_height = 4
                progress = self.work_progress / 100
                
                pygame.draw.rect(screen, (100, 100, 100), 
                               (draw_x - 10, draw_y - 25, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), 
                               (draw_x - 10, draw_y - 25, int(bar_width * progress), bar_height))
                
            # Draw product if available
            if self.product:
                pygame.draw.circle(screen, (255, 215, 0), 
                               (int(draw_x + 10), int(draw_y - 20)), 4)
                
                # Product label
                font = pygame.font.Font(None, 12)
                text = font.render(self.product[:3], True, BLACK)
                screen.blit(text, (draw_x + 5, draw_y - 35))

class Village:
    def __init__(self, x, y, village_type="normal"):
        self.x = x
        self.y = y
        self.type = village_type
        self.villagers = []
        self.buildings = []
        self.resources = {
            "wood": 100,
            "stone": 50,
            "food": 75,
            "tools": 20,
            "gems": 5
        }
        
        # Create village buildings
        self.create_buildings()
        
        # Create villagers with different jobs
        self.create_villagers()
        
    def create_buildings(self):
        """Create village buildings"""
        building_types = [
            {"type": "house", "color": (139, 69, 19), "size": (40, 40)},
            {"type": "workshop", "color": (105, 105, 105), "size": (50, 35)},
            {"type": "farm", "color": (34, 139, 34), "size": (60, 45)},
            {"type": "market", "color": (255, 215, 0), "size": (45, 40)},
            {"type": "bakery", "color": (255, 182, 193), "size": (35, 35)}
        ]
        
        for i, building in enumerate(building_types):
            building_x = self.x + (i % 3) * 60
            building_y = self.y + (i // 3) * 50
            
            self.buildings.append({
                "x": building_x,
                "y": building_y,
                "type": building["type"],
                "color": building["color"],
                "size": building["size"]
            })
            
    def create_villagers(self):
        """Create villagers with different jobs"""
        jobs = ["toolmaker", "farmer", "miner", "trader", "baker"]
        
        for i in range(8):  # 8 villagers per village
            villager_x = self.x + random.randint(-40, 60)
            villager_y = self.y + random.randint(-30, 50)
            job = random.choice(jobs)
            
            self.villagers.append(Villager(villager_x, villager_y, job))
            
    def update(self):
        """Update all villagers and village"""
        for villager in self.villagers:
            villager.update()
            
            # Collect products from villagers
            if villager.product:
                self.collect_product(villager)
                
        # Update resources
        if random.random() < 0.1:
            self.resources["food"] += 1
            self.resources["wood"] += random.randint(0, 2)
            
    def collect_product(self, villager):
        """Collect product from villager"""
        if villager.product == "bread" or villager.product == "cake":
            self.resources["food"] += 5
        elif villager.product == "pickaxe" or villager.product == "sword":
            self.resources["tools"] += 1
        elif villager.product == "coal" or villager.product == "iron":
            self.resources["stone"] += 3
        elif villager.product == "gems":
            self.resources["gems"] += 1
            
        villager.product = None
        
    def draw(self, screen, camera_x, camera_y):
        """Draw village with buildings and villagers"""
        # Draw buildings
        for building in self.buildings:
            draw_x = building["x"] - camera_x
            draw_y = building["y"] - camera_y
            
            if -100 < draw_x < SCREEN_WIDTH + 100 and -100 < draw_y < SCREEN_HEIGHT + 100:
                # Building base
                pygame.draw.rect(screen, building["color"], 
                               (draw_x, draw_y, building["size"][0], building["size"][1]))
                
                # Building roof
                roof_color = tuple(max(0, c - 30) for c in building["color"])
                pygame.draw.polygon(screen, roof_color, [
                    (draw_x - 5, draw_y),
                    (draw_x + building["size"][0] // 2, draw_y - 20),
                    (draw_x + building["size"][0] + 5, draw_y)
                ])
                
                # Building label
                font = pygame.font.Font(None, 16)
                text = font.render(building["type"][:4], True, WHITE)
                screen.blit(text, (draw_x + 5, draw_y + 5))
                
        # Draw villagers
        for villager in self.villagers:
            villager.draw(screen, camera_x, camera_y)
            
        # Draw village resources
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y - 60
        
        if -100 < draw_x < SCREEN_WIDTH + 100 and -100 < draw_y < SCREEN_HEIGHT + 100:
            font = pygame.font.Font(None, 18)
            
            # Resource display
            resources_text = f"🏘️ Village Resources:"
            text = font.render(resources_text, True, WHITE)
            screen.blit(text, (draw_x, draw_y))
            
            # Individual resources
            for i, (resource, amount) in enumerate(self.resources.items()):
                resource_text = f"{resource}: {amount}"
                text = font.render(resource_text, True, (255, 255, 0))
                screen.blit(text, (draw_x, draw_y + 20 + i * 18))

class RubyHill:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ruby_deposits = []
        self.sparkles = []
        
        # Create ruby deposits
        for _ in range(15):
            ruby_x = x + random.randint(-30, 30)
            ruby_y = y + random.randint(-20, 20)
            self.ruby_deposits.append({
                "x": ruby_x,
                "y": ruby_y,
                "size": random.randint(3, 8),
                "value": random.randint(50, 200)
            })
            
    def update(self):
        """Update sparkles"""
        # Add new sparkles
        if random.random() < 0.3:
            deposit = random.choice(self.ruby_deposits)
            self.sparkles.append({
                "x": deposit["x"] + random.randint(-10, 10),
                "y": deposit["y"] + random.randint(-10, 10),
                "life": 30
            })
            
        # Update existing sparkles
        self.sparkles = [s for s in self.sparkles if s["life"] > 0]
        for sparkle in self.sparkles:
            sparkle["life"] -= 1
            sparkle["y"] -= 1
            
    def draw(self, screen, camera_x, camera_y):
        """Draw ruby hill with sparkles"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if -100 < draw_x < SCREEN_WIDTH + 100 and -100 < draw_y < SCREEN_HEIGHT + 100:
            # Draw hill
            pygame.draw.ellipse(screen, (139, 69, 19), 
                             (draw_x - 40, draw_y - 20, 80, 40))
            pygame.draw.ellipse(screen, (220, 20, 60), 
                             (draw_x - 35, draw_y - 15, 70, 30))
            
            # Draw ruby deposits
            for deposit in self.ruby_deposits:
                ruby_x = deposit["x"] - camera_x
                ruby_y = deposit["y"] - camera_y
                pygame.draw.circle(screen, (220, 20, 60), 
                               (int(ruby_x), int(ruby_y)), deposit["size"])
                pygame.draw.circle(screen, (255, 100, 100), 
                               (int(ruby_x), int(ruby_y)), deposit["size"] - 2)
                
            # Draw sparkles
            for sparkle in self.sparkles:
                sparkle_x = sparkle["x"] - camera_x
                sparkle_y = sparkle["y"] - camera_y
                alpha = sparkle["life"] / 30
                size = int(3 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, (255, 255, 255), 
                                   (int(sparkle_x), int(sparkle_y)), size)

class BitcoinMine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mining_nodes = []
        self.lasers = []
        self.crypto_particles = []
        
        # Create mining nodes
        for _ in range(8):
            node_x = x + random.randint(-40, 40)
            node_y = y + random.randint(-30, 30)
            self.mining_nodes.append({
                "x": node_x,
                "y": node_y,
                "power": random.randint(50, 100),
                "bitcoin_rate": random.uniform(0.1, 0.5)
            })
            
    def update(self):
        """Update mining operations"""
        # Add crypto particles
        if random.random() < 0.4:
            node = random.choice(self.mining_nodes)
            self.crypto_particles.append({
                "x": node["x"] + random.randint(-15, 15),
                "y": node["y"] + random.randint(-15, 15),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-2, 2),
                "life": 60
            })
            
        # Update particles
        self.crypto_particles = [p for p in self.crypto_particles if p["life"] > 0]
        for particle in self.crypto_particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            
    def draw(self, screen, camera_x, camera_y):
        """Draw bitcoin mine with crypto effects"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if -100 < draw_x < SCREEN_WIDTH + 100 and -100 < draw_y < SCREEN_HEIGHT + 100:
            # Draw mine building
            pygame.draw.rect(screen, (247, 147, 26), 
                           (draw_x - 50, draw_y - 30, 100, 60))
            pygame.draw.rect(screen, (255, 215, 0), 
                           (draw_x - 50, draw_y - 30, 100, 60), 3)
            
            # Draw mining nodes
            for node in self.mining_nodes:
                node_x = node["x"] - camera_x
                node_y = node["y"] - camera_y
                
                # Node base
                pygame.draw.circle(screen, (105, 105, 105), 
                               (int(node_x), int(node_y)), 8)
                pygame.draw.circle(screen, (255, 215, 0), 
                               (int(node_x), int(node_y)), 6)
                
                # Power indicator
                power_color = (0, 255, 0) if node["power"] > 75 else (255, 255, 0)
                pygame.draw.circle(screen, power_color, 
                               (int(node_x), int(node_y - 15)), 3)
                
            # Draw crypto particles
            for particle in self.crypto_particles:
                particle_x = particle["x"] - camera_x
                particle_y = particle["y"] - camera_y
                alpha = particle["life"] / 60
                size = int(4 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, (255, 215, 0), 
                                   (int(particle_x), int(particle_y)), size)
                    
            # Bitcoin logo
            font = pygame.font.Font(None, 36)
            btc_text = font.render("₿", True, (0, 0, 0))
            screen.blit(btc_text, (draw_x - 10, draw_y - 10))

# Screen dimensions for drawing
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
RUBY_RED = (220, 20, 60)
EMERALD_GREEN = (0, 100, 0)
DIAMOND_BLUE = (185, 242, 255)
SAPPHIRE_BLUE = (15, 82, 186)
AMETHYST_PURPLE = (153, 102, 204)
CRYSTAL_WHITE = (255, 255, 255)
BITCOIN_ORANGE = (247, 147, 26)
BITCOIN_GOLD = (255, 203, 0)
GOLD = (255, 215, 0)
LIME = (50, 205, 50)
GRASS_GREEN = (34, 139, 34)
MOUNTAIN_BROWN = (139, 90, 43)
WATER_BLUE = (64, 164, 223)
SNOW_WHITE = (255, 250, 250)
SWAMP_GREEN = (85, 107, 47)
MYSTICAL_PURPLE = (147, 112, 219)
CRYSTAL_PINK = (255, 182, 193)
VOLCANO_RED = (178, 34, 34)
LAVA_GLOW = (255, 69, 0)
DESERT_SAND = (238, 203, 173)
OCEAN_DEEP = (0, 119, 190)
FOREST_DARK = (34, 100, 34)
CAVE_DARK = (47, 47, 47)
ICE_BLUE = (176, 224, 230)
COSMIC_PURPLE = (75, 0, 130)
DRAGON_SCALE = (139, 69, 19)
RAINBOW_GOLD = (255, 215, 0)
UNDERWORLD_FIRE = (255, 69, 0)
SKY_ISLAND_BLUE = (173, 216, 230)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

print("🏘️ FUN VILLAGES WITH WORKING VILLAGERS loaded! - Making tools, food, etc! 🛠️🍞⛏️")
