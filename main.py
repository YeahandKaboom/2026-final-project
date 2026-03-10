import pygame
import random
from constants import *
from player import Player
from game_platform import Ground
from enemy import Obstacle
from banana import Collectible
from portal import Portal

# Initialize Pygame
pygame.init()
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

# Game state
obstacles = []
collectibles = []
portals = []
score = 0
distance = 0
game_over = False
camera_offset_x = 0
high_score = 0
current_speed = INITIAL_PLAYER_SPEED
obstacle_sequence = 0  # Track which type to spawn next (0=BOX, 1=SPIKE)
last_obstacle_x = 0  # Track position of last spawned obstacle for proper spacing
portal_spawned = False  # Track if portal has been spawned

def generate_obstacle():
    """Generate obstacles every seven feet"""
    global obstacle_sequence, last_obstacle_x
    # Spawn exactly 7 feet (350 pixels) away from the last obstacle
    spawn_x = last_obstacle_x + 350
    last_obstacle_x = spawn_x
    
    # Cycle through obstacle types for variety (includes upside-down triangle)
    obstacle_types = [Obstacle.TYPE_BOX, Obstacle.TYPE_SPIKE, Obstacle.TYPE_UPSIDE_DOWN_TRIANGLE]
    obstacle_type = obstacle_types[obstacle_sequence % len(obstacle_types)]
    obstacle_sequence += 1
    
    return Obstacle(spawn_x, SCREEN_HEIGHT - GROUND_HEIGHT, obstacle_type)

def generate_collectible():
    """Generate random collectibles"""
    spawn_x = camera_offset_x + SCREEN_WIDTH + random.randint(100, 300)
    spawn_y = random.randint(SCREEN_HEIGHT - GROUND_HEIGHT - 150, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
    collectible_type = random.choice([Collectible.TYPE_COIN, Collectible.TYPE_COIN, Collectible.TYPE_STAR])
    return Collectible(spawn_x, spawn_y, collectible_type)

def spawn_portal():
    """Spawn portal when distance reaches 200"""
    global portal_spawned
    if not portal_spawned and distance // 50 >= 200:  # Distance is in feet units
        portal_x = player.rect.x + SCREEN_WIDTH  # Spawn ahead of player
        portals.append(Portal(portal_x, SCREEN_HEIGHT - GROUND_HEIGHT))
        portal_spawned = True

def spawn_manager(player_x, camera_offset_x):
    """Manage obstacle spawning"""
    # Spawn new obstacles if the last one is getting close to the screen
    if not obstacles or obstacles[-1].x < player_x + SCREEN_WIDTH + 500:
        new_obstacle = generate_obstacle()
        obstacles.append(new_obstacle)
    
    # Check if portal should spawn
    spawn_portal()
    
    # Collectibles disabled
    # if not collectibles or collectibles[-1].x < camera_offset_x + SCREEN_WIDTH + 500:
    #     if random.random() < 0.6:  # 60% chance to spawn collectible
    #         collectibles.append(generate_collectible())

def cleanup_obstacles():
    """Remove off-screen obstacles, collectibles, and portals"""
    global obstacles, collectibles, portals
    obstacles = [obs for obs in obstacles if not obs.is_off_screen()]
    collectibles = [col for col in collectibles if not col.is_off_screen()]
    portals = [port for port in portals if not port.is_off_screen()]

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
                # Reset game - reset obstacle sequence
                obstacle_sequence = 0  # Reset obstacle pattern
                last_obstacle_x = (SCREEN_WIDTH // 4) + 500  # Reset with 10 foot spacing from player start
                portal_spawned = False  # Reset portal spawn
                # Now reset the game state
                game_over = False
                if score > high_score:
                    high_score = score
                score = 0
                distance = 0
                obstacles = []
                collectibles = []
                portals = []  # Reset portals
                camera_offset_x = 0
                current_speed = INITIAL_PLAYER_SPEED
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
    
    if not game_over:
        # Get keys pressed
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        # Handle player input
        player.handle_input(keys, mouse_pressed)
        
        # Increase difficulty over time
        current_speed = min(INITIAL_PLAYER_SPEED + player.frames_survived * SPEED_INCREMENT, MAX_PLAYER_SPEED)
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
        
        # Check portal collision
        for portal in portals:
            if player.rect.colliderect(portal.rect):
                # Portal gives bonus points and removes itself
                score += 500
                portals.remove(portal)
                break
        
        # Update camera to follow player
        camera_offset_x = player.rect.x - SCREEN_WIDTH // 4
        camera_offset_x = max(0, camera_offset_x)
        
        # Spawn management
        spawn_manager(player.rect.x, camera_offset_x)
        cleanup_obstacles()
        
        # Update score and distance
        distance += current_speed
        score += int(current_speed / 50)  # Base score from distance
    
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
    
    # Draw player
    player.draw(screen, camera_offset_x)
    
    # Draw UI
    # Draw title
    title_text = font_title.render("GEOMETRY DASH", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 5))
    
    distance_text = font.render(f"Distance: {int(distance // 50)}", True, WHITE)
    speed_text = font_small.render(f"Speed: {current_speed:.1f}x", True, WHITE)
    
    screen.blit(distance_text, (10, 60))
    screen.blit(speed_text, (10, 100))
    
    # Draw game over screen
    if game_over:
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        restart_text = font.render("Click to Restart", True, WHITE)
        
        screen.blit(game_over_text, 
                   (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, 
                   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()

pygame.quit()
