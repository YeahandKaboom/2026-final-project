import pygame
import random
import time
import math
import urllib.request
import os
from constants import *
from player import Player
from enemy import Obstacle
from banana import Collectible
from portal import Portal
from boost import Boost
from game_platform import Ground

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("YEAH AND KABOOM!")
clock = pygame.time.Clock()

# Make sure window gets focus
pygame.event.set_grab(False)
pygame.mouse.set_visible(True)
pygame.display.flip()

# Fonts
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 28)
font_title = pygame.font.Font(None, 48)

# Music setup
def load_external_music():
    try:
        music_url = "https://www.bensound.com/royalty-free-music/track/extreme-action"
        local_filename = "extreme_action_music.ogg"
        if not os.path.exists(local_filename):
            print(f"Downloading music from: {music_url}")
            try:
                urllib.request.urlretrieve(music_url, local_filename)
                print("Music downloaded successfully!")
            except Exception as e:
                print(f"Could not download music: {e}")
                return None
        if os.path.exists(local_filename):
            music = pygame.mixer.music.load(local_filename)
            pygame.mixer.music.set_volume(0.4)  # Moderate volume
            return music
        else:
            return None
    except Exception as e:
        print(f"Error loading music: {e}")
        return None

def create_stressful_beeps():
    try:
        frequency = 440  # A4 note
        duration = 50  # milliseconds
        sample_rate = 22050
        samples = int(sample_rate * duration / 1000)
        wave = []
        for i in range(samples):
            value = 32767 if (i // 50) % 2 == 0 else -32767
            wave.extend([value, value])
        sound_bytes = bytes(wave)
        beep = pygame.mixer.Sound(buffer=sound_bytes)
        beep.set_volume(0.2)
        return beep
    except:
        return None

external_music = load_external_music()
if external_music:
    pygame.mixer.music.play(-1)
else:
    last_beep_time = time.time()

def update_background_music():
    global last_beep_time
    if not external_music and time.time() - last_beep_time > 0.8:
        beep_sound = create_stressful_beeps()
        if beep_sound:
            beep_sound.play()
        last_beep_time = time.time()

# Create victory sound effect
def create_victory_sound():
    try:
        sample_rate, duration, frames = 22050, 0.5, int(22050 * 0.5)
        arr = [[int(32767 * math.sin(2 * math.pi * 440 * (1 + i/frames) * (i/sample_rate)) * math.exp(-(i/sample_rate) * 2))] * 2 for i in range(frames)]
        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(0.5)
        return sound
    except:
        return None

# Initialize victory sound
try:
    victory_sound = create_victory_sound()
except Exception as e:
    print(f"Warning: Could not create victory sound: {e}")
    victory_sound = None

# Game state
obstacles, collectibles, portals, boosts = [], [], [], []
score, distance, game_over, camera_offset_x, high_score = 0, 0, False, 0, 0
current_speed, obstacle_sequence, last_obstacle_x = INITIAL_PLAYER_SPEED, 0, 0
portal_spawned, level, level_announcement_timer, boost_timer, victory_timer = False, 1, 0, 0, 0

# New systems
screen_shake = 0
combo = 0
max_combo = 0
total_jumps = 0
total_deaths = 0
total_play_time = 0
start_time = time.time()
game_state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER, VICTORY
menu_selection = 0
difficulty = "NORMAL"  # EASY, NORMAL, HARD
auto_start_timer = 180  # 3 seconds at 60 FPS

# Enhanced particles
particles = []
trail_particles = []

# Sound effects dictionary
sound_effects = {
    'jump': None,
    'land': None,
    'coin': None,
    'death': None,
    'victory': None,
    'powerup': None,
    'combo': None
}
# Enhanced sound generation
def create_jump_sound():
    arr = [(int(32767 * math.sin(2 * math.pi * 400 * t / 44100))) for t in range(44100 // 10)]
    return pygame.sndarray.make_sound(arr)

def create_land_sound():
    arr = [(int(32767 * math.sin(2 * math.pi * 200 * t / 44100) * (1 - t / (44100 // 20)))) for t in range(44100 // 20)]
    return pygame.sndarray.make_sound(arr)

def create_coin_sound():
    arr = [(int(32767 * math.sin(2 * math.pi * 800 * t / 44100) * (1 - t / (44100 // 15)))) for t in range(44100 // 15)]
    return pygame.sndarray.make_sound(arr)

def create_death_sound():
    arr = [(int(32767 * math.sin(2 * math.pi * 150 * t / 44100) * (t / (44100 // 30)))) for t in range(44100 // 30)]
    return pygame.sndarray.make_sound(arr)

def create_powerup_sound():
    arr = [(int(32767 * math.sin(2 * math.pi * 600 * t / 44100) * math.sin(2 * math.pi * 3 * t / 44100))) for t in range(44100 // 20)]
    return pygame.sndarray.make_sound(arr)

def create_combo_sound():
    arr = [(int(32767 * math.sin(2 * math.pi * 1000 * t / 44100) * (1 - t / (44100 // 10)))) for t in range(44100 // 10)]
    return pygame.sndarray.make_sound(arr)

# Initialize sound effects
try:
    sound_effects['jump'] = create_jump_sound()
    sound_effects['land'] = create_land_sound()
    sound_effects['coin'] = create_coin_sound()
    sound_effects['death'] = create_death_sound()
    sound_effects['powerup'] = create_powerup_sound()
    sound_effects['combo'] = create_combo_sound()
except Exception as e:
    print(f"Warning: Could not create sound effects: {e}")

def play_sound(sound_name):
    if sound_effects.get(sound_name):
        sound_effects[sound_name].play()

# Enhanced particle system
def create_particle(x, y, vx, vy, color, size, life, particle_type="normal"):
    return {
        'x': x, 'y': y, 'vx': vx, 'vy': vy,
        'color': color, 'size': size, 'life': life,
        'type': particle_type, 'max_life': life
    }

def create_explosion(x, y, count=20, colors=None):
    if colors is None:
        colors = [RED, ORANGE, YELLOW, WHITE]
    for _ in range(count):
        vx = random.uniform(-10, 10)
        vy = random.uniform(-15, 5)
        color = random.choice(colors)
        size = random.randint(2, 6)
        life = random.randint(30, 60)
        particles.append(create_particle(x, y, vx, vy, color, size, life))

def create_trail_particle(x, y):
    vx = random.uniform(-2, 0)
    vy = random.uniform(-1, 1)
    color = random.choice([BLUE, CYAN, WHITE])
    size = random.randint(1, 3)
    life = random.randint(10, 20)
    trail_particles.append(create_particle(x, y, vx, vy, color, size, life, "trail"))

def update_particles(particle_list):
    for particle in particle_list[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += 0.5  # Gravity
        particle['life'] -= 1
        
        if particle['type'] == "trail":
            particle['size'] *= 0.95  # Shrink trail particles
        
        if particle['life'] <= 0:
            particle_list.remove(particle)

def apply_screen_shake(intensity):
    global screen_shake
    screen_shake = max(screen_shake, intensity)

# Moving obstacle class
class MovingObstacle(Obstacle):
    def __init__(self, x, y, obstacle_type, level, move_type="horizontal", move_range=100, move_speed=2):
        super().__init__(x, y, obstacle_type, level)
        self.move_type = move_type
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_x = x
        self.start_y = y
        self.direction = 1
        self.time = 0
    
    def update(self, player_speed):
        super().update(player_speed)
        self.time += 1
        
        if self.move_type == "horizontal":
            self.rect.x += self.move_speed * self.direction
            if abs(self.rect.x - self.start_x) > self.move_range:
                self.direction *= -1
        elif self.move_type == "vertical":
            self.rect.y += self.move_speed * self.direction
            if abs(self.rect.y - self.start_y) > self.move_range:
                self.direction *= -1

explosion_particles = []
game_over_message_index = 0

def generate_obstacle():
    global obstacle_sequence, last_obstacle_x, obstacles, boosts, level
    spawn_x = last_obstacle_x + 350
    last_obstacle_x = spawn_x
    
    # Add moving obstacles in level 2
    if level >= 2 and random.random() < 0.3:  # 30% chance for moving obstacle
        obstacle_type = random.choice([Obstacle.TYPE_SPIKE, Obstacle.TYPE_UPSIDE_DOWN_TRIANGLE])
        move_type = random.choice(["horizontal", "vertical"])
        move_range = random.randint(50, 150)
        move_speed = random.uniform(1, 3)
        new_obstacle = MovingObstacle(spawn_x, SCREEN_HEIGHT - GROUND_HEIGHT, obstacle_type, level, move_type, move_range, move_speed)
    else:
        obstacle_type = random.choice([Obstacle.TYPE_BOX, Obstacle.TYPE_SPIKE, Obstacle.TYPE_UPSIDE_DOWN_TRIANGLE, Obstacle.TYPE_TALL_BOX])
        new_obstacle = Obstacle(spawn_x, SCREEN_HEIGHT - GROUND_HEIGHT, obstacle_type, level)
    
    if obstacle_type == Obstacle.TYPE_TALL_BOX and random.random() < 0.5:
        boost_y = SCREEN_HEIGHT - GROUND_HEIGHT - (100 if random.random() < 0.5 else 0)
        boosts.append(Boost(spawn_x + 20, boost_y))
    
    obstacles.append(new_obstacle)
    return new_obstacle

# Power-up system
class PowerUp:
    def __init__(self, x, y, power_type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.power_type = power_type  # "speed", "invincibility", "double_jump", "slow_motion"
        self.collected = False
        self.animation_time = 0
    
    def update(self, player_speed):
        self.rect.x -= player_speed
        self.animation_time += 1
    
    def draw(self, surface, camera_offset_x=0):
        if self.collected:
            return
        
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_offset_x
        
        # Animated power-up
        pulse = abs(math.sin(self.animation_time * 0.1)) * 5
        size = 15 + pulse
        
        colors = {
            "speed": (255, 100, 100),
            "invincibility": (255, 215, 0),
            "double_jump": (100, 255, 100),
            "slow_motion": (100, 100, 255)
        }
        
        color = colors.get(self.power_type, WHITE)
        pygame.draw.circle(surface, color, adjusted_rect.center, int(size))
        pygame.draw.circle(surface, WHITE, adjusted_rect.center, int(size), 2)
    
    def is_off_screen(self):
        return self.rect.right < 0

def generate_powerup():
    power_types = ["speed", "invincibility", "double_jump", "slow_motion"]
    power_type = random.choice(power_types)
    spawn_x = camera_offset_x + SCREEN_WIDTH + random.randint(100, 300)
    spawn_y = random.randint(SCREEN_HEIGHT - GROUND_HEIGHT - 200, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
    return PowerUp(spawn_x, spawn_y, power_type)

# Main menu functions
def draw_main_menu():
    screen.fill(BLACK)
    
    # Animated background
    for i in range(0, SCREEN_WIDTH, 50):
        for j in range(0, SCREEN_HEIGHT, 50):
            color = (i % 255, j % 255, (i + j) % 255)
            pygame.draw.rect(screen, color, (i, j, 50, 50))
    
    # Title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("YEAH AND KABOOM", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(title_text, title_rect)
    
    # Menu options
    menu_font = pygame.font.Font(None, 48)
    options = ["START GAME", "DIFFICULTY", "STATISTICS", "QUIT"]
    
    for i, option in enumerate(options):
        color = YELLOW if i == menu_selection else WHITE
        text = menu_font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 80))
        screen.blit(text, text_rect)
    
    # Difficulty display
    diff_text = font.render(f"Current: {difficulty}", True, WHITE)
    diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
    screen.blit(diff_text, diff_rect)

def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pause_font = pygame.font.Font(None, 64)
    pause_text = pause_font.render("PAUSED", True, WHITE)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(pause_text, pause_rect)
    
    menu_font = pygame.font.Font(None, 48)
    options = ["RESUME", "RESTART", "MAIN MENU"]
    
    for i, option in enumerate(options):
        color = YELLOW if i == menu_selection else WHITE
        text = menu_font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 80))
        screen.blit(text, text_rect)

def draw_statistics():
    screen.fill(BLACK)
    
    stats_font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    
    title_text = title_font.render("STATISTICS", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    stats = [
        f"High Score: {high_score}",
        f"Total Jumps: {total_jumps}",
        f"Total Deaths: {total_deaths}",
        f"Max Combo: {max_combo}",
        f"Play Time: {int(total_play_time)}s",
        f"Best Progress: {0}%"  # Will be calculated
    ]
    
    for i, stat in enumerate(stats):
        text = stats_font.render(stat, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 50))
        screen.blit(text, text_rect)
    
    back_text = stats_font.render("Press ESC to go back", True, YELLOW)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
    screen.blit(back_text, back_rect)

def generate_collectible():
    spawn_x = camera_offset_x + SCREEN_WIDTH + random.randint(100, 300)
    spawn_y = random.randint(SCREEN_HEIGHT - GROUND_HEIGHT - 150, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
    collectible_type = random.choice([Collectible.TYPE_COIN, Collectible.TYPE_COIN, Collectible.TYPE_STAR])
    return Collectible(spawn_x, spawn_y, collectible_type)

def generate_portal():
    global portal_spawned, portals, last_obstacle_x, obstacles, level
    portal_spawned = True
    portal_x = last_obstacle_x + 500
    portals.append(Portal(portal_x, SCREEN_HEIGHT - GROUND_HEIGHT - 50))
    tall_box = Obstacle(portal_x + 10, SCREEN_HEIGHT - GROUND_HEIGHT, Obstacle.TYPE_TALL_BOX, level)
    obstacles.append(tall_box)

def cleanup_obstacles():
    """Remove off-screen obstacles, collectibles, portals, and boosts"""
    global obstacles, collectibles, portals, boosts
    obstacles = [obs for obs in obstacles if not obs.is_off_screen()]
    collectibles = [col for col in collectibles if not col.is_off_screen()]
    portals = [por for por in portals if not por.is_off_screen()]
    boosts = [boo for boo in boosts if not boo.is_off_screen()]

# Initial setup
last_obstacle_x = (SCREEN_WIDTH // 4) + 500
for _ in range(1): obstacles.append(generate_obstacle())
player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
ground = Ground()
powerups = []
active_powerups = []

def cleanup_obstacles():
    """Remove obstacles that are too far behind the player"""
    global obstacles
    obstacles = [obs for obs in obstacles if obs.rect.x > camera_offset_x - SCREEN_WIDTH]

def spawn_manager(player_x, camera_offset_x):
    """Manage spawning of obstacles and collectibles"""
    global last_obstacle_x
    
    # Spawn obstacles when player gets close to the last one
    if player_x + SCREEN_WIDTH > last_obstacle_x - 200:
        obstacles.append(generate_obstacle())
    
    # Randomly spawn collectibles
    if random.random() < 0.02:  # 2% chance per frame
        collectibles.append(generate_collectible())

def reset_game():
    global game_over, score, distance, obstacles, collectibles, portals, boosts, camera_offset_x
    global current_speed, boost_timer, victory_timer, explosion_particles, obstacle_sequence
    global last_obstacle_x, portal_spawned, level, level_announcement_timer, high_score
    global combo, max_combo, screen_shake, particles, trail_particles, powerups, active_powerups
    
    obstacle_sequence = 0
    last_obstacle_x = (SCREEN_WIDTH // 4) + 500
    portal_spawned = False
    level = 1
    level_announcement_timer = 0
    game_over = False
    if score > high_score: high_score = score
    if combo > max_combo: max_combo = combo
    
    score, distance, camera_offset_x, current_speed, boost_timer, victory_timer = 0, 0, 0, INITIAL_PLAYER_SPEED, 0, 0
    obstacles, collectibles, portals, boosts, explosion_particles = [], [], [], [], []
    particles, trail_particles, powerups, active_powerups = [], [], [], []
    combo = 0
    screen_shake = 0
    
    player.rect.x, player.rect.y = SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT - 40
    player.vel_y, player.current_speed, player.frames_survived, player.jump_count = 0, INITIAL_PLAYER_SPEED, 0, 0
    for _ in range(3): obstacles.append(generate_obstacle())
    for _ in range(2): collectibles.append(generate_collectible())

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Handle events for all states first
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle different game states
    if game_state == "MENU":
        draw_main_menu()
        
        # Auto-start after 3 seconds if no interaction
        auto_start_timer -= 1
        if auto_start_timer <= 0:
            print("Auto-starting game...")
            game_state = "PLAYING"
            reset_game()
            auto_start_timer = 180  # Reset timer
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}")  # Debug message
                auto_start_timer = 180  # Reset timer on any key press
                if event.key == pygame.K_UP:
                    menu_selection = (menu_selection - 1) % 4
                    print(f"Menu selection: {menu_selection}")
                elif event.key == pygame.K_DOWN:
                    menu_selection = (menu_selection + 1) % 4
                    print(f"Menu selection: {menu_selection}")
                elif event.key == pygame.K_RETURN:
                    print("ENTER pressed - starting game")
                    if menu_selection == 0:  # START GAME
                        game_state = "PLAYING"
                        reset_game()
                        print("Game started!")
                    elif menu_selection == 1:  # DIFFICULTY
                        difficulties = ["EASY", "NORMAL", "HARD"]
                        current_index = difficulties.index(difficulty)
                        difficulty = difficulties[(current_index + 1) % 3]
                    elif menu_selection == 2:  # STATISTICS
                        game_state = "STATISTICS"
                    elif menu_selection == 3:  # QUIT
                        running = False
    
    elif game_state == "STATISTICS":
        draw_statistics()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "MENU"
    
    elif game_state == "PLAYING" or game_state == "PAUSED":
        if game_state == "PAUSED":
            draw_pause_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "PLAYING"
                    elif event.key == pygame.K_UP:
                        menu_selection = (menu_selection - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        menu_selection = (menu_selection + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if menu_selection == 0:  # RESUME
                            game_state = "PLAYING"
                        elif menu_selection == 1:  # RESTART
                            reset_game()
                            game_state = "PLAYING"
                        elif menu_selection == 2:  # MAIN MENU
                            game_state = "MENU"
        else:  # PLAYING state
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "PAUSED"
                        menu_selection = 0
                elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                    if victory_timer > 0: 
                        victory_timer = 0
                        reset_game()
                        game_state = "MENU"
                    else:
                        total_deaths += 1
                        reset_game()
            
            if not game_over and level_announcement_timer == 0:
                keys, mouse_pressed = pygame.key.get_pressed(), pygame.mouse.get_pressed()[0]
                
                # Track jumps for combo system
                if keys[pygame.K_SPACE] and player.on_ground:
                    total_jumps += 1
                    combo += 1
                    play_sound('jump')
                    create_trail_particle(player.rect.centerx, player.rect.bottom)
                    apply_screen_shake(2)
                elif not player.on_ground:
                    # Reset combo if player falls without jumping
                    if player.vel_y > 5:  # Falling fast
                        combo = 0
                
                player.handle_input(keys, mouse_pressed)
                
                base_speed = min(INITIAL_PLAYER_SPEED + player.frames_survived * SPEED_INCREMENT, MAX_PLAYER_SPEED)
                
                # Apply difficulty settings
                difficulty_mult = {"EASY": 0.6, "NORMAL": 1.0, "HARD": 1.4}.get(difficulty, 1.0)
                base_speed *= difficulty_mult
                
                # Make levels slower
                if level == 1:
                    base_speed = base_speed * 0.7  # 30% slower on level 1
                elif level == 2:
                    # Set level 2 speed to range from 3.3 to 3.5
                    progress_in_level = min(1.0, (distance - 100 * 50) / (100 * 50))  # Progress through level 2 (0-1)
                    base_speed = 3.3 + (progress_in_level * 0.2)  # 3.3 to 3.5
                
                current_speed = min(base_speed * 1.5, MAX_PLAYER_SPEED * 1.2) if boost_timer > 0 else base_speed
                if boost_timer > 0: boost_timer -= 1
                player.current_speed = current_speed
                
                result = player.update(obstacles)
                if not result['alive']: 
                    game_over = True
                    total_deaths += 1
                    play_sound('death')
                    apply_screen_shake(10)
                    combo = 0
                    # Create character break particles when hitting obstacle
                    collision_type = result['collision_type']
                    particle_colors = {
                        'spike': [RED, WHITE, GRAY],
                        'triangle': [RED, ORANGE, WHITE],
                        'box': [BLUE, WHITE, GRAY]
                    }
                    colors = particle_colors.get(collision_type, [WHITE, GRAY, DARK_GRAY])
                    create_explosion(player.rect.centerx, player.rect.centery, 15, colors)
                
                ground.update()
                for obstacle in obstacles: obstacle.update(current_speed)
                for portal in portals: portal.update(current_speed)
                for boost in boosts: boost.update(current_speed)
                for powerup in powerups: powerup.update(current_speed)
                
                # Update particles
                update_particles(particles)
                update_particles(trail_particles)
                
                # Update screen shake
                if screen_shake > 0:
                    screen_shake -= 1
                
                # Collectibles and collisions
                for collectible in collectibles[:]:
                    if not collectible.collected and player.rect.colliderect(collectible.rect):
                        collectible.collected = True
                        score += collectible.points
                        combo += 1
                        play_sound('coin')
                        create_explosion(collectible.rect.centerx, collectible.rect.centery, 5, [YELLOW, WHITE])
                        if combo > max_combo: max_combo = combo
                        if combo % 10 == 0:  # Combo milestone
                            play_sound('combo')
                            apply_screen_shake(5)
                        collectibles.remove(collectible)
                
                # Power-up collisions
                for powerup in powerups[:]:
                    if not powerup.collected and player.rect.colliderect(powerup.rect):
                        powerup.collected = True
                        play_sound('powerup')
                        active_powerups.append({'type': powerup.power_type, 'timer': 300})  # 5 seconds
                        create_explosion(powerup.rect.centerx, powerup.rect.centery, 10, [(255, 215, 0), YELLOW])
                        powerups.remove(powerup)
                        score += 100
                
                # Update active power-ups
                for powerup in active_powerups[:]:
                    powerup['timer'] -= 1
                    if powerup['timer'] <= 0:
                        active_powerups.remove(powerup)
                
                for boost in boosts[:]:
                    if not boost.collected and player.rect.colliderect(boost.rect) and player.vel_y > 0:
                        boost.collected = True
                        boost_timer = 180
                        score += 50
                        play_sound('powerup')
                        create_explosion(boost.rect.centerx, boost.rect.centery, 8, [CYAN, BLUE])
                        boosts.remove(boost)
                
                # Portal collision
                for portal in portals[:]:
                    if not portal.used and player.rect.colliderect(portal.rect):
                        portal.used = True
                        level += 1
                        level_announcement_timer = 180
                        play_sound('powerup')
                        create_explosion(portal.rect.centerx, portal.rect.centery, 20, [PURPLE, BLUE, WHITE])
                        if level > 2:
                            level = 2  # Cap at level 2
                        # Reset obstacles for new level
                        obstacles.clear()
                        last_obstacle_x = player.rect.x + 500
                        for _ in range(3): obstacles.append(generate_obstacle())
                
                camera_offset_x = max(0, player.rect.x - SCREEN_WIDTH // 4)
                spawn_manager(player.rect.x, camera_offset_x)
                cleanup_obstacles()
                
                # Randomly spawn power-ups
                if random.random() < 0.005:  # 0.5% chance per frame
                    powerups.append(generate_powerup())
                
                # Check if portal should spawn at distance 100 (only in level 1)
                if int(distance // 50) >= 100 and not portal_spawned and level == 1:
                    generate_portal()
                
                distance += current_speed
                score += int(current_speed / 50)
                total_play_time = time.time() - start_time
                
                if level >= 2 and int(distance // 50) >= 200 and victory_timer == 0:
                    victory_timer = 300
                    play_sound('victory')
                    create_explosion(player.rect.centerx, player.rect.centery, 50, [RED, BLUE, GREEN, YELLOW, PURPLE, (255, 128, 0), (0, 255, 255)])
                    player.vel_y, player.vel_x = -15, 12
                    game_over = True
                    apply_screen_shake(15)
                
                # Victory animation update
                if victory_timer > 0:
                    victory_timer -= 1
                    for particle in explosion_particles[:]:
                        particle['x'] += particle['vx']
                        particle['y'] += particle['vy']
                        particle['vy'] += 0.8
                        particle['life'] -= 1
                        if particle['life'] <= 0:
                            explosion_particles.remove(particle)
                    
                    player.rect.y += player.vel_y
                    player.vel_y += 0.8
                    player.rect.x += player.vel_x
                    player.rotation_angle += 15
                    if player.rect.right >= SCREEN_WIDTH:
                        create_explosion(player.rect.right, player.rect.centery, 20, [RED, ORANGE, YELLOW])
                        player.vel_x = 0
                        player.rect.right = SCREEN_WIDTH
                        apply_screen_shake(20)
            
            # Apply screen shake to camera
            shake_offset_x = 0
            shake_offset_y = 0
            if screen_shake > 0:
                shake_offset_x = random.randint(-screen_shake, screen_shake)
                shake_offset_y = random.randint(-screen_shake, screen_shake)
            
            # Rendering
            # Background with screen shake
            bg_color_index = int(distance // 100) % len(BG_COLORS)
            bg_color = BG_COLORS[bg_color_index]
            next_color = BG_COLORS[(bg_color_index + 1) % len(BG_COLORS)]
            fade = (distance % 100) / 100
            final_bg_color = tuple(int(bg_color[i] * (1 - fade) + next_color[i] * fade) for i in range(3))
            screen.fill(final_bg_color)
            
            # Draw background elements with shake
            for i in range(0, SCREEN_WIDTH * 3, 100):
                for j in range(0, SCREEN_HEIGHT - GROUND_HEIGHT, 100):
                    star_color = (255, 255, 255, 100 + int(155 * math.sin(distance * 0.01 + i * 0.1 + j * 0.1)))
                    pygame.draw.circle(screen, WHITE[:3], (i - camera_offset_x // 2 + shake_offset_x, j + shake_offset_y), 2)
            
            # Draw ground with shake
            ground_rect = ground.rect.copy()
            ground_rect.x += shake_offset_x
            ground_rect.y += shake_offset_y
            screen.blit(ground.image, ground_rect)
            
            # Draw game elements with shake
            for obstacle in obstacles:
                obstacle.draw(screen, camera_offset_x - shake_offset_x)
            for portal in portals:
                portal.draw(screen, camera_offset_x - shake_offset_x)
            for boost in boosts:
                boost.draw(screen, camera_offset_x - shake_offset_x)
            for powerup in powerups:
                powerup.draw(screen, camera_offset_x - shake_offset_x)
            for collectible in collectibles:
                collectible.draw(screen, camera_offset_x - shake_offset_x)
            
            # Draw particles with shake
            for particle in particles + trail_particles:
                alpha = particle['life'] / particle['max_life']
                size = int(particle['size'] * alpha)
                if size > 0:
                    pygame.draw.circle(screen, particle['color'], 
                                      (int(particle['x'] - camera_offset_x + shake_offset_x), 
                                       int(particle['y'] + shake_offset_y)), size)
            
            # Draw player with shake
            player.draw(screen, camera_offset_x - shake_offset_x)
            
            # UI (no shake)
            title_text = font_title.render("GEOMETRY DASH", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 5))
            
            # Calculate progress percentage (0-100% from start of level 1 to end of level 2)
            total_distance = min(distance, 200 * 50)
            progress_percent = min(100, int((total_distance / (200 * 50)) * 100))
            
            progress_text = font.render(f"Progress: {progress_percent}%", True, WHITE)
            speed_text = font_small.render(f"Speed: {current_speed:.1f}x", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            combo_text = font.render(f"Combo: {combo}", True, YELLOW) if combo > 1 else font.render(f"Combo: {combo}", True, WHITE)
            
            if boost_timer > 0:
                boost_text = font_small.render(f"BOOST: {boost_timer // 60 + 1}s", True, (0, 255, 255))
                screen.blit(boost_text, (10, 180))
            
            # Active power-ups
            y_offset = 220
            for powerup in active_powerups:
                power_text = font_small.render(f"{powerup['type'].upper()}: {powerup['timer'] // 60 + 1}s", True, (255, 215, 0))
                screen.blit(power_text, (10, y_offset))
                y_offset += 30
            
            screen.blit(progress_text, (10, 60))
            screen.blit(speed_text, (10, 100))
            screen.blit(level_text, (10, 140))
            screen.blit(combo_text, (10, 180))
            
            if level_announcement_timer > 0:
                announcement_text = "GEOMETRY DASH LEVEL TWO!" if level == 2 else f"GEOMETRY DASH LEVEL {level}!"
                announcement_surface = font_large.render(announcement_text, True, YELLOW)
                announcement_rect = announcement_surface.get_rect()
                announcement_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                
                announcement_bg = pygame.Surface((announcement_rect.width + 40, announcement_rect.height + 40), pygame.SRCALPHA)
                announcement_bg.fill((0, 0, 0, 180))
                announcement_bg_rect = announcement_bg.get_rect()
                announcement_bg_rect.center = announcement_rect.center
                
                screen.blit(announcement_bg, announcement_bg_rect)
                screen.blit(announcement_surface, announcement_rect)
            
            if victory_timer > 0:
                colors = [RED, BLUE, GREEN, YELLOW, PURPLE, (255, 128, 0), (0, 255, 255)]
                victory_text = "YEAH AND KABOOM!"
                
                for i, color in enumerate(colors):
                    offset = i * 2
                    victory_surface = font_large.render(victory_text, True, color)
                    victory_rect = victory_surface.get_rect()
                    victory_rect.center = (SCREEN_WIDTH // 2 + offset, SCREEN_HEIGHT // 2 - 100 + offset)
                    screen.blit(victory_surface, victory_rect)
                
                if victory_timer < 240:
                    restart_text = font.render("Click to Play Again", True, (200, 200, 255))
                    restart_rect = restart_text.get_rect()
                    restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
                    screen.blit(restart_text, restart_rect)
            
            if game_over and victory_timer == 0:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(200)
                overlay.fill(BLACK)
                screen.blit(overlay, (0, 0))
                
                # Calculate final progress percentage
                total_distance = min(distance, 200 * 50)
                final_progress = min(100, int((total_distance / (200 * 50)) * 100))
                
                # Only show game over message if not victory (victory_timer > 0 means victory)
                if victory_timer == 0:
                    game_over_text = font.render("I'VE SEEN ROBOTS DO BETTER!", True, RED)
                    progress_text = font.render(f"You made it {final_progress}% through the game!", True, WHITE)
                    combo_text = font.render(f"Max Combo: {max_combo}", True, YELLOW)
                    restart_text = font.render("Click to Restart", True, WHITE)
                    
                    screen.blit(game_over_text, 
                               (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
                    screen.blit(progress_text,
                               (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                    screen.blit(combo_text,
                               (SCREEN_WIDTH // 2 - combo_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    screen.blit(restart_text, 
                               (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()

pygame.quit()
