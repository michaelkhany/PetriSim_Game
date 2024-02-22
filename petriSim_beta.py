import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 182, 193)
BACTERIA_SIZE = 10
FOOD_SIZE = 5
MOVE_INCREMENT = 5
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ENEMY_SPEED = 2
SPAWN_FOOD_EVERY = 2000  # milliseconds
RANGE_OF_SIGHT = 100

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Petri Simulator")

# Timer
pygame.time.set_timer(pygame.USEREVENT, SPAWN_FOOD_EVERY)

# Bacteria and food setup
green_bacteria = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BACTERIA_SIZE, BACTERIA_SIZE)
red_bacteria = [pygame.Rect(random.randint(0, SCREEN_WIDTH - BACTERIA_SIZE), random.randint(0, SCREEN_HEIGHT - BACTERIA_SIZE), BACTERIA_SIZE, BACTERIA_SIZE) for _ in range(5)]
food_list = []

# Spawn food function
def spawn_food():
    x = random.randint(0, SCREEN_WIDTH - FOOD_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - FOOD_SIZE)
    food_list.append(pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE))

# Move red bacteria towards nearest food or green bacteria
def move_red_bacteria():
    for red in red_bacteria:
        nearest_target = None
        min_distance = math.inf
        for food in food_list:
            distance = math.hypot(red.centerx - food.centerx, red.centery - food.centery)
            if distance < min_distance:
                min_distance = distance
                nearest_target = food
        distance_to_green = math.hypot(red.centerx - green_bacteria.centerx, red.centery - green_bacteria.centery)
        if distance_to_green < min_distance and distance_to_green < RANGE_OF_SIGHT:
            min_distance = distance_to_green
            nearest_target = green_bacteria
        if nearest_target:
            move_x, move_y = nearest_target.centerx - red.centerx, nearest_target.centery - red.centery
            norm = math.sqrt(move_x ** 2 + move_y ** 2)
            move_x, move_y = move_x / norm, move_y / norm
            red.x += int(move_x * ENEMY_SPEED)
            red.y += int(move_y * ENEMY_SPEED)

# Check collisions
def check_collisions():
    global running
    # Check if green bacteria eats food
    for food in food_list[:]:
        if green_bacteria.colliderect(food):
            food_list.remove(food)
            # Logic for green bacteria multiplying could go here
    
    # Check if red bacteria eats food
    for red in red_bacteria:
        for food in food_list[:]:
            if red.colliderect(food):
                food_list.remove(food)
                # Logic for red bacteria multiplying could go here

    # Check if green bacteria collides with red bacteria
    for red in red_bacteria[:]:
        if green_bacteria.colliderect(red):
            red_bacteria.remove(red)
            # Logic for game over or bacteria removal

    # Win/Lose Conditions
    if not red_bacteria:
        print("You win!")
        running = False
    elif not green_bacteria:
        print("You lose!")
        running = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            spawn_food()

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        green_bacteria.y -= MOVE_INCREMENT
    if keys[pygame.K_s]:
        green_bacteria.y += MOVE_INCREMENT
    if keys[pygame.K_a]:
        green_bacteria.x -= MOVE_INCREMENT
    if keys[pygame.K_d]:
        green_bacteria.x += MOVE_INCREMENT
    if keys[pygame.K_q]:
        running = False
    if keys[pygame.K_e]:
        # Restart or start game logic could go here
        pass

    move_red_bacteria()
    check_collisions()

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    for food in food_list:
        pygame.draw.rect(screen, WHITE, food)
    pygame.draw.rect(screen, GREEN, green_bacteria)
    for red in red_bacteria:
        pygame.draw.rect(screen, RED, red)

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
