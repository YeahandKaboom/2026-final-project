# Simplified Game Enhancement Module
import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.health = 50
        self.max_health = 50
        self.damage = 5
        self.speed = 1
        self.animation_frame = 0
        self.direction = random.choice([-1, 1])
        
        # Enemy properties
        self.properties = {
            "goblin": {"color": (100, 200, 100), "health": 30, "damage": 5, "speed": 2, "reward": 50},
            "rock_monster": {"color": (150, 150, 150), "health": 100, "damage": 10, "speed": 0.5, "reward": 100},
            "creeper": {"color": (0, 255, 0), "health": 40, "damage": 15, "speed": 1.5, "reward": 75},
            "dragon": {"color": (255, 100, 0), "health": 200, "damage": 25, "speed": 1, "reward": 500},
            "ghost": {"color": (200, 200, 255), "health": 25, "damage": 8, "speed": 3, "reward": 60},
            "spider": {"color": (50, 0, 50), "health": 35, "damage": 7, "speed": 2.5, "reward": 65}
        }
        
        props = self.properties[enemy_type]
        self.health = props["health"]
        self.max_health = props["health"]
        self.damage = props["damage"]
        self.speed = props["speed"]
        self.color = props["color"]
        self.reward = props["reward"]
        
    def update(self, player_x, player_y):
        # Move towards player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0 and distance < 300:  # Detection range
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        self.animation_frame += 1
        
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw enemy body
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, 30, 30))
        pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, 30, 30), 2)
        
        # Draw health bar
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (draw_x, draw_y - 10, 30, 5))
        pygame.draw.rect(screen, (0, 255, 0), (draw_x, draw_y - 10, int(30 * health_percentage), 5))
        
        # Draw eyes
        pygame.draw.circle(screen, (255, 255, 255), (draw_x + 8, draw_y + 10), 3)
        pygame.draw.circle(screen, (255, 255, 255), (draw_x + 22, draw_y + 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (draw_x + 8, draw_y + 10), 1)
        pygame.draw.circle(screen, (0, 0, 0), (draw_x + 22, draw_y + 10), 1)

class NPC:
    def __init__(self, x, y, npc_type):
        self.x = x
        self.y = y
        self.type = npc_type
        self.dialogue = []
        self.quest_giver = False
        self.shop_keeper = False
        self.animation_frame = 0
        
        if npc_type == "shopkeeper":
            self.color = (255, 200, 100)
            self.dialogue = ["Welcome to my shop!", "Come back anytime!"]
            self.shop_keeper = True
        elif npc_type == "quest_giver":
            self.color = (100, 255, 100)
            self.dialogue = ["I have a quest for you!", "Complete it for rewards!"]
            self.quest_giver = True
        else:
            self.color = (200, 200, 200)
            self.dialogue = ["Hello traveler!", "Nice day for mining!"]
            
    def update(self):
        self.animation_frame += 1
        
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw NPC body
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, 25, 35))
        pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, 25, 35), 2)
        
        # Draw face
        pygame.draw.circle(screen, (255, 255, 255), (draw_x + 8, draw_y + 10), 3)
        pygame.draw.circle(screen, (255, 255, 255), (draw_x + 17, draw_y + 10), 3)
        
        # Draw hat if shopkeeper
        if self.shop_keeper:
            pygame.draw.rect(screen, (255, 0, 0), (draw_x + 5, draw_y - 5, 15, 5))

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.collected = False
        self.animation_frame = 0
        self.glow_timer = 0
        
        # Power-up properties
        self.properties = {
            "speed_boost": {"color": (255, 255, 0), "duration": 10000, "name": "Speed Boost"},
            "double_wealth": {"color": (255, 215, 0), "duration": 15000, "name": "Double Wealth"},
            "instant_mine": {"color": (255, 100, 255), "duration": 8000, "name": "Instant Mine"},
            "magnet_boost": {"color": (100, 255, 255), "duration": 12000, "name": "Magnet Boost"},
            "shield": {"color": (100, 100, 255), "duration": 20000, "name": "Shield"},
            "xray_vision": {"color": (255, 255, 100), "duration": 10000, "name": "X-Ray Vision"}
        }
        
        self.color = self.properties[powerup_type]["color"]
        self.duration = self.properties[powerup_type]["duration"]
        self.name = self.properties[powerup_type]["name"]
        
    def update(self):
        self.animation_frame += 1
        self.glow_timer += 1
        
    def draw(self, screen, camera_x, camera_y):
        if self.collected:
            return
            
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Glowing effect
        glow_size = 20 + abs(math.sin(self.glow_timer * 0.1)) * 5
        pygame.draw.circle(screen, (*self.color, 50), (int(draw_x + 10), int(draw_y + 10)), int(glow_size))
        
        # Draw power-up
        pygame.draw.circle(screen, self.color, (int(draw_x + 10), int(draw_y + 10)), 10)
        pygame.draw.circle(screen, (255, 255, 255), (int(draw_x + 10), int(draw_y + 10)), 10, 2)

class Quest:
    def __init__(self, quest_type, target, reward, description):
        self.type = quest_type
        self.target = target
        self.reward = reward
        self.description = description
        self.progress = 0
        self.completed = False
        
    def update_progress(self, amount=1):
        self.progress += amount
        if self.progress >= self.target:
            self.completed = True
            return True
        return False

class Structure:
    def __init__(self, x, y, structure_type):
        self.x = x
        self.y = y
        self.type = structure_type
        self.width = 60
        self.height = 60
        
        if structure_type == "house":
            self.color = (150, 100, 50)
        elif structure_type == "shop":
            self.color = (200, 150, 100)
        elif structure_type == "factory":
            self.color = (100, 100, 150)
        else:
            self.color = (100, 150, 100)
            
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw structure
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, self.width, self.height), 3)
        
        # Draw roof
        pygame.draw.polygon(screen, (100, 50, 0), [
            (draw_x - 10, draw_y),
            (draw_x + self.width + 10, draw_y),
            (draw_x + self.width // 2, draw_y - 30)
        ])

class Pet:
    def __init__(self, pet_type):
        self.type = pet_type
        self.x = 0
        self.y = 0
        self.speed = 2
        self.animation_frame = 0
        self.follow_distance = 50
        
        if pet_type == "dog":
            self.color = (150, 100, 50)
            self.size = 15
        elif pet_type == "cat":
            self.color = (100, 100, 100)
            self.size = 12
        else:
            self.color = (200, 200, 100)
            self.size = 10
            
    def update(self, player_x, player_y):
        # Follow player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > self.follow_distance:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        self.animation_frame += 1
        
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw pet
        pygame.draw.circle(screen, self.color, (int(draw_x), int(draw_y)), self.size)
        pygame.draw.circle(screen, (0, 0, 0), (int(draw_x), int(draw_y)), self.size, 2)
        
        # Draw eyes
        pygame.draw.circle(screen, (255, 255, 255), (int(draw_x - 5), int(draw_y - 3)), 2)
        pygame.draw.circle(screen, (255, 255, 255), (int(draw_x + 5), int(draw_y - 3)), 2)

class WeatherSystem:
    def __init__(self):
        self.current_weather = "clear"
        self.weather_timer = 0
        self.weather_duration = 0
        self.particles = []
        
    def update(self):
        self.weather_timer += 1
        
        if self.weather_timer >= self.weather_duration:
            self.change_weather()
            
        # Update weather particles
        if self.current_weather == "rain":
            self.update_rain()
        elif self.current_weather == "snow":
            self.update_snow()
            
    def change_weather(self):
        self.weather_timer = 0
        self.weather_duration = random.randint(300, 900)  # 5-15 seconds
        
        weather_choices = ["clear", "rain", "snow", "storm", "fog"]
        self.current_weather = random.choice(weather_choices)
        
    def update_rain(self):
        # Add rain particles
        for _ in range(5):
            x = random.randint(0, 1400)
            y = -10
            self.particles.append({"x": x, "y": y, "speed": random.uniform(5, 10)})
            
        # Update existing particles
        self.particles = [p for p in self.particles if p["y"] < 900]
        for particle in self.particles:
            particle["y"] += particle["speed"]
            
    def update_snow(self):
        # Add snow particles
        for _ in range(3):
            x = random.randint(0, 1400)
            y = -10
            self.particles.append({"x": x, "y": y, "speed": random.uniform(1, 3), "drift": random.uniform(-1, 1)})
            
        # Update existing particles
        self.particles = [p for p in self.particles if p["y"] < 900]
        for particle in self.particles:
            particle["y"] += particle["speed"]
            particle["x"] += particle["drift"]
            
    def draw(self, screen):
        if self.current_weather == "rain":
            for particle in self.particles:
                pygame.draw.line(screen, (100, 100, 255), 
                               (particle["x"], particle["y"]), 
                               (particle["x"], particle["y"] + 10), 1)
        elif self.current_weather == "snow":
            for particle in self.particles:
                pygame.draw.circle(screen, (255, 255, 255), (int(particle["x"]), int(particle["y"])), 2)

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            "first_gem": False,
            "wealthy": False,
            "miner": False,
            "explorer": False,
            "combat_master": False,
            "collector": False,
            "speed_miner": False,
            "rare_hunter": False
        }
        self.notifications = []
        
    def check_achievement(self, achievement_type, game):
        if not self.achievements[achievement_type]:
            # Check specific achievement conditions
            if achievement_type == "first_gem":
                if game.rubies > 0 or game.emeralds > 0 or game.diamonds > 0:
                    self.unlock_achievement(achievement_type, "First Gem Collected!", game)
            elif achievement_type == "wealthy":
                if game.wealth >= 1000:
                    self.unlock_achievement(achievement_type, "Wealthy Miner!", game)
            elif achievement_type == "miner":
                if hasattr(game, 'total_mined') and game.total_mined >= 100:
                    self.unlock_achievement(achievement_type, "Experienced Miner!", game)
            elif achievement_type == "explorer":
                if hasattr(game, 'explored_areas') and len(game.explored_areas) >= 10:
                    self.unlock_achievement(achievement_type, "Explorer!", game)
            elif achievement_type == "combat_master":
                if hasattr(game, 'enemies_defeated') and game.enemies_defeated >= 50:
                    self.unlock_achievement(achievement_type, "Combat Master!", game)
            elif achievement_type == "collector":
                total_gems = game.rubies + game.emeralds + game.diamonds + game.gold
                if total_gems >= 100:
                    self.unlock_achievement(achievement_type, "Gem Collector!", game)
            elif achievement_type == "speed_miner":
                if game.mining_speed >= 10:
                    self.unlock_achievement(achievement_type, "Speed Miner!", game)
            elif achievement_type == "rare_hunter":
                if game.diamonds >= 20:
                    self.unlock_achievement(achievement_type, "Rare Hunter!", game)
                    
    def unlock_achievement(self, achievement_type, message, game):
        self.achievements[achievement_type] = True
        self.notifications.append({"message": message, "timer": 180, "achievement": achievement_type})
        
        # Give reward
        game.wealth += 100
        if hasattr(game, 'gain_experience'):
            game.gain_experience(50)
        
    def update(self):
        # Update notifications
        for notification in self.notifications[:]:
            notification["timer"] -= 1
            if notification["timer"] <= 0:
                self.notifications.remove(notification)
                
    def draw(self, screen):
        for i, notification in enumerate(self.notifications):
            y_pos = 150 + i * 60
            
            # Draw achievement popup
            popup_rect = pygame.Rect(1400 // 2 - 200, y_pos, 400, 50)
            pygame.draw.rect(screen, (50, 50, 0), popup_rect)
            pygame.draw.rect(screen, (255, 215, 0), popup_rect, 3)
            
            # Draw text
            font = pygame.font.Font(None, 24)
            text = font.render("🏆 " + notification["message"], True, (255, 215, 0))
            text_rect = text.get_rect(center=(1400 // 2, y_pos + 25))
            screen.blit(text, text_rect)

print("Simplified Game Enhancement Module loaded successfully!")
print("Added: Enemies, NPCs, Power-ups, Weather, Achievements, Quests, Structures, Pets!")
