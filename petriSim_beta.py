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
BLUE = (0, 0, 255) # Lead-user-controlled ally bacteria color
GREEN = (0, 255, 0) # Ally bacteria color
WHITE = (255, 255, 255) # Food particle color
RED = (255, 0, 0) # Enemy bacteria color
ORANGE = (255, 165, 0)  # Lead-enemy bacteria color
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

# Game state variable
game_state = "start"  # Possible values: "start", "running", "won", "lost"

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

# Function to draw the start, win, or lose banners
def draw_banner():
    if game_state == "start":
        message = 'To start the game, press "s".'
    elif game_state == "won":
        message = 'You won! Press "r" to restart the game.'
    elif game_state == "lost":
        message = 'You lost! Press "r" to restart the game.'
    else:
        return  # No banner to draw if the game is running
    
    text_surface = game_font.render(message, True, text_color)
    rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text_surface, rect)
# Bacteria and food setup
player_bacteria = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BACTERIA_SIZE, BACTERIA_SIZE)
green_bacteria = []
red_bacteria = [pygame.Rect(random.randint(0, SCREEN_WIDTH - BACTERIA_SIZE), random.randint(0, SCREEN_HEIGHT - BACTERIA_SIZE), BACTERIA_SIZE, BACTERIA_SIZE) for _ in range(5)]
orange_bacteria = pygame.Rect(random.randint(0, SCREEN_WIDTH - BACTERIA_SIZE), random.randint(0, SCREEN_HEIGHT - BACTERIA_SIZE), BACTERIA_SIZE, BACTERIA_SIZE)
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
        # Include player_bacteria in the targets list only if it's not None
        targets = food_list + ([player_bacteria] if player_bacteria else [])
        nearest_target, _ = find_nearest_target(red, targets)
        if nearest_target:
            move_bacteria_towards(red, nearest_target, ENEMY_SPEED)

    # Move green bacteria towards nearest food
    for green in green_bacteria:
        nearest_target, _ = find_nearest_target(green, food_list)
        if nearest_target:
            move_bacteria_towards(green, nearest_target, ALLY_SPEED)

    # Move orange bacteria towards player-controlled bacteria
    # Ensure player_bacteria exists before moving orange bacteria towards it
    if player_bacteria:
        move_bacteria_towards(orange_bacteria, player_bacteria, ENEMY_SPEED)

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
    global player_bacteria, green_bacteria, red_bacteria, orange_bacteria, game_state

    # Player bacteria eats food
    for food in food_list[:]:
        if player_bacteria and player_bacteria.colliderect(food):
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

    # Collision between orange bacteria and player or green bacteria
    if player_bacteria and orange_bacteria.colliderect(player_bacteria):
        if green_bacteria:
            # Replace player bacteria with the first green bacteria
            player_bacteria = green_bacteria.pop(0)
        else:
            # End game if no green bacteria left
            game_state = "lost"
            print("You lose!")
            return  # Exit the function to avoid further processing
    for green in green_bacteria[:]:
        if orange_bacteria.colliderect(green):
            green_bacteria.remove(green)
            break  # Break to avoid modifying list during iteration

    # Collision between green and red bacteria
    for green in green_bacteria[:]:
        for red in red_bacteria[:]:
            if green.colliderect(red):
                green_bacteria.remove(green)
                red_bacteria.remove(red)
                break  # Break to avoid modifying list during iteration

    # Check for player collision with red bacteria
    if player_bacteria:
        for red in red_bacteria[:]:
            if player_bacteria.colliderect(red):
                red_bacteria.remove(red)
                if green_bacteria:
                    player_bacteria = green_bacteria.pop(0)  # Replace with a green one
                else:
                    game_state = "lost"
                    print("You lose!")
                    return
                break  # Break since player bacteria has been updated or game is over

    # Win condition
    if not red_bacteria and game_state != "lost":
        game_state = "won"
        print("You win!")

# Reset game function
def reset_game():
    global player_bacteria, green_bacteria, red_bacteria, food_list, game_state
    player_bacteria = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BACTERIA_SIZE, BACTERIA_SIZE)
    green_bacteria = []
    red_bacteria = [pygame.Rect(random.randint(0, SCREEN_WIDTH - BACTERIA_SIZE), random.randint(0, SCREEN_HEIGHT - BACTERIA_SIZE), BACTERIA_SIZE, BACTERIA_SIZE) for _ in range(5)]
    food_list = []
    running = True
    game_state = "running"
    
# Game loop flag
running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT and game_state == "running":
            spawn_food()

    keys = pygame.key.get_pressed()
    if game_state == "start" and keys[pygame.K_s]:
        game_state = "running"
    elif game_state in ["won", "lost"] and keys[pygame.K_r]:
        reset_game()

    if game_state == "running":
        # Handle movement and game logic
        if keys[pygame.K_w]:
            player_bacteria.y -= MOVE_INCREMENT if player_bacteria.y - MOVE_INCREMENT > 0 else 0
        if keys[pygame.K_s]:
            player_bacteria.y += MOVE_INCREMENT if player_bacteria.y + MOVE_INCREMENT + BACTERIA_SIZE < SCREEN_HEIGHT else 0
        if keys[pygame.K_a]:
            player_bacteria.x -= MOVE_INCREMENT if player_bacteria.x - MOVE_INCREMENT > 0 else 0
        if keys[pygame.K_d]:
            player_bacteria.x += MOVE_INCREMENT if player_bacteria.x + MOVE_INCREMENT + BACTERIA_SIZE < SCREEN_WIDTH else 0
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

        move_bacteria()
        check_collisions_and_multiply()

    screen.fill(BACKGROUND_COLOR)

    if game_state == "running":
        if player_bacteria:  # Add this check to ensure player_bacteria exists
            pygame.draw.rect(screen, BLUE, player_bacteria)
        for food in food_list:
            pygame.draw.rect(screen, WHITE, food)
        for green in green_bacteria:
            pygame.draw.rect(screen, GREEN, green)
        for red in red_bacteria:
            pygame.draw.rect(screen, RED, red)
        if orange_bacteria:  # Similarly, ensure orange_bacteria exists before drawing
            pygame.draw.rect(screen, ORANGE, orange_bacteria)
        
        draw_instructions()

    draw_banner()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Outside the game loop, after quitting the game
pygame.quit()
sys.exit()
