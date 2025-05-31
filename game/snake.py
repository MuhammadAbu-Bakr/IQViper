import pygame
import random
import sys
import time
import json
import os
from datetime import datetime

pygame.init()

# Constants
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
CELL_SIZE = 25
SCORES_FILE = "scores.json"
MENU_BG = (50, 50, 50, 200)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Screen size options
SCREEN_SIZES = [
    (800, 600),   # Default
    (1024, 768),  # Medium
    (1280, 720),  # HD
    (1920, 1080)  # Full HD
]

# Initialize screen and clock
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
pygame.display.set_caption("Smart Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
menu_font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 16)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = LIGHT_GRAY if self.is_hovered else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = menu_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.action:
                self.action()
                return True
        return False

def draw_pause_menu(buttons):
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_BG)
    screen.blit(overlay, (0, 0))
    
    # Draw menu title
    title = menu_font.render("PAUSED", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)

def save_score(score, elapsed_time):
    try:
        # Create scores directory if it doesn't exist
        scores_dir = "data"
        if not os.path.exists(scores_dir):
            os.makedirs(scores_dir)
        
        scores_file = os.path.join(scores_dir, "scores.json")
        
        # Load existing scores
        if os.path.exists(scores_file):
            with open(scores_file, 'r') as f:
                scores = json.load(f)
        else:
            scores = []
        
        # Add new score
        scores.append({
            'score': score,
            'time': elapsed_time,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Sort by score (highest first)
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top 10 scores
        scores = scores[:10]
        
        # Save scores
        with open(scores_file, 'w') as f:
            json.dump(scores, f, indent=4)
            
        print(f"Score saved: {score} points")
    except Exception as e:
        print(f"Error saving score: {e}")

def show_leaderboard():
    try:
        scores_file = os.path.join("data", "scores.json")
        if not os.path.exists(scores_file):
            return
        
        with open(scores_file, 'r') as f:
            scores = json.load(f)
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(MENU_BG)
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title = menu_font.render("LEADERBOARD", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Calculate column positions based on screen width
        col_width = WIDTH // 4
        x_positions = [col_width * i + col_width//4 for i in range(4)]
        
        # Draw headers
        headers = ["Rank", "Score", "Time", "Date"]
        for i, header in enumerate(headers):
            header_text = small_font.render(header, True, WHITE)
            screen.blit(header_text, (x_positions[i], 100))
        
        # Draw scores
        for i, score_data in enumerate(scores):
            y_pos = 130 + i * 30
            rank = small_font.render(str(i + 1), True, WHITE)
            score = small_font.render(str(score_data['score']), True, WHITE)
            time_str = small_font.render(f"{int(score_data['time']//60)}:{int(score_data['time']%60):02d}", True, WHITE)
            date = small_font.render(score_data['date'], True, WHITE)
            
            screen.blit(rank, (x_positions[0], y_pos))
            screen.blit(score, (x_positions[1], y_pos))
            screen.blit(time_str, (x_positions[2], y_pos))
            screen.blit(date, (x_positions[3], y_pos))
        
        # Draw back button
        back_button = Button(WIDTH//2 - 100, HEIGHT - 50, 200, 40, "Back", lambda: None)
        back_button.draw(screen)
        
        pygame.display.flip()
        
        # Wait for back button click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.rect.collidepoint(event.pos):
                        waiting = False
    
    except Exception as e:
        print(f"Error showing leaderboard: {e}")

def show_about():
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_BG)
    screen.blit(overlay, (0, 0))
    
    # About text
    about_text = [
        "Smart Snake Game",
        "",
        "A Python implementation of the classic Snake game",
        "with AI-powered movement and modern features.",
        "",
        "Features:",
        "- AI-controlled snake movement",
        "- Score tracking and leaderboard",
        "- Time tracking",
        "- Pause menu system",
        "- Customizable screen size",
        "",
        "Controls:",
        "- Press 'P' to pause/unpause",
        "- ESC to exit menus",
        "",
        "Created with Pygame"
    ]
    
    # Draw title
    title = menu_font.render("ABOUT", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, 50))
    screen.blit(title, title_rect)
    
    # Draw about text
    for i, line in enumerate(about_text):
        text = small_font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH//2, 150 + i * 25))
        screen.blit(text, text_rect)
    
    # Draw back button
    back_button = Button(WIDTH//2 - 100, HEIGHT - 50, 200, 40, "Back", lambda: None)
    back_button.draw(screen)
    
    pygame.display.flip()
    
    # Wait for back button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    waiting = False

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

def draw_score_and_time(score, elapsed_time):
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
    screen.blit(time_text, (150, 10))

def draw_menu(buttons):
    # Draw menu background
    menu_rect = pygame.Rect(0, 0, WIDTH, 30)
    pygame.draw.rect(screen, LIGHT_GRAY, menu_rect)
    pygame.draw.line(screen, BLACK, (0, 30), (WIDTH, 30), 2)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)

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
    
    # Save the final score
    save_score(score, time.time() - start_time)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def save_settings(width, height):
    try:
        settings_dir = "data"
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        settings_file = os.path.join(settings_dir, "settings.json")
        settings = {
            'width': width,
            'height': height
        }
        
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
            
        print(f"Settings saved: {width}x{height}")
    except Exception as e:
        print(f"Error saving settings: {e}")

def load_settings():
    try:
        settings_file = os.path.join("data", "settings.json")
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                return settings.get('width', DEFAULT_WIDTH), settings.get('height', DEFAULT_HEIGHT)
    except Exception as e:
        print(f"Error loading settings: {e}")
    return DEFAULT_WIDTH, DEFAULT_HEIGHT

def show_settings():
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_BG)
    screen.blit(overlay, (0, 0))
    
    # Draw title
    title = menu_font.render("SETTINGS", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, 50))
    screen.blit(title, title_rect)
    
    # Draw screen size options
    size_text = small_font.render("Screen Size:", True, WHITE)
    screen.blit(size_text, (WIDTH//2 - 100, 150))
    
    # Create size option buttons
    size_buttons = []
    for i, (w, h) in enumerate(SCREEN_SIZES):
        button = Button(
            WIDTH//2 - 100,
            200 + i * 60,
            200,
            40,
            f"{w}x{h}",
            lambda w=w, h=h: [save_settings(w, h), pygame.display.set_mode((w, h)), update_screen_size(w, h)]
        )
        size_buttons.append(button)
    
    # Draw back button
    back_button = Button(WIDTH//2 - 100, HEIGHT - 50, 200, 40, "Back", lambda: None)
    
    # Wait for button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check size buttons
                for button in size_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.action()
                        waiting = False
                        break
                # Check back button
                if back_button.rect.collidepoint(event.pos):
                    waiting = False
        
        # Draw everything
        screen.blit(overlay, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(size_text, (WIDTH//2 - 100, 150))
        
        for button in size_buttons:
            button.draw(screen)
        back_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def update_screen_size(new_width, new_height):
    global WIDTH, HEIGHT, screen, pause_buttons
    
    WIDTH = new_width
    HEIGHT = new_height
    
    # Update screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Update pause menu buttons
    button_width = min(200, WIDTH // 4)  # Ensure buttons don't get too wide
    button_height = min(50, HEIGHT // 12)  # Ensure buttons don't get too tall
    button_x = WIDTH//2 - button_width//2
    
    pause_buttons = [
        Button(button_x, HEIGHT//2 - 150, button_width, button_height, "Leaderboard", show_leaderboard),
        Button(button_x, HEIGHT//2 - 50, button_width, button_height, "Settings", show_settings),
        Button(button_x, HEIGHT//2 + 50, button_width, button_height, "About", show_about),
        Button(button_x, HEIGHT//2 + 150, button_width, button_height, "Exit", lambda: [save_score(score, time.time() - start_time), sys.exit()])
    ]

def main():
    global score, start_time, WIDTH, HEIGHT  # Make these accessible to other functions
    
    # Load saved settings
    WIDTH, HEIGHT = load_settings()
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smart Snake Game")
    clock = pygame.time.Clock()
    
    # Initialize game state
    snake = [(WIDTH//2, HEIGHT//2)]
    direction = (CELL_SIZE, 0)
    food_pos = get_food_position(snake)
    score = 0
    running = True
    paused = False
    last_move_time = time.time()
    move_delay = 0.1
    start_time = time.time()

    # Create pause menu buttons
    button_width = 200
    button_height = 50
    button_x = WIDTH//2 - button_width//2
    button_spacing = 20
    
    pause_buttons = [
        Button(button_x, HEIGHT//2 - 100, button_width, button_height, "Leaderboard", show_leaderboard),
        Button(button_x, HEIGHT//2, button_width, button_height, "Settings", show_settings),
        Button(button_x, HEIGHT//2 + 100, button_width, button_height, "About", show_about),
        Button(button_x, HEIGHT//2 + 200, button_width, button_height, "Exit", lambda: [save_score(score, time.time() - start_time), sys.exit()])
    ]

    try:
        while running:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_score(score, time.time() - start_time)
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                elif paused:
                    for button in pause_buttons:
                        if button.handle_event(event):
                            button.action()

            if not paused:
                # AI movement
                if current_time - last_move_time >= move_delay:
                    direction = get_next_move(snake, food_pos)
                    if direction is None:
                        game_over()
                    
                    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
                    snake.insert(0, head)

                    if head == food_pos:
                        score += 1
                        food_pos = get_food_position(snake)
                        move_delay = max(0.05, move_delay - 0.001)
                    else:
                        snake.pop()

                    last_move_time = current_time

            # Draw everything
            screen.fill(BLACK)
            draw_snake(snake)
            draw_food(food_pos)
            draw_score_and_time(score, elapsed_time)
            
            if paused:
                draw_pause_menu(pause_buttons)
            
            pygame.display.flip()
            clock.tick(60)

    finally:
        # Save score when exiting
        save_score(score, time.time() - start_time)
        pygame.quit()

if __name__ == "__main__":
    main() 