import pygame
import sys
import random
import math

# Initialize Pygame and font module
pygame.init()
pygame.font.init()  # Initialize font module

# Create a font object
font_size = 20
game_font = pygame.font.SysFont('Arial', font_size)

# Define text color
text_color = (0, 0, 0)  # Black color

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 182, 193)
BACTERIA_SIZE = 10
FOOD_SIZE = 5
MOVE_INCREMENT = 5
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ENEMY_SPEED = 2
ALLY_SPEED = 2
SPAWN_FOOD_EVERY = 2000  # milliseconds
RANGE_OF_SIGHT = 100
MULTIPLY_RATE = 2  # How much the bacteria multiplies by

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Petri Simulator")

# Timer
pygame.time.set_timer(pygame.USEREVENT, SPAWN_FOOD_EVERY)

# Instructions draw setup
def draw_instructions():
    instructions = [
        "Use W, A, S, D to move",
        "Q to quit",
        "Avoid Red, Eat White to multiply"
    ]
    for i, line in enumerate(instructions):
        text_surface = game_font.render(line, True, text_color)
        # Adjust the y position based on how many lines of text there are
        screen.blit(text_surface, (5, SCREEN_HEIGHT - (len(instructions) - i) * (font_size + 5)))


# Bacteria and food setup
player_bacteria = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BACTERIA_SIZE, BACTERIA_SIZE)
green_bacteria = []
red_bacteria = [pygame.Rect(random.randint(0, SCREEN_WIDTH - BACTERIA_SIZE), random.randint(0, SCREEN_HEIGHT - BACTERIA_SIZE), BACTERIA_SIZE, BACTERIA_SIZE) for _ in range(5)]
food_list = []

# Spawn food function
def spawn_food():
    x = random.randint(0, SCREEN_WIDTH - FOOD_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - FOOD_SIZE)
    food_list.append(pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE))

# Move bacteria towards nearest food or opposite bacteria
def move_bacteria():
    # Move red bacteria towards nearest food or player-controlled bacteria
    for red in red_bacteria:
        nearest_target, _ = find_nearest_target(red, food_list + [player_bacteria])
        if nearest_target:
            move_bacteria_towards(red, nearest_target, ENEMY_SPEED)

    # Move green bacteria towards nearest food
    for green in green_bacteria:
        nearest_target, _ = find_nearest_target(green, food_list)
        if nearest_target:
            move_bacteria_towards(green, nearest_target, ALLY_SPEED)

def find_nearest_target(bacteria, targets):
    nearest_target = None
    min_distance = math.inf
    for target in targets:
        distance = math.hypot(bacteria.centerx - target.centerx, bacteria.centery - target.centery)
        if distance < min_distance:
            min_distance = distance
            nearest_target = target
    return nearest_target, min_distance

def move_bacteria_towards(bacteria, target, speed):
    move_x, move_y = target.centerx - bacteria.centerx, target.centery - bacteria.centery
    norm = math.sqrt(move_x ** 2 + move_y ** 2) if math.sqrt(move_x ** 2 + move_y ** 2) > 0 else 1
    move_x, move_y = move_x / norm, move_y / norm
    bacteria.x += int(move_x * speed)
    bacteria.y += int(move_y * speed)

# Check collisions and multiply bacteria
def check_collisions_and_multiply():
    global player_bacteria, green_bacteria, red_bacteria, running

    # Player bacteria eats food
    for food in food_list[:]:
        if player_bacteria.colliderect(food):
            food_list.remove(food)
            # Multiply player bacteria (turning into green bacteria)
            for _ in range(MULTIPLY_RATE - 1):
                new_bacteria = pygame.Rect(player_bacteria.x + random.randint(-5, 5), 
                                           player_bacteria.y + random.randint(-5, 5), 
                                           BACTERIA_SIZE, BACTERIA_SIZE)
                green_bacteria.append(new_bacteria)

    # Green bacteria eats food
    for green in green_bacteria[:]:
        for food in food_list[:]:
            if green.colliderect(food):
                food_list.remove(food)
                # Multiply green bacteria
                new_bacteria = pygame.Rect(green.x + random.randint(-5, 5), 
                                           green.y + random.randint(-5, 5), 
                                           BACTERIA_SIZE, BACTERIA_SIZE)
                green_bacteria.append(new_bacteria)

    # Red bacteria eats food
    for red in red_bacteria[:]:
        for food in food_list[:]:
            if red.colliderect(food):
                food_list.remove(food)
                # Multiply red bacteria
                new_bacteria = pygame.Rect(red.x + random.randint(-5, 5), 
                                           red.y + random.randint(-5, 5), 
                                           BACTERIA_SIZE, BACTERIA_SIZE)
                red_bacteria.append(new_bacteria)

    # Check for collisions between green and red bacteria
    for green in green_bacteria[:]:
        for red in red_bacteria[:]:
            if green.colliderect(red):
                green_bacteria.remove(green)
                red_bacteria.remove(red)
                break  # Break to avoid modifying list during iteration

    # If the player-controlled bacteria collides with red bacteria, both are removed
    player_collided = False
    for red in red_bacteria[:]:
        if player_bacteria.colliderect(red):
            red_bacteria.remove(red)
            player_bacteria = None  # Mark player bacteria as eliminated
            player_collided = True
            break  # Only one collision is needed to remove the player bacteria

    # If player bacteria is eliminated, try to assign a new player bacteria from green ones
    if player_collided:
        if green_bacteria:
            player_bacteria = green_bacteria.pop(0)  # Assign first green bacteria as new player
        else:
            print("You lose!")
            running = False
            return  # Exit the function to avoid further processing

    # Win Condition
    if not red_bacteria:
        print("You win!")
        running = False

# Game loop flag
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            spawn_food()

    # Key handling for player bacteria movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_bacteria.y -= MOVE_INCREMENT if player_bacteria.y - MOVE_INCREMENT > 0 else 0
    if keys[pygame.K_s]:
        player_bacteria.y += MOVE_INCREMENT if player_bacteria.y + MOVE_INCREMENT + BACTERIA_SIZE < SCREEN_HEIGHT else 0
    if keys[pygame.K_a]:
        player_bacteria.x -= MOVE_INCREMENT if player_bacteria.x - MOVE_INCREMENT > 0 else 0
    if keys[pygame.K_d]:
        player_bacteria.x += MOVE_INCREMENT if player_bacteria.x + MOVE_INCREMENT + BACTERIA_SIZE < SCREEN_WIDTH else 0
    if keys[pygame.K_q]:
        running = False

    # Move all bacteria
    move_bacteria()

    # Check for collisions and handle multiplication
    check_collisions_and_multiply()

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BLUE, player_bacteria)  # Draw the player-controlled bacteria
    for food in food_list:
        pygame.draw.rect(screen, WHITE, food)  # Draw food
    for green in green_bacteria:
        pygame.draw.rect(screen, GREEN, green)  # Draw green bacteria
    for red in red_bacteria:
        pygame.draw.rect(screen, RED, red)  # Draw red bacteria

    # Draw instructions
    draw_instructions()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(30)

# Quit the game
pygame.quit()
sys.exit()
