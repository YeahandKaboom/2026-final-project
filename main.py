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
explosion_particles, game_over_message_index = [], 0

def generate_obstacle():
    global obstacle_sequence, last_obstacle_x, obstacles, boosts, level
    spawn_x = last_obstacle_x + 350
    last_obstacle_x = spawn_x
    obstacle_type = random.choice([Obstacle.TYPE_BOX, Obstacle.TYPE_SPIKE, Obstacle.TYPE_UPSIDE_DOWN_TRIANGLE])
    new_obstacle = Obstacle(spawn_x, SCREEN_HEIGHT - GROUND_HEIGHT, obstacle_type, level)
    if obstacle_type == Obstacle.TYPE_TALL_BOX and random.random() < 0.5:
        boost_y = SCREEN_HEIGHT - GROUND_HEIGHT - (100 if random.random() < 0.5 else 0)
        boosts.append(Boost(spawn_x + 20, boost_y))
    obstacles.append(new_obstacle)
    return new_obstacle

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

def reset_game():
    global game_over, score, distance, obstacles, collectibles, portals, boosts, camera_offset_x
    global current_speed, boost_timer, victory_timer, explosion_particles, obstacle_sequence
    global last_obstacle_x, portal_spawned, level, level_announcement_timer, high_score
    obstacle_sequence = 0
    last_obstacle_x = (SCREEN_WIDTH // 4) + 500
    portal_spawned = False
    level = 1
    level_announcement_timer = 0
    game_over = False
    if score > high_score: high_score = score
    score, distance, camera_offset_x, current_speed, boost_timer, victory_timer = 0, 0, 0, INITIAL_PLAYER_SPEED, 0, 0
    obstacles, collectibles, portals, boosts, explosion_particles = [], [], [], [], []
    player.rect.x, player.rect.y = SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT - 40
    player.vel_y, player.current_speed, player.frames_survived, player.jump_count = 0, INITIAL_PLAYER_SPEED, 0, 0
    for _ in range(3): obstacles.append(generate_obstacle())
    for _ in range(2): collectibles.append(generate_collectible())

def spawn_manager(player_x, camera_offset_x):
    """Manage spawning of obstacles and collectibles"""
    global last_obstacle_x
    
    # Spawn obstacles when player gets close to the last one
    if player_x + SCREEN_WIDTH > last_obstacle_x - 200:
        obstacles.append(generate_obstacle())
    
    # Randomly spawn collectibles
    if random.random() < 0.02:  # 2% chance per frame
        collectibles.append(generate_collectible())

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if victory_timer > 0: victory_timer = 0
            reset_game()
    
    if not game_over and level_announcement_timer == 0:
        keys, mouse_pressed = pygame.key.get_pressed(), pygame.mouse.get_pressed()[0]
        player.handle_input(keys, mouse_pressed)
        
        base_speed = min(INITIAL_PLAYER_SPEED + player.frames_survived * SPEED_INCREMENT, MAX_PLAYER_SPEED)
        
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
            # Create character break particles when hitting obstacle
            collision_type = result['collision_type']
            particle_colors = {
                'spike': [RED, WHITE, GRAY],
                'triangle': [RED, ORANGE, WHITE],
                'box': [BLUE, WHITE, GRAY]
            }
            colors = particle_colors.get(collision_type, [WHITE, GRAY, DARK_GRAY])
            
            for _ in range(15):
                explosion_particles.append({
                    'x': player.rect.centerx, 'y': player.rect.centery,
                    'vx': random.uniform(-8, 8), 'vy': random.uniform(-10, 3),
                    'color': random.choice(colors),
                    'size': random.randint(2, 5), 'life': 60
                })
        
        ground.update()
        for obstacle in obstacles: obstacle.update(current_speed)
        for portal in portals: portal.update(current_speed)
        for boost in boosts: boost.update(current_speed)
        
        for boost in boosts[:]:
            if not boost.collected and player.rect.colliderect(boost.rect) and player.vel_y > 0:
                boost.collected = True
                boost_timer = 180
                score += 50
                boosts.remove(boost)
        
        for portal in portals:
            if player.rect.colliderect(portal.rect):
                level += 1
                score += 1000
                level_announcement_timer = 180
                obstacles, portals, boosts = [], [], []
                portal_spawned = False
                obstacle_sequence = 0
                last_obstacle_x = (SCREEN_WIDTH // 4) + 500
                boost_timer = 0
                player.rect.x, player.rect.y = SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT - 40
                player.vel_y = 0
                player.jump_count = 0
                for _ in range(1): obstacles.append(generate_obstacle())
        
        camera_offset_x = max(0, player.rect.x - SCREEN_WIDTH // 4)
        spawn_manager(player.rect.x, camera_offset_x)
        
        # Check if portal should spawn at distance 100 (only in level 1)
        if int(distance // 50) >= 100 and not portal_spawned and level == 1:
            generate_portal()
        
        cleanup_obstacles()
        
        distance += current_speed
        score += int(current_speed / 50)
        
        if level >= 2 and int(distance // 50) >= 200 and victory_timer == 0:
            victory_timer = 300
            for _ in range(50):
                explosion_particles.append({
                    'x': player.rect.centerx, 'y': player.rect.centery,
                    'vx': random.uniform(-10, 10), 'vy': random.uniform(-15, 5),
                    'color': random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, (255, 128, 0), (0, 255, 255)]),
                    'size': random.randint(3, 8), 'life': 300
                })
            player.vel_y, player.vel_x = -15, 12
            game_over = True
            if victory_sound: victory_sound.play()
        
    if victory_timer > 0:
        victory_timer -= 1
        for particle in explosion_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.5
            particle['life'] -= 1
            particle['size'] = max(1, particle['size'] - 0.05)
            if particle['life'] <= 0:
                explosion_particles.remove(particle)
        
        player.rect.y += player.vel_y
        player.vel_y += 0.8
        player.rect.x += player.vel_x
        player.rotation_angle += 15
        
        if player.rect.right >= SCREEN_WIDTH:
            for _ in range(20):
                explosion_particles.append({
                    'x': player.rect.right, 'y': player.rect.centery,
                    'vx': random.uniform(-5, 5), 'vy': random.uniform(-8, 2),
                    'color': random.choice([RED, ORANGE, YELLOW]),
                    'size': random.randint(2, 6), 'life': 100
                })
            player.vel_x = 0
            player.rect.right = SCREEN_WIDTH
    
    if level_announcement_timer > 0: level_announcement_timer -= 1
    update_background_music()
    
    screen.fill(BLACK)
    
    color_index = (int(distance // 500) % len(BG_COLORS))
    next_color_index = (color_index + 1) % len(BG_COLORS)
    color_progress = (distance % 500) / 500.0
    current_color, next_color = BG_COLORS[color_index], BG_COLORS[next_color_index]
    
    bg_color = (
        int(current_color[0] + (next_color[0] - current_color[0]) * color_progress),
        int(current_color[1] + (next_color[1] - current_color[1]) * color_progress),
        int(current_color[2] + (next_color[2] - current_color[2]) * color_progress)
    )
    pygame.draw.rect(screen, bg_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
    
    ground.draw(screen)
    for obstacle in obstacles: obstacle.draw(screen, camera_offset_x)
    for portal in portals: portal.draw(screen, camera_offset_x)
    for boost in boosts: boost.draw(screen, camera_offset_x)
    
    for particle in explosion_particles:
        pygame.draw.circle(screen, particle['color'], 
                          (int(particle['x'] - camera_offset_x), int(particle['y'])), 
                          int(particle['size']))
    
    player.draw(screen, camera_offset_x)
    
    title_text = font_title.render("GEOMETRY DASH", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 5))
    
    # Calculate progress percentage (0-100% from start of level 1 to end of level 2)
    # Level 1: 0-100 feet, Level 2: 100-200 feet (total 200 feet)
    total_distance = min(distance, 200 * 50)  # Cap at end of level 2 (200 feet)
    progress_percent = min(100, int((total_distance / (200 * 50)) * 100))
    
    progress_text = font.render(f"Progress: {progress_percent}%", True, WHITE)
    speed_text = font_small.render(f"Speed: {current_speed:.1f}x", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    
    if boost_timer > 0:
        boost_text = font_small.render(f"BOOST: {boost_timer // 60 + 1}s", True, (0, 255, 255))
        screen.blit(boost_text, (10, 180))
    
    screen.blit(progress_text, (10, 60))
    screen.blit(speed_text, (10, 100))
    screen.blit(level_text, (10, 140))
    
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
        
        game_over_text = font.render("I'VE SEEN ROBOTS DO BETTER!", True, RED)
        progress_text = font.render(f"You made it {final_progress}% through the game!", True, WHITE)
        restart_text = font.render("Click to Restart", True, WHITE)
        
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(progress_text,
                   (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(restart_text, 
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()

pygame.quit()
