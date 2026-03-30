# Ultimate Game Enhancement Module
import pygame
import random
import math
import json
import time

# Add these new classes to your wealth_craft_game.py

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
            GameState.EnemyType.GOBLIN: {"color": (100, 200, 100), "health": 30, "damage": 5, "speed": 2, "reward": 50},
            GameState.EnemyType.ROCK_MONSTER: {"color": (150, 150, 150), "health": 100, "damage": 10, "speed": 0.5, "reward": 100},
            GameState.EnemyType.CREEPER: {"color": (0, 255, 0), "health": 40, "damage": 15, "speed": 1.5, "reward": 75},
            GameState.EnemyType.DRAGON: {"color": (255, 100, 0), "health": 200, "damage": 25, "speed": 1, "reward": 500},
            GameState.EnemyType.GHOST: {"color": (200, 200, 255), "health": 25, "damage": 8, "speed": 3, "reward": 60},
            GameState.EnemyType.SPIDER: {"color": (50, 0, 50), "health": 35, "damage": 7, "speed": 2.5, "reward": 65}
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
        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, 30, 30), 2)
        
        # Draw health bar
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, RED, (draw_x, draw_y - 10, 30, 5))
        pygame.draw.rect(screen, GREEN, (draw_x, draw_y - 10, int(30 * health_percentage), 5))
        
        # Draw eyes
        pygame.draw.circle(screen, WHITE, (draw_x + 8, draw_y + 10), 3)
        pygame.draw.circle(screen, WHITE, (draw_x + 22, draw_y + 10), 3)
        pygame.draw.circle(screen, BLACK, (draw_x + 8, draw_y + 10), 1)
        pygame.draw.circle(screen, BLACK, (draw_x + 22, draw_y + 10), 1)

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
            
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Draw NPC body
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, 25, 35))
        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, 25, 35), 2)
        
        # Draw face
        pygame.draw.circle(screen, WHITE, (draw_x + 8, draw_y + 10), 3)
        pygame.draw.circle(screen, WHITE, (draw_x + 17, draw_y + 10), 3)
        
        # Draw hat if shopkeeper
        if self.shop_keeper:
            pygame.draw.rect(screen, (255, 0, 0), (draw_x + 5, draw_y - 5, 15, 5))
            
        self.animation_frame += 1

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
            GameState.PowerUpType.SPEED_BOOST: {"color": YELLOW, "duration": 10000, "name": "Speed Boost"},
            GameState.PowerUpType.DOUBLE_WEALTH: {"color": GOLD, "duration": 15000, "name": "Double Wealth"},
            GameState.PowerUpType.INSTANT_MINE: {"color": (255, 100, 255), "duration": 8000, "name": "Instant Mine"},
            GameState.PowerUpType.MAGNET_BOOST: {"color": (100, 255, 255), "duration": 12000, "name": "Magnet Boost"},
            GameState.PowerUpType.SHIELD: {"color": (100, 100, 255), "duration": 20000, "name": "Shield"},
            GameState.PowerUpType.XRAY_VISION: {"color": (255, 255, 100), "duration": 10000, "name": "X-Ray Vision"}
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
        pygame.draw.circle(screen, WHITE, (int(draw_x + 10), int(draw_y + 10)), 10, 2)

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
        pygame.draw.rect(screen, BLACK, (draw_x, draw_y, self.width, self.height), 3)
        
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
        pygame.draw.circle(screen, BLACK, (int(draw_x), int(draw_y)), self.size, 2)
        
        # Draw eyes
        pygame.draw.circle(screen, WHITE, (int(draw_x - 5), int(draw_y - 3)), 2)
        pygame.draw.circle(screen, WHITE, (int(draw_x + 5), int(draw_y - 3)), 2)

class WeatherSystem:
    def __init__(self):
        self.current_weather = GameState.WeatherType.CLEAR
        self.weather_timer = 0
        self.weather_duration = 0
        self.particles = []
        
    def update(self):
        self.weather_timer += 1
        
        if self.weather_timer >= self.weather_duration:
            self.change_weather()
            
        # Update weather particles
        if self.current_weather == GameState.WeatherType.RAIN:
            self.update_rain()
        elif self.current_weather == GameState.WeatherType.SNOW:
            self.update_snow()
            
    def change_weather(self):
        self.weather_timer = 0
        self.weather_duration = random.randint(300, 900)  # 5-15 seconds
        
        weather_choices = list(GameState.WeatherType)
        self.current_weather = random.choice(weather_choices)
        
    def update_rain(self):
        # Add rain particles
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = -10
            self.particles.append({"x": x, "y": y, "speed": random.uniform(5, 10)})
            
        # Update existing particles
        self.particles = [p for p in self.particles if p["y"] < SCREEN_HEIGHT]
        for particle in self.particles:
            particle["y"] += particle["speed"]
            
    def update_snow(self):
        # Add snow particles
        for _ in range(3):
            x = random.randint(0, SCREEN_WIDTH)
            y = -10
            self.particles.append({"x": x, "y": y, "speed": random.uniform(1, 3), "drift": random.uniform(-1, 1)})
            
        # Update existing particles
        self.particles = [p for p in self.particles if p["y"] < SCREEN_HEIGHT]
        for particle in self.particles:
            particle["y"] += particle["speed"]
            particle["x"] += particle["drift"]
            
    def draw(self, screen):
        if self.current_weather == GameState.WeatherType.RAIN:
            for particle in self.particles:
                pygame.draw.line(screen, (100, 100, 255), 
                               (particle["x"], particle["y"]), 
                               (particle["x"], particle["y"] + 10), 1)
        elif self.current_weather == GameState.WeatherType.SNOW:
            for particle in self.particles:
                pygame.draw.circle(screen, WHITE, (int(particle["x"]), int(particle["y"])), 2)

class AchievementSystem:
    def __init__(self):
        from wealth_craft_game import AchievementType
        self.achievements = {achievement: False for achievement in AchievementType}
        self.notifications = []
        
    def check_achievement(self, achievement_type, game):
        if not self.achievements[achievement_type]:
            # Check specific achievement conditions
            if achievement_type == GameState.AchievementType.FIRST_GEM:
                if game.rubies > 0 or game.emeralds > 0 or game.diamonds > 0:
                    self.unlock_achievement(achievement_type, "First Gem Collected!", game)
            elif achievement_type == GameState.AchievementType.WEALTHY:
                if game.wealth >= 1000:
                    self.unlock_achievement(achievement_type, "Wealthy Miner!", game)
            elif achievement_type == GameState.AchievementType.MINER:
                if game.total_mined >= 100:
                    self.unlock_achievement(achievement_type, "Experienced Miner!", game)
            elif achievement_type == GameState.AchievementType.EXPLORER:
                if len(game.explored_areas) >= 10:
                    self.unlock_achievement(achievement_type, "Explorer!", game)
            elif achievement_type == GameState.AchievementType.COMBAT_MASTER:
                if game.enemies_defeated >= 50:
                    self.unlock_achievement(achievement_type, "Combat Master!", game)
            elif achievement_type == GameState.AchievementType.COLLECTOR:
                total_gems = game.rubies + game.emeralds + game.diamonds + game.gold
                if total_gems >= 100:
                    self.unlock_achievement(achievement_type, "Gem Collector!", game)
            elif achievement_type == GameState.AchievementType.SPEED_MINER:
                if game.mining_speed >= 10:
                    self.unlock_achievement(achievement_type, "Speed Miner!", game)
            elif achievement_type == GameState.AchievementType.RARE_HUNTER:
                if game.diamonds >= 20:
                    self.unlock_achievement(achievement_type, "Rare Hunter!", game)
                    
    def unlock_achievement(self, achievement_type, message, game):
        self.achievements[achievement_type] = True
        self.notifications.append({"message": message, "timer": 180, "achievement": achievement_type})
        
        # Give reward
        game.wealth += 100
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
            popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_pos, 400, 50)
            pygame.draw.rect(screen, (50, 50, 0), popup_rect)
            pygame.draw.rect(screen, GOLD, popup_rect, 3)
            
            # Draw text
            font = pygame.font.Font(None, 24)
            text = font.render("🏆 " + notification["message"], True, GOLD)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 25))
            screen.blit(text, text_rect)

# Add these methods to your WealthCraftGame class:

def generate_biomes(self):
    """Generate different biomes in the world"""
    self.biomes = []
    biome_types = list(GameState.BiomeType)
    
    for i in range(5):  # Generate 5 biomes
        biome_type = random.choice(biome_types)
        x = i * 200
        y = random.randint(100, 400)
        self.biomes.append({"type": biome_type, "x": x, "y": y, "width": 200, "height": 300})
        
def spawn_enemies(self):
    """Spawn enemies in the world"""
    enemy_types = list(GameState.EnemyType)
    
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
        
def start_weather_system(self):
    """Initialize weather system"""
    self.weather_system = WeatherSystem()
    
def generate_initial_quests(self):
    """Generate starting quests"""
    # Add collect gems quest
    quest1 = Quest(
        GameState.QuestType.COLLECT_GEMS,
        10,
        {"wealth": 200, "experience": 100},
        "Collect 10 gems"
    )
    self.active_quests.append(quest1)
    
    # Add reach level quest
    quest2 = Quest(
        GameState.QuestType.REACH_LEVEL,
        3,
        {"wealth": 500, "experience": 200},
        "Reach level 3"
    )
    self.active_quests.append(quest2)
    
    # Add mine blocks quest
    quest3 = Quest(
        GameState.QuestType.MINE_BLOCKS,
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
        return SKY_BLUE
    elif 1800 < self.time_of_day <= 2000:  # Sunset
        return (255, 150, 100)
    elif 2000 < self.time_of_day <= 600:  # Night
        return (25, 25, 112)
    else:  # Sunrise
        return (255, 200, 150)

def spawn_powerups(self):
    """Spawn random power-ups"""
    if random.randint(1, 1000) == 1:  # 0.1% chance per frame
        powerup_types = list(GameState.PowerUpType)
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
    
    if powerup_type == GameState.PowerUpType.SPEED_BOOST:
        self.speed_boost = 2
    elif powerup_type == GameState.PowerUpType.DOUBLE_WEALTH:
        self.wealth_multiplier = 2
    elif powerup_type == GameState.PowerUpType.INSTANT_MINE:
        self.instant_mine = True
    elif powerup_type == GameState.PowerUpType.MAGNET_BOOST:
        self.magnet_boost = 2
    elif powerup_type == GameState.PowerUpType.SHIELD:
        self.shield_active = True
    elif powerup_type == GameState.PowerUpType.XRAY_VISION:
        self.xray_vision = True

def deactivate_powerup(self, powerup_type):
    """Deactivate a power-up effect"""
    if powerup_type == GameState.PowerUpType.SPEED_BOOST:
        self.speed_boost = 1
    elif powerup_type == GameState.PowerUpType.DOUBLE_WEALTH:
        self.wealth_multiplier = 1
    elif powerup_type == GameState.PowerUpType.INSTANT_MINE:
        self.instant_mine = False
    elif powerup_type == GameState.PowerUpType.MAGNET_BOOST:
        self.magnet_boost = 1
    elif powerup_type == GameState.PowerUpType.SHIELD:
        self.shield_active = False
    elif powerup_type == GameState.PowerUpType.XRAY_VISION:
        self.xray_vision = False

def check_quests(self):
    """Check quest progress"""
    for quest in self.active_quests[:]:
        if quest.type == GameState.QuestType.COLLECT_GEMS:
            total_gems = self.rubies + self.emeralds + self.diamonds + self.gold
            if quest.update_progress(total_gems - quest.progress):
                self.complete_quest(quest)
        elif quest.type == GameState.QuestType.REACH_LEVEL:
            if self.level >= quest.target:
                quest.completed = True
                self.complete_quest(quest)
        elif quest.type == GameState.QuestType.MINE_BLOCKS:
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

def save_game(self):
    """Save game progress"""
    save_data = {
        "level": self.level,
        "wealth": self.wealth,
        "experience": self.experience,
        "achievements": self.achievements,
        "owned_tools": self.owned_tools,
        "owned_weapons": self.owned_weapons,
        "owned_upgrades": self.owned_upgrades,
        "owned_items": self.owned_items,
        "completed_quests": len(self.completed_quests),
        "total_earned": self.total_earned
    }
    
    with open("wealth_craft_save.json", "w") as f:
        json.dump(save_data, f)

def load_game(self):
    """Load game progress"""
    try:
        with open("wealth_craft_save.json", "r") as f:
            save_data = json.load(f)
            
        self.level = save_data.get("level", 1)
        self.wealth = save_data.get("wealth", 0)
        self.experience = save_data.get("experience", 0)
        self.achievements = save_data.get("achievements", {})
        self.owned_tools = save_data.get("owned_tools", {})
        self.owned_weapons = save_data.get("owned_weapons", {})
        self.owned_upgrades = save_data.get("owned_upgrades", {})
        self.owned_items = save_data.get("owned_items", {})
        self.total_earned = save_data.get("total_earned", 0)
        
        return True
    except:
        return False

# Add these to your main game loop:

# In update() method:
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
    self.achievement_system.check_achievement(GameState.AchievementType.FIRST_GEM, self)
    self.achievement_system.check_achievement(GameState.AchievementType.WEALTHY, self)
    self.achievement_system.check_achievement(GameState.AchievementType.MINER, self)
    
    # Update quests
    self.check_quests()

# In draw() method:
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

# Add these initialization calls in __init__:
self.achievement_system = AchievementSystem()
self.weather_system = WeatherSystem()
self.powerups = []
self.powerup_properties = {
    powerup_type: {"color": (255, 255, 255), "duration": 10000}
    for powerup_type in GameState.PowerUpType
}
self.quest_notifications = []
self.total_mined = 0
self.enemies_defeated = 0

print("Ultimate Game Enhancement Module loaded successfully!")
print("Added: Enemies, NPCs, Power-ups, Weather, Achievements, Quests, Structures, Pets, Day/Night, Save System!")
