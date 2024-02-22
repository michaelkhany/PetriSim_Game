import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 182, 193)  # Pink color for the agar
BACTERIA_SIZE = 10
FOOD_SIZE = 1
MOVE_INCREMENT = 10
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Petri Simulator")

# Bacteria setup
green_bacteria = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BACTERIA_SIZE, BACTERIA_SIZE)
bacteria_velocity = {'x': 0, 'y': 0}

# Food setup
food_list = []

# Function to spawn food
def spawn_food():
    x = random.randint(0, SCREEN_WIDTH - FOOD_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - FOOD_SIZE)
    food_list.append(pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE))

# Initial food spawn
for _ in range(10):  # Spawn 10 initial food particles
    spawn_food()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        bacteria_velocity['y'] = -MOVE_INCREMENT
    elif keys[pygame.K_s]:
        bacteria_velocity['y'] = MOVE_INCREMENT
    else:
        bacteria_velocity['y'] = 0
    
    if keys[pygame.K_a]:
        bacteria_velocity['x'] = -MOVE_INCREMENT
    elif keys[pygame.K_d]:
        bacteria_velocity['x'] = MOVE_INCREMENT
    else:
        bacteria_velocity['x'] = 0

    # Update bacteria position
    green_bacteria.x += bacteria_velocity['x']
    green_bacteria.y += bacteria_velocity['y']

    # Boundaries check
    if green_bacteria.left < 0:
        green_bacteria.left = 0
    if green_bacteria.right > SCREEN_WIDTH:
        green_bacteria.right = SCREEN_WIDTH
    if green_bacteria.top < 0:
        green_bacteria.top = 0
    if green_bacteria.bottom > SCREEN_HEIGHT:
        green_bacteria.bottom = SCREEN_HEIGHT

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, GREEN, green_bacteria)
    
    for food in food_list:
        pygame.draw.rect(screen, WHITE, food)

    # Update the display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
