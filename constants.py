# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (200, 50, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Background color palette for fading effect - toned down neon colors (no yellow)
BG_COLORS = [
    (0, 200, 200),      # Soft cyan
    (200, 0, 200),      # Soft pink
    (0, 200, 0),        # Soft green
    (200, 100, 0),      # Soft orange
    (100, 0, 200),      # Soft purple
    (200, 150, 150),    # Light pink
    (0, 200, 100),      # Soft spring green
    (100, 200, 200),    # Light cyan
    (150, 100, 200),    # Soft lavender
    (0, 200, 200),      # Back to soft cyan
]

# Physics
GRAVITY = 0.5
JUMP_STRENGTH = -14
PLAYER_SPEED = 8  # Constant forward speed

# Game FPS
FPS = 60

# Camera
CAMERA_SCROLL_THRESHOLD_Y = 300  # Distance from top before camera scrolls up
CAMERA_SCROLL_THRESHOLD_X = 200  # Distance from sides before camera scrolls horizontally

# Geometry Dash specific
GROUND_HEIGHT = 100
OBSTACLE_SPAWN_DISTANCE = 1200  # Spawn obstacles ahead of player

# Game difficulty
INITIAL_PLAYER_SPEED = 4
MAX_PLAYER_SPEED = 10
SPEED_INCREMENT = 0.0005  # Increases every frame

# Collectibles
COLLECTIBLE_SIZE = 20
COLLECTIBLE_SCORE = 50

