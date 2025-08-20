# Snake-Game
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚗 Traffic vs. Zombie 🧟")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 30, bold=True)

# Load assets (You can replace with real images)
car_img = pygame.Surface((60, 100))
car_img.fill(GREEN)

zombie_img = pygame.Surface((50, 70))
zombie_img.fill(RED)

background = pygame.Surface((WIDTH, HEIGHT))
background.fill((50, 50, 50))

# Player class
class Car:
    def __init__(self):
        self.image = car_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Zombie class
class Zombie:
    def __init__(self):
        self.image = zombie_img
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH - 40), -100))
        self.speed = random.randint(3, 6)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Main game function
def game_loop():
    car = Car()
    zombies = []
    score = 0
    spawn_timer = 0
    running = True

    while running:
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        car.move(keys)

        # Spawn zombies
        spawn_timer += 1
        if spawn_timer > 30:  # spawn rate
            zombies.append(Zombie())
            spawn_timer = 0

        # Move zombies
        for zombie in zombies[:]:
            zombie.move()
            if zombie.rect.top > HEIGHT:
                zombies.remove(zombie)
                score += 1  # survived a zombie
            if zombie.rect.colliderect(car.rect):
                game_over(score)

        # Draw everything
        car.draw()
        for zombie in zombies:
            zombie.draw()

        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update
        pygame.display.flip()
        clock.tick(60)

# Game over screen
def game_over(score):
    screen.fill(BLACK)
    over_text = font.render("GAME OVER! Zombies ate your car 🚗💀", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, GREEN)
    screen.blit(over_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 220, HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Run game
game_loop()
