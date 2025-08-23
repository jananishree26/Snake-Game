import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Game window
pygame.display.set_caption("Snake Game by Janani")
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
clock = pygame.time.Clock()
snake_speed = 15   # ✅ control speed of snake

# Snake default position & body
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Direction control
direction = 'RIGHT'
change_to = direction

# Food position
food_position = [random.randrange(1, (window_x//10)) * 10,
                 random.randrange(1, (window_y//10)) * 10]
food_spawn = True

# Score
score = 0

# Function to display score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_x/10, 15)
    else:
        score_rect.midtop = (window_x/2, window_y/4)
    game_window.blit(score_surface, score_rect)

# Game Over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    go_surface = my_font.render('Game Over! Your Score is: ' + str(score), True, red)
    go_rect = go_surface.get_rect()
    go_rect.midtop = (window_x/2, window_y/4)
    game_window.blit(go_surface, go_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main Function
def gameLoop():
    global direction, change_to, snake_position, snake_body
    global food_position, food_spawn, score

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # No reverse direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn new food
        if not food_spawn:
            food_position = [random.randrange(1, (window_x//10)) * 10,
                             random.randrange(1, (window_y//10)) * 10]
        food_spawn = True

        # Background
        game_window.fill(black)

        # Draw snake body
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw food
        pygame.draw.rect(game_window, white, pygame.Rect(food_position[0], food_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > (window_x-10):
            game_over()
        if snake_position[1] < 0 or snake_position[1] > (window_y-10):
            game_over()

        # Check collision with itself
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        # Display score
        show_score(1, white, 'consolas', 20)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second / Refresh Rate
        clock.tick(snake_speed)

# Start the game
gameLoop()
