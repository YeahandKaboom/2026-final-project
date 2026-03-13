import pygame
import random
from constants import *
from player import Player
from game_platform import Ground
from enemy import Obstacle
from banana import Collectible
from portal import Portal
from boost import Boost

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound system
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 28)
font_title = pygame.font.Font(None, 48)

# Create player
player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT - 40)

# Create ground
ground = Ground()

# Create stressful background music
def create_stressful_music():
    """Create intense, stressful background music"""
    sample_rate = 22050
    duration = 1.0  # 1 second loop for intensity
    frames = int(sample_rate * duration)
    arr = []
    
    for i in range(frames):
        time = float(i) / sample_rate
        # Create stressful, dissonant pattern
        if i % (frames // 8) < frames // 16:  # Rapid changes
            freq = 220  # Low, ominous A3
        elif i % (frames // 8) < frames // 8:  # Medium
            freq = 330  # Unstable E4
        elif i % (frames // 8) < 3 * frames // 16:  # Higher tension
            freq = 440  # A4
        else:  # Dissonant intervals
            freq = 554 * 1.05  # Slightly sharp C#5
            
        # Add harsh square wave for stress
        value = 32767 if math.sin(2 * math.pi * freq * time) > 0 else -32767
        # Add noise for anxiety
        value += random.randint(-1000, 1000)
        arr.append([value, value])
    
    sound = pygame.sndarray.make_sound(arr)
    sound.set_volume(0.4)  # Slightly louder for stress
    return sound

# Create stressful background music using pygame channels
def create_stressful_beeps():
    """Create stressful beeping using pygame's mixer channels"""
    # Use pygame's built-in beep generation
    try:
        # Create a simple beep using pygame's sound system
        frequency = 440  # A4 note
        duration = 50  # milliseconds
        
        # Generate square wave
        sample_rate = 22050
        samples = int(sample_rate * duration / 1000)
        wave = []
        
        for i in range(samples):
            value = 32767 if (i // 50) % 2 == 0 else -32767
            wave.extend([value, value])
        
        # Convert to bytes and play
        sound_bytes = bytes(wave)
        beep = pygame.mixer.Sound(buffer=sound_bytes)
        beep.set_volume(0.2)
        return beep
    except:
        return None

# Load external music file
def load_external_music():
    """Load music from URL or local file"""
    try:
        # Try to load the extreme action music
        # First, let's try downloading and loading the music
        import urllib.request
        import os
        
        music_url = "https://www.bensound.com/royalty-free-music/track/extreme-action"
        local_filename = "extreme_action_music.ogg"
        
        # Download if not exists
        if not os.path.exists(local_filename):
            print(f"Downloading music from: {music_url}")
            try:
                urllib.request.urlretrieve(music_url, local_filename)
                print("Music downloaded successfully!")
            except Exception as e:
                print(f"Could not download music: {e}")
                return None
        
        # Load the music file
        if os.path.exists(local_filename):
            music = pygame.mixer.music.load(local_filename)
            pygame.mixer.music.set_volume(0.4)  # Moderate volume
            return music
        else:
            return None
    except Exception as e:
        print(f"Error loading music: {e}")
        return None

# Initialize music
external_music = load_external_music()
if external_music:
    pygame.mixer.music.play(-1)  # Loop indefinitely
    print("Playing external extreme action music!")
else:
    print("Using fallback beeping system")
    # Fallback to beeping system
    import time
    last_beep_time = time.time()

def update_background_music():
    """Update background music with continuous beeps (fallback)"""
    global last_beep_time
    if external_music:
        return  # Don't use beeps if external music loaded
    
    current_time = time.time()
    
    # Play beep every 0.8 seconds for stress
    if current_time - last_beep_time > 0.8:
        beep_sound = create_stressful_beeps()
        if beep_sound:
            beep_sound.play()
        last_beep_time = current_time

# Create victory sound effect
def create_victory_sound():
    """Create a victory celebration sound"""
    try:
        import math
        sample_rate = 22050
        duration = 0.5
        frames = int(sample_rate * duration)
        arr = []
        
        for i in range(frames):
            time_val = float(i) / sample_rate
            # Create ascending arpeggio for victory
            freq = 440 * (1 + i / frames)  # Rising frequency
            value = int(32767 * math.sin(2 * math.pi * freq * time_val) * math.exp(-time_val * 2))  # Fade out
            arr.append([value, value])
        
        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(0.5)
        return sound
    except ImportError:
        print("Warning: math/numpy not available for victory sound.")
        return None
    except Exception as e:
        print(f"Warning: Could not create victory sound: {e}")
        return None

# Initialize victory sound
try:
    victory_sound = create_victory_sound()
except Exception as e:
    print(f"Warning: Could not create victory sound: {e}")
    victory_sound = None

# Game state
obstacles = []
collectibles = []
portals = []
boosts = []
score = 0
distance = 0
game_over = False
camera_offset_x = 0
high_score = 0
current_speed = INITIAL_PLAYER_SPEED
obstacle_sequence = 0  # Track which type to spawn next (0=BOX, 1=SPIKE)
last_obstacle_x = 0  # Track position of last spawned obstacle for proper spacing
portal_spawned = False  # Track if portal has been spawned for current level
level = 1  # Current level
level_announcement_timer = 0  # Timer for showing level announcement
boost_timer = 0  # Timer for speed boost effect
victory_timer = 0  # Timer for victory animation
explosion_particles = []  # List for explosion particles
game_over_message_index = 0  # Track which game over message to show

def generate_obstacle():
    """Generate obstacles every seven feet with random types"""
    global obstacle_sequence, last_obstacle_x
    # Spawn exactly 7 feet (350 pixels) away from the last obstacle
    spawn_x = last_obstacle_x + 350
    last_obstacle_x = spawn_x
    
    # Random obstacle types for variety
    obstacle_types = [Obstacle.TYPE_BOX, Obstacle.TYPE_SPIKE, Obstacle.TYPE_UPSIDE_DOWN_TRIANGLE]
    obstacle_type = random.choice(obstacle_types)
    
    new_obstacle = Obstacle(spawn_x, SCREEN_HEIGHT - GROUND_HEIGHT, obstacle_type, level)
    
    # Spawn boost with tall triangles (randomly on box or ground)
    if obstacle_type == Obstacle.TYPE_TALL_BOX and random.random() < 0.5:
        # Randomly place boost on top of tall box or on ground nearby
        if random.random() < 0.5:
            # On top of tall box
            boost_y = SCREEN_HEIGHT - GROUND_HEIGHT - 100
            boost_x = spawn_x + 5
        else:
            # On ground near the box
            boost_y = SCREEN_HEIGHT - GROUND_HEIGHT
            boost_x = spawn_x + random.randint(-50, 90)
        
        boosts.append(Boost(boost_x, boost_y))
    
    return new_obstacle

def generate_collectible():
    """Generate random collectibles"""
    spawn_x = camera_offset_x + SCREEN_WIDTH + random.randint(100, 300)
    spawn_y = random.randint(SCREEN_HEIGHT - GROUND_HEIGHT - 150, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
    collectible_type = random.choice([Collectible.TYPE_COIN, Collectible.TYPE_COIN, Collectible.TYPE_STAR])
    return Collectible(spawn_x, spawn_y, collectible_type)

def spawn_manager(player_x, camera_offset_x):
    """Manage obstacle spawning"""
    # Spawn new obstacles if the last one is getting close to the screen
    if not obstacles or obstacles[-1].x < player_x + SCREEN_WIDTH + 500:
        new_obstacle = generate_obstacle()
        obstacles.append(new_obstacle)
    
    # Collectibles disabled
    # if not collectibles or collectibles[-1].x < camera_offset_x + SCREEN_WIDTH + 500:
    #     if random.random() < 0.6:  # 60% chance to spawn collectible
    #         collectibles.append(generate_collectible())

def spawn_portal():
    """Spawn portal on top of a tall box"""
    global portal_spawned
    # Spawn portal 1000 pixels ahead of player when they reach distance 200
    portal_x = player.rect.x + 1000
    # Position portal on top of a tall box (100px tall) + 60px clearance
    portal_y = SCREEN_HEIGHT - GROUND_HEIGHT - 160
    portal = Portal(portal_x, portal_y)
    portals.append(portal)
    portal_spawned = True
    
    # Also spawn a tall box underneath the portal for the player to land on
    tall_box = Obstacle(portal_x + 10, SCREEN_HEIGHT - GROUND_HEIGHT, Obstacle.TYPE_TALL_BOX, level)
    obstacles.append(tall_box)

def cleanup_obstacles():
    """Remove off-screen obstacles, collectibles, portals, and boosts"""
    global obstacles, collectibles, portals, boosts
    obstacles = [obs for obs in obstacles if not obs.is_off_screen()]
    collectibles = [col for col in collectibles if not col.is_off_screen()]
    portals = [por for por in portals if not por.is_off_screen()]
    boosts = [boo for boo in boosts if not boo.is_off_screen()]

# Initial obstacles - start with 10 foot spacing from player
last_obstacle_x = (SCREEN_WIDTH // 4) + 500  # 10 feet = 500 pixels from player start
for _ in range(1):
    obstacles.append(generate_obstacle())

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if victory_timer > 0:
                    # Click during victory animation - restart immediately
                    victory_timer = 0
                # Reset game - reset obstacle sequence
                obstacle_sequence = 0  # Reset obstacle pattern
                last_obstacle_x = (SCREEN_WIDTH // 4) + 500  # Reset with 10 foot spacing from player start
                portal_spawned = False  # Reset portal spawn
                level = 1  # Reset level
                level_announcement_timer = 0  # Reset announcement timer
                # Now reset the game state
                game_over = False
                if score > high_score:
                    high_score = score
                score = 0
                distance = 0
                obstacles = []
                collectibles = []
                portals = []  # Reset portals
                boosts = []  # Reset boosts
                camera_offset_x = 0
                current_speed = INITIAL_PLAYER_SPEED
                boost_timer = 0  # Reset boost timer
                victory_timer = 0  # Reset victory timer
                explosion_particles = []  # Clear explosion particles
                player.rect.x = SCREEN_WIDTH // 4
                player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40
                player.vel_y = 0
                player.current_speed = INITIAL_PLAYER_SPEED
                player.frames_survived = 0
                player.jump_count = 0
                for _ in range(3):
                    obstacles.append(generate_obstacle())
                for _ in range(2):
                    collectibles.append(generate_collectible())
    
    if not game_over and level_announcement_timer == 0:  # Only update game if not paused by announcement
        # Get keys pressed
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        # Handle player input
        player.handle_input(keys, mouse_pressed)
        
        # Increase difficulty over time
        base_speed = min(INITIAL_PLAYER_SPEED + player.frames_survived * SPEED_INCREMENT, MAX_PLAYER_SPEED)
        
        # Apply boost effect
        if boost_timer > 0:
            current_speed = min(base_speed * 1.5, MAX_PLAYER_SPEED * 1.2)  # 50% speed boost
            boost_timer -= 1
        else:
            current_speed = base_speed
            
        player.current_speed = current_speed
        
        # Update player
        is_alive = player.update(obstacles)
        if not is_alive:
            game_over = True
        
        # Update ground
        ground.update()
        
        # Update obstacles
        for obstacle in obstacles:
            obstacle.update(current_speed)
        
        # Update portals
        for portal in portals:
            portal.update(current_speed)
        
        # Update boosts
        for boost in boosts:
            boost.update(current_speed)
        
        # Check boost collisions
        for boost in boosts[:]:  # Use slice to safely modify during iteration
            if not boost.collected and player.rect.colliderect(boost.rect):
                # Check if player is jumping down onto the boost
                if player.vel_y > 0:
                    boost.collected = True
                    boost_timer = 180  # 3 seconds of boost at 60 FPS
                    score += 50  # Bonus points for collecting boost
                    boosts.remove(boost)
        
        # Check portal collision
        for portal in portals:
            if player.rect.colliderect(portal.rect):
                # Level complete - advance to next level
                level += 1
                score += 1000  # Bonus points for completing level
                
                # Start level announcement
                level_announcement_timer = 180  # 3 seconds at 60 FPS
                
                # Make triangles taller starting from level 2
                if level >= 2:
                    # This will be used in obstacle generation
                    pass
                
                # Reset for next level
                obstacles = []
                portals = []
                boosts = []  # Reset boosts for new level
                portal_spawned = False
                obstacle_sequence = 0
                last_obstacle_x = (SCREEN_WIDTH // 4) + 500
                boost_timer = 0  # Reset boost timer for new level
                player.rect.x = SCREEN_WIDTH // 4
                player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40
                player.vel_y = 0
                player.jump_count = 0
                # Spawn initial obstacles for new level
                for _ in range(1):
                    obstacles.append(generate_obstacle())
        
        # Update camera to follow player
        camera_offset_x = player.rect.x - SCREEN_WIDTH // 4
        camera_offset_x = max(0, camera_offset_x)
        
        # Spawn management
        spawn_manager(player.rect.x, camera_offset_x)
        
        # Check if portal should spawn at distance 200 (only in level 1)
        if int(distance // 50) >= 200 and not portal_spawned and level == 1:
            spawn_portal()
        
        cleanup_obstacles()
        
        # Update score and distance
        distance += current_speed
        score += int(current_speed / 50)  # Base score from distance
        
        # Check for victory condition (level 2, distance 400)
        if level >= 2 and int(distance // 50) >= 400 and victory_timer == 0:
            victory_timer = 300  # 5 seconds of victory animation
            # Create explosion particles
            for _ in range(50):
                particle = {
                    'x': player.rect.centerx,
                    'y': player.rect.centery,
                    'vx': random.uniform(-10, 10),
                    'vy': random.uniform(-15, 5),
                    'color': random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, (255, 128, 0), (0, 255, 255)]),
                    'size': random.randint(3, 8),
                    'life': 300
                }
                explosion_particles.append(particle)
            
            # Make player jump forward to crash into wall
            player.vel_y = -15  # Jump up
            player.vel_x = 12  # Move forward fast
            game_over = True  # End the game but show victory instead
            
            # Play victory sound
            if victory_sound:
                victory_sound.play()
        
        # Update victory timer and particles
    if victory_timer > 0:
        victory_timer -= 1
        # Update explosion particles
        for particle in explosion_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.5  # Gravity
            particle['life'] -= 1
            particle['size'] = max(1, particle['size'] - 0.05)
            if particle['life'] <= 0:
                explosion_particles.remove(particle)
        
        # Update player during victory animation
        player.rect.y += player.vel_y
        player.vel_y += 0.8  # Gravity
        player.rect.x += player.vel_x  # Move forward for wall crash
        player.rotation_angle += 15  # Spin during leap
        
        # Check if player hit the "wall" (screen edge)
        if player.rect.right >= SCREEN_WIDTH:
            # Create crash impact particles
            for _ in range(20):
                particle = {
                    'x': player.rect.right,
                    'y': player.rect.centery,
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-8, 2),
                    'color': random.choice([RED, ORANGE, YELLOW]),
                    'size': random.randint(2, 6),
                    'life': 100
                }
                explosion_particles.append(particle)
            # Stop horizontal movement after crash
            player.vel_x = 0
            player.rect.right = SCREEN_WIDTH  # Keep at wall
        
        # Update score and distance
        distance += current_speed
        score += int(current_speed / 50)  # Base score from distance
    
    # Update level announcement timer (even when game is paused)
    if level_announcement_timer > 0:
        level_announcement_timer -= 1
    
    # Update background music (stressful beeps)
    update_background_music()
    
    # Rendering
    screen.fill(BLACK)
    
    # Draw background with fading color effect based on distance
    color_index = (int(distance // 500) % len(BG_COLORS))
    next_color_index = (color_index + 1) % len(BG_COLORS)
    
    # Calculate interpolation between current and next color
    color_progress = (distance % 500) / 500.0
    current_color = BG_COLORS[color_index]
    next_color = BG_COLORS[next_color_index]
    
    # Interpolate between colors
    bg_color = (
        int(current_color[0] + (next_color[0] - current_color[0]) * color_progress),
        int(current_color[1] + (next_color[1] - current_color[1]) * color_progress),
        int(current_color[2] + (next_color[2] - current_color[2]) * color_progress)
    )
    pygame.draw.rect(screen, bg_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
    
    # Draw ground
    ground.draw(screen)
    
    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen, camera_offset_x)
    
    # Draw portals
    for portal in portals:
        portal.draw(screen, camera_offset_x)
    
    # Draw boosts
    for boost in boosts:
        boost.draw(screen, camera_offset_x)
    
    # Draw explosion particles
    for particle in explosion_particles:
        pygame.draw.circle(screen, particle['color'], 
                          (int(particle['x'] - camera_offset_x), int(particle['y'])), 
                          int(particle['size']))
    
    # Draw player
    player.draw(screen, camera_offset_x)
    
    # Draw UI
    # Draw title
    title_text = font_title.render("GEOMETRY DASH", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 5))
    
    distance_text = font.render(f"Distance: {int(distance // 50)}", True, WHITE)
    speed_text = font_small.render(f"Speed: {current_speed:.1f}x", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    
    # Draw boost indicator
    if boost_timer > 0:
        boost_text = font_small.render(f"BOOST: {boost_timer // 60 + 1}s", True, (0, 255, 255))
        screen.blit(boost_text, (10, 180))
    
    screen.blit(distance_text, (10, 60))
    screen.blit(speed_text, (10, 100))
    screen.blit(level_text, (10, 140))
    
    # Draw level announcement
    if level_announcement_timer > 0:
        # Create announcement text
        if level == 2:
            announcement_text = "GEOMETRY DASH LEVEL TWO!"
        else:
            announcement_text = f"GEOMETRY DASH LEVEL {level}!"
        
        # Render announcement
        announcement_surface = font_large.render(announcement_text, True, YELLOW)
        announcement_rect = announcement_surface.get_rect()
        announcement_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Draw semi-transparent background for text
        announcement_bg = pygame.Surface((announcement_rect.width + 40, announcement_rect.height + 40), pygame.SRCALPHA)
        announcement_bg.fill((0, 0, 0, 180))
        announcement_bg_rect = announcement_bg.get_rect()
        announcement_bg_rect.center = announcement_rect.center
        
        screen.blit(announcement_bg, announcement_bg_rect)
        screen.blit(announcement_surface, announcement_rect)
    
    # Draw victory screen
    if victory_timer > 0:
        # Create colorful "YEAH AND KABOOM!" text
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, (255, 128, 0), (0, 255, 255)]
        victory_text = "YEAH AND KABOOM!"
        
        # Draw multiple colored versions for rainbow effect
        for i, color in enumerate(colors):
            offset = i * 2
            victory_surface = font_large.render(victory_text, True, color)
            victory_rect = victory_surface.get_rect()
            victory_rect.center = (SCREEN_WIDTH // 2 + offset, SCREEN_HEIGHT // 2 - 100 + offset)
            screen.blit(victory_surface, victory_rect)
        
        # Main white text
        victory_surface = font_large.render(victory_text, True, WHITE)
        victory_rect = victory_surface.get_rect()
        victory_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        screen.blit(victory_surface, victory_rect)
        
        # Victory subtitle
        subtitle_text = font.render("VICTORY! You conquered Yeah and Kaboom!", True, YELLOW)
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Score display
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        screen.blit(score_text, score_rect)
        
        # Restart instruction
        if victory_timer < 240:  # Show after 1 second
            restart_text = font.render("Click to Play Again", True, (200, 200, 255))
            restart_rect = restart_text.get_rect()
            restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            screen.blit(restart_text, restart_rect)
    
    # Draw game over screen (only if not victory)
    if game_over and victory_timer == 0:
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Single game over message
        game_over_text = font.render("I'VE SEEN ROBOTS DO BETTER!", True, RED)
        restart_text = font.render("Click to Restart", True, WHITE)
        
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, 
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()

pygame.quit()
