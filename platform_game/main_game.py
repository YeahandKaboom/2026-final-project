import pygame
import random
import sys
from constants import *
from game_platform import Platform, Ground
from portal import Portal

class Player(pygame.sprite.Sprite):
    """Player character for platform game"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 30
        self.vel_y = 0
        self.on_ground = False
        self.speed = PLAYER_SPEED
        
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ground collision
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True

class PlatformGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platform Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player()
        self.ground = Ground()
        self.platforms = []
        self.portals = []
        
        # Camera
        self.camera_x = 0
        
        # Generate initial platforms
        self.generate_platforms()
        
    def generate_platforms(self):
        """Generate platforms for the level"""
        # Generate some platforms
        for i in range(10):
            x = 300 + i * 200
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(50, 200)
            width = random.randint(80, 150)
            height = 20
            self.platforms.append(Platform(x, y, width, height))
            
        # Generate some portals
        for i in range(3):
            x = 500 + i * 400
            y = SCREEN_HEIGHT - GROUND_HEIGHT - 50
            self.portals.append(Portal(x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        # Update player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= self.player.speed
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += self.player.speed
            
        self.player.update()
        
        # Update ground
        self.ground.update()
        
        # Update portals
        for portal in self.portals[:]:
            portal.update(self.player.speed)
            if portal.is_off_screen():
                self.portals.remove(portal)
        
        # Camera follow player
        if self.player.rect.x > SCREEN_WIDTH // 2:
            self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
            
        # Generate new platforms as needed
        if self.platforms and self.platforms[-1].rect.x - self.camera_x < SCREEN_WIDTH:
            last_platform = self.platforms[-1]
            x = last_platform.rect.x + random.randint(200, 400)
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(50, 200)
            width = random.randint(80, 150)
            height = 20
            self.platforms.append(Platform(x, y, width, height))
            
        # Generate new portals
        if random.random() < 0.01:  # 1% chance per frame
            x = self.camera_x + SCREEN_WIDTH + random.randint(100, 300)
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(50, 150)
            self.portals.append(Portal(x, y))
    
    def draw(self):
        # Background
        self.screen.fill(BLACK)
        
        # Draw ground
        self.ground.draw(self.screen)
        
        # Draw platforms
        for platform in self.platforms:
            if platform.rect.x - self.camera_x < SCREEN_WIDTH and platform.rect.right - self.camera_x > 0:
                platform.draw(self.screen, self.camera_x)
        
        # Draw portals
        for portal in self.portals:
            portal.draw(self.screen, self.camera_x)
        
        # Draw player
        player_draw_x = self.player.rect.x - self.camera_x
        self.screen.blit(self.player.image, (player_draw_x, self.player.rect.y))
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        text = font.render("Platform Game - Use Arrow Keys to Move, Space to Jump", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = PlatformGame()
    game.run()

if __name__ == "__main__":
    main()
