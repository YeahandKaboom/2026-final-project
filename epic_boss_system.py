# EPIC BOSS SYSTEM - Ultimate Mining Game Enhancement!
import pygame
import random
import math

class Boss:
    def __init__(self, x, y, boss_type):
        self.x = x
        self.y = y
        self.type = boss_type
        self.health = 1000
        self.max_health = 1000
        self.damage = 50
        self.speed = 2
        self.animation_frame = 0
        self.attack_timer = 0
        self.special_attack_cooldown = 0
        self.phase = 1
        self.enraged = False
        
        # Boss properties
        self.properties = {
            "crystal_golem": {
                "color": (200, 200, 255), 
                "health": 5000, 
                "damage": 30, 
                "speed": 1, 
                "reward": 10000,
                "special": "crystal_rain",
                "phases": 2
            },
            "shadow_dragon": {
                "color": (50, 0, 100), 
                "health": 8000, 
                "damage": 50, 
                "speed": 3, 
                "reward": 25000,
                "special": "shadow_breath",
                "phases": 3
            },
            "quantum_beast": {
                "color": (0, 255, 255), 
                "health": 12000, 
                "damage": 75, 
                "speed": 4, 
                "reward": 50000,
                "special": "quantum_teleport",
                "phases": 4
            },
            "cosmic_titan": {
                "color": (255, 0, 255), 
                "health": 20000, 
                "damage": 100, 
                "speed": 2, 
                "reward": 100000,
                "special": "cosmic_storm",
                "phases": 5
            },
            "infinity_warrior": {
                "color": (255, 255, 255), 
                "health": 50000, 
                "damage": 150, 
                "speed": 5, 
                "reward": 1000000,
                "special": "infinity_blade",
                "phases": 6
            }
        }
        
        props = self.properties[boss_type]
        self.health = props["health"]
        self.max_health = props["health"]
        self.damage = props["damage"]
        self.speed = props["speed"]
        self.color = props["color"]
        self.reward = props["reward"]
        self.special_attack = props["special"]
        self.max_phases = props["phases"]
        
    def update(self, player_x, player_y):
        self.animation_frame += 1
        self.attack_timer += 1
        self.special_attack_cooldown = max(0, self.special_attack_cooldown - 1)
        
        # Phase transitions
        health_percentage = self.health / self.max_health
        if health_percentage < 0.8 and self.phase == 1:
            self.phase = 2
            self.enraged = True
            self.speed *= 1.5
        elif health_percentage < 0.6 and self.phase == 2:
            self.phase = 3
            self.damage *= 1.5
        elif health_percentage < 0.4 and self.phase == 3:
            self.phase = 4
            self.speed *= 2
        elif health_percentage < 0.2 and self.phase == 4:
            self.phase = 5
            self.damage *= 2
            
        # Movement patterns based on boss type
        if self.type == "crystal_golem":
            # Slow, steady movement
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0 and distance < 400:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
        elif self.type == "shadow_dragon":
            # Flying pattern
            self.x += math.sin(self.animation_frame * 0.05) * self.speed * 2
            self.y += math.cos(self.animation_frame * 0.03) * self.speed
            if distance < 500:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
        elif self.type == "quantum_beast":
            # Teleporting movement
            if self.animation_frame % 60 == 0:
                self.x = player_x + random.randint(-200, 200)
                self.y = player_y + random.randint(-200, 200)
            else:
                dx = player_x - self.x
                dy = player_y - self.y
                if distance > 0:
                    self.x += (dx / distance) * self.speed
                    self.y += (dy / distance) * self.speed
                    
        elif self.type == "cosmic_titan":
            # Circular pattern
            angle = self.animation_frame * 0.02
            self.x = player_x + math.cos(angle) * 300
            self.y = player_y + math.sin(angle) * 300
            
        elif self.type == "infinity_warrior":
            # Aggressive pursuit
            dx = player_x - self.x
            dy = player_y - self.y
            if distance > 0:
                self.x += (dx / distance) * self.speed * 2
                self.y += (dy / distance) * self.speed * 2
    
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        # Boss size based on type
        if self.type == "crystal_golem":
            size = 60
            # Crystal golem body
            pygame.draw.rect(screen, self.color, (draw_x - size//2, draw_y - size//2, size, size))
            pygame.draw.rect(screen, BLACK, (draw_x - size//2, draw_y - size//2, size, size), 3)
            # Crystal spikes
            for i in range(8):
                angle = i * math.pi / 4
                spike_x = draw_x + math.cos(angle) * size
                spike_y = draw_y + math.sin(angle) * size
                pygame.draw.line(screen, (150, 150, 255), (draw_x, draw_y), (spike_x, spike_y), 3)
                
        elif self.type == "shadow_dragon":
            size = 80
            # Dragon body
            pygame.draw.ellipse(screen, self.color, (draw_x - size, draw_y - size//2, size * 2, size))
            pygame.draw.ellipse(screen, BLACK, (draw_x - size, draw_y - size//2, size * 2, size), 3)
            # Wings
            wing_flap = math.sin(self.animation_frame * 0.1) * 20
            pygame.draw.polygon(screen, (30, 0, 60), [
                (draw_x - size, draw_y),
                (draw_x - size - 40, draw_y - 20 + wing_flap),
                (draw_x - size - 40, draw_y + 20 + wing_flap)
            ])
            pygame.draw.polygon(screen, (30, 0, 60), [
                (draw_x + size, draw_y),
                (draw_x + size + 40, draw_y - 20 - wing_flap),
                (draw_x + size + 40, draw_y + 20 - wing_flap)
            ])
            
        elif self.type == "quantum_beast":
            size = 50
            # Quantum effect - multiple overlapping circles
            for i in range(5):
                offset = math.sin(self.animation_frame * 0.1 + i) * 10
                alpha = 100 + i * 30
                pygame.draw.circle(screen, (*self.color, alpha), 
                                 (int(draw_x + offset), int(draw_y - offset)), size - i * 5)
            # Core
            pygame.draw.circle(screen, WHITE, (int(draw_x), int(draw_y)), 10)
            
        elif self.type == "cosmic_titan":
            size = 100
            # Cosmic aura
            for i in range(3):
                aura_size = size + i * 20
                aura_alpha = 50 - i * 15
                pygame.draw.circle(screen, (*self.color, aura_alpha), 
                                 (int(draw_x), int(draw_y)), aura_size, 2)
            # Titan body
            pygame.draw.circle(screen, self.color, (int(draw_x), int(draw_y)), size)
            pygame.draw.circle(screen, BLACK, (int(draw_x), int(draw_y)), size, 3)
            # Cosmic particles
            for i in range(8):
                angle = self.animation_frame * 0.05 + i * math.pi / 4
                particle_x = draw_x + math.cos(angle) * (size + 20)
                particle_y = draw_y + math.sin(angle) * (size + 20)
                pygame.draw.circle(screen, WHITE, (int(particle_x), int(particle_y)), 3)
                
        elif self.type == "infinity_warrior":
            size = 70
            # Infinity symbol body
            pygame.draw.arc(screen, self.color, (draw_x - size, draw_y - size//2, size * 2, size), 0, math.pi, 5)
            pygame.draw.arc(screen, self.color, (draw_x - size, draw_y - size//2, size * 2, size), math.pi, 2 * math.pi, 5)
            # Warrior core
            pygame.draw.circle(screen, WHITE, (int(draw_x), int(draw_y)), 15)
            # Infinity blades
            blade_angle = self.animation_frame * 0.1
            for i in range(4):
                angle = blade_angle + i * math.pi / 2
                blade_x = draw_x + math.cos(angle) * (size + 20)
                blade_y = draw_y + math.sin(angle) * (size + 20)
                pygame.draw.line(screen, (255, 255, 255), (draw_x, draw_y), (blade_x, blade_y), 3)
        
        # Health bar
        bar_width = 100
        bar_height = 10
        bar_x = draw_x - bar_width // 2
        bar_y = draw_y - size - 30
        
        pygame.draw.rect(screen, BLACK, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        health_percentage = self.health / self.max_health
        health_color = GREEN if health_percentage > 0.5 else YELLOW if health_percentage > 0.25 else RED
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, int(bar_width * health_percentage), bar_height))
        
        # Boss name
        font = pygame.font.Font(None, 24)
        name = self.type.replace("_", " ").title()
        text = font.render(name, True, WHITE)
        text_rect = text.get_rect(center=(draw_x, bar_y - 10))
        screen.blit(text, text_rect)
        
        # Phase indicator
        if self.enraged:
            phase_text = font.render(f"Phase {self.phase}/{self.max_phases} - ENRAGED!", True, RED)
        else:
            phase_text = font.render(f"Phase {self.phase}/{self.max_phases}", True, WHITE)
        phase_rect = phase_text.get_rect(center=(draw_x, bar_y + 20))
        screen.blit(phase_text, phase_rect)

class SpecialEffect:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.type = effect_type
        self.animation_frame = 0
        self.lifetime = 60
        self.particles = []
        
        if effect_type == "explosion":
            self.color = (255, 100, 0)
            self.create_explosion_particles()
        elif effect_type == "lightning":
            self.color = (255, 255, 0)
            self.create_lightning_bolts()
        elif effect_type == "fire":
            self.color = (255, 0, 0)
            self.create_fire_particles()
        elif effect_type == "ice":
            self.color = (100, 200, 255)
            self.create_ice_crystals()
        elif effect_type == "heal":
            self.color = (0, 255, 0)
            self.create_heal_orbs()
        elif effect_type == "teleport":
            self.color = (200, 0, 255)
            self.create_teleport_swirl()
        elif effect_type == "time_warp":
            self.color = (255, 255, 255)
            self.create_time_rings()
        elif effect_type == "black_hole":
            self.color = (0, 0, 0)
            self.create_black_hole()
            
    def create_explosion_particles(self):
        for _ in range(30):
            particle = {
                "x": self.x,
                "y": self.y,
                "vx": random.uniform(-10, 10),
                "vy": random.uniform(-10, 10),
                "size": random.randint(3, 8),
                "life": random.randint(20, 40)
            }
            self.particles.append(particle)
            
    def create_lightning_bolts(self):
        for _ in range(5):
            bolt = []
            x, y = self.x, self.y
            for _ in range(5):
                x += random.randint(-30, 30)
                y += random.randint(20, 40)
                bolt.append((x, y))
            self.particles.append(bolt)
            
    def create_fire_particles(self):
        for _ in range(20):
            particle = {
                "x": self.x + random.randint(-20, 20),
                "y": self.y + random.randint(-20, 20),
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-5, -1),
                "size": random.randint(2, 6),
                "life": random.randint(15, 30)
            }
            self.particles.append(particle)
            
    def create_ice_crystals(self):
        for _ in range(15):
            crystal = {
                "x": self.x + random.randint(-30, 30),
                "y": self.y + random.randint(-30, 30),
                "size": random.randint(4, 10),
                "rotation": random.uniform(0, 360),
                "life": random.randint(30, 50)
            }
            self.particles.append(crystal)
            
    def create_heal_orbs(self):
        for _ in range(10):
            orb = {
                "x": self.x + random.randint(-25, 25),
                "y": self.y + random.randint(-25, 25),
                "vy": random.uniform(-2, -0.5),
                "size": random.randint(3, 6),
                "life": random.randint(20, 35)
            }
            self.particles.append(orb)
            
    def create_teleport_swirl(self):
        for i in range(20):
            angle = i * math.pi / 10
            particle = {
                "x": self.x + math.cos(angle) * 20,
                "y": self.y + math.sin(angle) * 20,
                "angle": angle,
                "radius": 20,
                "life": 30
            }
            self.particles.append(particle)
            
    def create_time_rings(self):
        for i in range(5):
            ring = {
                "radius": 10 + i * 15,
                "alpha": 255 - i * 40,
                "life": 40
            }
            self.particles.append(ring)
            
    def create_black_hole(self):
        self.particles = [{"radius": 5, "max_radius": 50, "life": 60}]
        
    def update(self):
        self.animation_frame += 1
        self.lifetime -= 1
        
        # Update particles based on effect type
        if self.type == "explosion":
            for particle in self.particles[:]:
                particle["x"] += particle["vx"]
                particle["y"] += particle["vy"]
                particle["vy"] += 0.5  # Gravity
                particle["life"] -= 1
                if particle["life"] <= 0:
                    self.particles.remove(particle)
                    
        elif self.type == "fire":
            for particle in self.particles[:]:
                particle["x"] += particle["vx"]
                particle["y"] += particle["vy"]
                particle["vy"] += 0.2
                particle["life"] -= 1
                if particle["life"] <= 0:
                    self.particles.remove(particle)
                    
        elif self.type == "heal":
            for particle in self.particles[:]:
                particle["y"] += particle["vy"]
                particle["life"] -= 1
                if particle["life"] <= 0:
                    self.particles.remove(particle)
                    
        elif self.type == "teleport":
            for particle in self.particles[:]:
                particle["angle"] += 0.2
                particle["radius"] -= 1
                particle["x"] = self.x + math.cos(particle["angle"]) * particle["radius"]
                particle["y"] = self.y + math.sin(particle["angle"]) * particle["radius"]
                particle["life"] -= 1
                if particle["life"] <= 0 or particle["radius"] <= 0:
                    self.particles.remove(particle)
                    
        elif self.type == "black_hole":
            for particle in self.particles[:]:
                particle["radius"] += 1
                particle["life"] -= 1
                if particle["radius"] >= particle["max_radius"]:
                    self.particles.remove(particle)
                    
    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        
        if self.type == "explosion":
            for particle in self.particles:
                alpha = particle["life"] / 40
                color = (255, int(100 * alpha), 0)
                pygame.draw.circle(screen, color, 
                                 (int(particle["x"] - camera_x), int(particle["y"] - camera_y)), 
                                 particle["size"])
                                 
        elif self.type == "lightning":
            for bolt in self.particles:
                if len(bolt) > 1:
                    points = [(x - camera_x, y - camera_y) for x, y in bolt]
                    pygame.draw.lines(screen, self.color, False, points, 2)
                    
        elif self.type == "fire":
            for particle in self.particles:
                alpha = particle["life"] / 30
                color = (255, int(100 * alpha), 0)
                pygame.draw.circle(screen, color,
                                 (int(particle["x"] - camera_x), int(particle["y"] - camera_y)),
                                 particle["size"])
                                 
        elif self.type == "ice":
            for crystal in self.particles:
                alpha = crystal["life"] / 50
                color = (int(100 * alpha), int(200 * alpha), 255)
                # Draw diamond shape
                points = [
                    (crystal["x"] - camera_x, crystal["y"] - camera_y - crystal["size"]),
                    (crystal["x"] - camera_x + crystal["size"], crystal["y"] - camera_y),
                    (crystal["x"] - camera_x, crystal["y"] - camera_y + crystal["size"]),
                    (crystal["x"] - camera_x - crystal["size"], crystal["y"] - camera_y)
                ]
                pygame.draw.polygon(screen, color, points)
                
        elif self.type == "heal":
            for particle in self.particles:
                alpha = particle["life"] / 35
                pygame.draw.circle(screen, (0, int(255 * alpha), 0),
                                 (int(particle["x"] - camera_x), int(particle["y"] - camera_y)),
                                 particle["size"])
                                 
        elif self.type == "teleport":
            for particle in self.particles:
                alpha = particle["life"] / 30
                color = (int(200 * alpha), 0, int(255 * alpha))
                pygame.draw.circle(screen, color,
                                 (int(particle["x"] - camera_x), int(particle["y"] - camera_y)), 3)
                                 
        elif self.type == "time_warp":
            for ring in self.particles:
                alpha = ring["life"] / 40
                color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
                pygame.draw.circle(screen, color, (draw_x, draw_y), ring["radius"], 2)
                
        elif self.type == "black_hole":
            for particle in self.particles:
                alpha = 1 - (particle["radius"] / particle["max_radius"])
                pygame.draw.circle(screen, (int(50 * alpha), 0, int(50 * alpha)), 
                                 (draw_x, draw_y), particle["radius"])

print("EPIC BOSS SYSTEM loaded! - Ultimate bosses, special effects, and insane battles!")
