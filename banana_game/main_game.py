import pygame
import random
import sys
from constants import *
from banana import Collectible
from boost import Boost

class Player(pygame.sprite.Sprite):
    """Player character for banana game"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)  # Yellow player for banana game
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 30
        self.vel_y = 0
        self.on_ground = False
        self.speed = PLAYER_SPEED
        self.score = 0
        
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

class BananaGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Banana Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player()
        self.collectibles = []
        self.boosts = []
        
        # Camera
        self.camera_x = 0
        
        # Generate initial items
        self.generate_items()
        
    def generate_items(self):
        """Generate collectibles and boosts"""
        # Generate some collectibles
        for i in range(15):
            x = 200 + i * 150
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(50, 200)
            collectible_type = random.choice([Collectible.TYPE_COIN, Collectible.TYPE_STAR])
            self.collectibles.append(Collectible(x, y, collectible_type))
            
        # Generate some boosts
        for i in range(5):
            x = 300 + i * 300
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(30, 150)
            self.boosts.append(Boost(x, y))
    
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
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            collectible.update(self.player.speed)
            if collectible.is_off_screen():
                self.collectibles.remove(collectible)
            elif not collectible.collected and self.player.rect.colliderect(collectible.rect):
                collectible.collected = True
                self.player.score += collectible.points
        
        # Update boosts
        for boost in self.boosts[:]:
            boost.update(self.player.speed)
            if boost.is_off_screen():
                self.boosts.remove(boost)
            elif not boost.collected and self.player.rect.colliderect(boost.rect):
                boost.collected = True
                self.player.speed *= 1.5  # Speed boost
        
        # Camera follow player
        if self.player.rect.x > SCREEN_WIDTH // 2:
            self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
            
        # Generate new items as needed
        if random.random() < 0.02:  # 2% chance per frame
            x = self.camera_x + SCREEN_WIDTH + random.randint(50, 200)
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(50, 200)
            collectible_type = random.choice([Collectible.TYPE_COIN, Collectible.TYPE_STAR])
            self.collectibles.append(Collectible(x, y, collectible_type))
            
        if random.random() < 0.005:  # 0.5% chance per frame
            x = self.camera_x + SCREEN_WIDTH + random.randint(100, 300)
            y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(30, 150)
            self.boosts.append(Boost(x, y))
    
    def draw(self):
        # Background
        self.screen.fill(BLACK)
        
        # Draw ground
        pygame.draw.rect(self.screen, DARK_GRAY, 
                        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Draw collectibles
        for collectible in self.collectibles:
            if not collectible.collected:
                collectible.draw(self.screen, self.camera_x)
        
        # Draw boosts
        for boost in self.boosts:
            if not boost.collected:
                boost.draw(self.screen, self.camera_x)
        
        # Draw player
        player_draw_x = self.player.rect.x - self.camera_x
        self.screen.blit(self.player.image, (player_draw_x, self.player.rect.y))
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        instruction_text = font.render("Banana Game - Arrow Keys: Move, Space: Jump", True, WHITE)
        self.screen.blit(instruction_text, (10, 50))
        
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
    game = BananaGame()
    game.run()

if __name__ == "__main__":
    main()
