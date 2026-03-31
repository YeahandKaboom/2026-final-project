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

class RubyHill:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ruby_deposits = []
        self.ruby_particles = []
        self.generate_ruby_hill()
        
    def generate_ruby_hill(self):
        """Generate ruby deposits on the hill"""
        # Create ruby deposits all over the hill
        for _ in range(random.randint(20, 40)):
            ruby_x = self.x + random.randint(-80, 80)
            ruby_y = self.y + random.randint(-40, 40)
            
            self.ruby_deposits.append({
                "x": ruby_x,
                "y": ruby_y,
                "size": random.randint(5, 15),
                "value": random.randint(100, 500),
                "sparkle_timer": random.randint(0, 60)
            })
            
    def update(self):
        """Update ruby hill effects"""
        # Update ruby sparkles
        for ruby in self.ruby_deposits:
            ruby["sparkle_timer"] = (ruby["sparkle_timer"] + 1) % 60
            
            # Create sparkle particles
            if ruby["sparkle_timer"] == 0:
                self.ruby_particles.append({
                    "x": ruby["x"] + random.randint(-10, 10),
                    "y": ruby["y"] + random.randint(-10, 10),
                    "vx": random.uniform(-2, 2),
                    "vy": random.uniform(-3, -1),
                    "life": 30,
                    "color": random.choice([RUBY_RED, (255, 100, 100), (255, 200, 200)])
                })
                
        # Update particles
        for particle in self.ruby_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.2  # Gravity
            particle["life"] -= 1
            
            if particle["life"] <= 0:
                self.ruby_particles.remove(particle)
                
    def draw(self, screen, camera_x, camera_y):
        """Draw the ruby hill"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if -150 < draw_x < SCREEN_WIDTH + 150 and -150 < draw_y < SCREEN_HEIGHT + 150:
            # Draw hill base (ruby-colored)
            pygame.draw.ellipse(screen, (178, 34, 34), (draw_x - 100, draw_y - 50, 200, 100))
            pygame.draw.ellipse(screen, (220, 20, 60), (draw_x - 80, draw_y - 40, 160, 80))
            
            # Draw ruby deposits
            for ruby in self.ruby_deposits:
                ruby_draw_x = ruby["x"] - camera_x
                ruby_draw_y = ruby["y"] - camera_y
                
                # Sparkle effect
                if ruby["sparkle_timer"] < 10:
                    sparkle_size = ruby["size"] + 5
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (int(ruby_draw_x), int(ruby_draw_y)), sparkle_size)
                    
                # Ruby deposit
                pygame.draw.circle(screen, RUBY_RED, 
                                 (int(ruby_draw_x), int(ruby_draw_y)), ruby["size"])
                pygame.draw.circle(screen, (255, 100, 100), 
                                 (int(ruby_draw_x), int(ruby_draw_y)), ruby["size"] - 2)
                                 
            # Draw particles
            for particle in self.ruby_particles:
                particle_draw_x = particle["x"] - camera_x
                particle_draw_y = particle["y"] - camera_y
                
                alpha = particle["life"] / 30
                size = int(3 * alpha)
                if size > 0:
                    pygame.draw.circle(screen, particle["color"], 
                                     (int(particle_draw_x), int(particle_draw_y)), size)

class BitcoinMine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bitcoin_nodes = []
        self.mining_lasers = []
        self.crypto_particles = []
        self.generate_bitcoin_mine()
        
    def generate_bitcoin_mine(self):
        """Generate Bitcoin mining operation"""
        # Create Bitcoin mining nodes
        for _ in range(random.randint(8, 15)):
            node_x = self.x + random.randint(-100, 100)
            node_y = self.y + random.randint(-60, 60)
            
            self.bitcoin_nodes.append({
                "x": node_x,
                "y": node_y,
                "active": True,
                "hash_rate": random.randint(100, 1000),
                "timer": random.randint(0, 120)
            })
            
    def update(self):
        """Update Bitcoin mining operation"""
        # Update mining nodes
        for node in self.bitcoin_nodes:
            if node["active"]:
                node["timer"] = (node["timer"] + 1) % 120
                
                # Generate mining laser
                if node["timer"] == 0:
                    self.mining_lasers.append({
                        "x": node["x"],
                        "y": node["y"],
                        "target_x": node["x"] + random.randint(-50, 50),
                        "target_y": node["y"] + random.randint(-50, 50),
                        "life": 30
                    })
                    
                # Generate crypto particles
                if random.random() < 0.1:
                    self.crypto_particles.append({
                        "x": node["x"] + random.randint(-20, 20),
                        "y": node["y"] + random.randint(-20, 20),
                        "vx": random.uniform(-1, 1),
                        "vy": random.uniform(-2, 0),
                        "life": 60,
                        "symbol": "₿"
                    })
                    
        # Update lasers
        for laser in self.mining_lasers[:]:
            laser["life"] -= 1
            if laser["life"] <= 0:
                self.mining_lasers.remove(laser)
                
        # Update particles
        for particle in self.crypto_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1
            particle["life"] -= 1
            
            if particle["life"] <= 0:
                self.crypto_particles.remove(particle)
                
    def draw(self, screen, camera_x, camera_y):
        """Draw the Bitcoin mine"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if -200 < draw_x < SCREEN_WIDTH + 200 and -200 < draw_y < SCREEN_HEIGHT + 200:
            # Draw mine base
            pygame.draw.rect(screen, BITCOIN_ORANGE, (draw_x - 120, draw_y - 80, 240, 160))
            pygame.draw.rect(screen, BITCOIN_GOLD, (draw_x - 100, draw_y - 60, 200, 120))
            
            # Draw Bitcoin logo
            font_large = pygame.font.Font(None, 48)
            bitcoin_text = font_large.render("₿", True, WHITE)
            screen.blit(bitcoin_text, (draw_x - 20, draw_y - 30))
            
            # Draw mining nodes
            for node in self.bitcoin_nodes:
                node_draw_x = node["x"] - camera_x
                node_draw_y = node["y"] - camera_y
                
                # Node base
                color = BITCOIN_GOLD if node["active"] else (100, 100, 100)
                pygame.draw.rect(screen, color, (node_draw_x - 15, node_draw_y - 15, 30, 30))
                pygame.draw.rect(screen, BLACK, (node_draw_x - 15, node_draw_y - 15, 30, 30), 2)
                
                # Bitcoin symbol
                font = pygame.font.Font(None, 20)
                btc_text = font.render("₿", True, WHITE)
                screen.blit(btc_text, (node_draw_x - 8, node_draw_y - 10))
                
                # Activity indicator
                if node["active"] and node["timer"] < 20:
                    pygame.draw.circle(screen, (255, 255, 0), 
                                     (int(node_draw_x + 20), int(node_draw_y - 20)), 5)
                    
            # Draw mining lasers
            for laser in self.mining_lasers:
                laser_start_x = laser["x"] - camera_x
                laser_start_y = laser["y"] - camera_y
                laser_end_x = laser["target_x"] - camera_x
                laser_end_y = laser["target_y"] - camera_y
                
                alpha = laser["life"] / 30
                color = (int(255 * alpha), int(203 * alpha), int(0 * alpha))
                pygame.draw.line(screen, color, 
                               (laser_start_x, laser_start_y), 
                               (laser_end_x, laser_end_y), 2)
                               
            # Draw crypto particles
            for particle in self.crypto_particles:
                particle_draw_x = particle["x"] - camera_x
                particle_draw_y = particle["y"] - camera_y
                
                alpha = particle["life"] / 60
                color = (int(247 * alpha), int(147 * alpha), int(26 * alpha))
                
                font = pygame.font.Font(None, 16)
                crypto_text = font.render(particle["symbol"], True, color)
                screen.blit(crypto_text, (int(particle_draw_x), int(particle_draw_y)))

print("FUN VILLAGES, RUBY HILLS, AND BITCOIN MINES loaded!")
