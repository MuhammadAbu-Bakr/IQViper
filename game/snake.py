import pygame
import random
import sys
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 25

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

def get_food_position(snake):
    while True:
        pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
               random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        if pos not in snake:
            return pos

def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = BLUE if i == 0 else GREEN  # Head is blue, body is green
        pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(pos):
    pygame.draw.rect(screen, RED, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def is_safe_move(head, snake_body):
    # Check if the move is within bounds
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT):
        return False
    
    # Check if the move collides with snake body
    if head in snake_body:
        return False
    
    return True

def get_next_move(snake, food_pos):
    head = snake[0]
    possible_moves = [
        (CELL_SIZE, 0),   # Right
        (-CELL_SIZE, 0),  # Left
        (0, CELL_SIZE),   # Down
        (0, -CELL_SIZE)   # Up
    ]
    
    # Calculate distances to food for each possible move
    best_move = None
    min_distance = float('inf')
    
    for move in possible_moves:
        new_head = (head[0] + move[0], head[1] + move[1])
        
        # Skip if move is not safe
        if not is_safe_move(new_head, snake[1:]):
            continue
        
        # Calculate Manhattan distance to food
        distance = abs(new_head[0] - food_pos[0]) + abs(new_head[1] - food_pos[1])
        
        # If this move gets us closer to food, consider it
        if distance < min_distance:
            min_distance = distance
            best_move = move
    
    # If no safe move found, try to find any safe move
    if best_move is None:
        for move in possible_moves:
            new_head = (head[0] + move[0], head[1] + move[1])
            if is_safe_move(new_head, snake[1:]):
                return move
    
    return best_move

def game_over():
    text = font.render("Game Over! Press ESC to Quit", True, RED)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(1000)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def main():
    # Initialize game state
    snake = [(100, 100), (75, 100), (50, 100)]
    direction = (CELL_SIZE, 0)
    food_pos = get_food_position(snake)
    score = 0
    running = True
    last_move_time = time.time()
    move_delay = 0.1  # Time between moves in seconds

    while running:
        current_time = time.time()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # AI movement
        if current_time - last_move_time >= move_delay:
            direction = get_next_move(snake, food_pos)
            if direction is None:  # No safe moves available
                game_over()
            
            # Move snake
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, head)

            # Check for food collision
            if head == food_pos:
                score += 1
                food_pos = get_food_position(snake)
                # Increase speed slightly with each food eaten
                move_delay = max(0.05, move_delay - 0.001)
            else:
                snake.pop()

            last_move_time = current_time

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food_pos)
        draw_score(score)
        pygame.display.flip()
        clock.tick(60)  # Cap at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main() 