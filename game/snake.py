import pygame
import random
import sys
import time
import json
import os
from datetime import datetime
import math

pygame.init()


DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
CELL_SIZE = 25
SCORES_FILE = "scores.json"
MENU_BG = (20, 20, 30, 230)


icon_path = os.path.join("assets", "icon.png")
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

# Colors
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 69, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_BLUE = (25, 25, 112)
GOLD = (255, 215, 0)
GRID_COLOR = (40, 40, 40)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 16, 240)
NEON_GREEN = (57, 255, 20)


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
font = pygame.font.SysFont("Arial", 24, bold=True)
menu_font = pygame.font.SysFont("Arial", 32, bold=True)
small_font = pygame.font.SysFont("Arial", 16, bold=True)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        self.life = 1.0
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 0.02
        self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life * 255)
            color = (*self.color[:3], alpha)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.animation_offset = 0
        self.animation_speed = 0.2
        self.particles = []

    def draw(self, surface):
        if self.is_hovered:
            self.animation_offset = min(self.animation_offset + self.animation_speed, 1)
            if random.random() < 0.1:
                self.particles.append(Particle(
                    random.randint(self.rect.left, self.rect.right),
                    random.randint(self.rect.top, self.rect.bottom),
                    NEON_BLUE
                ))
        else:
            self.animation_offset = max(self.animation_offset - self.animation_speed, 0)

        color = self.lerp_color(LIGHT_GRAY, NEON_BLUE, self.animation_offset)
        border_color = self.lerp_color(GRAY, WHITE, self.animation_offset)
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)
        
        text_surface = menu_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
            particle.draw(surface)

    def lerp_color(self, color1, color2, t):
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.action:
                self.action()
                return True
        return False

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        alpha = int(128 + 127 * math.sin(time.time() * 2 + x * 0.01))
        color = (*GRID_COLOR[:3], alpha)
        pygame.draw.line(screen, color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        alpha = int(128 + 127 * math.sin(time.time() * 2 + y * 0.01))
        color = (*GRID_COLOR[:3], alpha)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def is_safe_move(head, snake_body):
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT):
        return False
    
    if head in snake_body:
        return False
    
    return True

def draw_snake(snake):
    for i, segment in enumerate(snake):
        if i == 0:
            color = NEON_BLUE
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE), border_radius=5)
            pygame.draw.rect(screen, WHITE, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE), 2, border_radius=5)
        else:
            color = NEON_GREEN
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE), border_radius=3)

def draw_food(pos):
    radius = CELL_SIZE//2
    center = (pos[0] + radius, pos[1] + radius)
    
    # Draw glow effect
    for r in range(radius + 5, radius - 5, -1):
        alpha = int(255 * (1 - (r - radius + 5) / 10))
        color = (*NEON_PINK[:3], alpha)
        pygame.draw.circle(screen, color, center, r)
    
    # Draw main food circle
    pygame.draw.circle(screen, NEON_PINK, center, radius)
    pygame.draw.circle(screen, WHITE, center, radius, 2)

def draw_score_and_time(score, elapsed_time):
    # Draw score with glow effect
    score_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
    score_bg.fill((0, 0, 0, 128))
    screen.blit(score_bg, (10, 10))
    
    score_text = font.render(f"Score: {score}", True, NEON_BLUE)
    screen.blit(score_text, (20, 15))
    
    # Draw time with glow effect
    time_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
    time_bg.fill((0, 0, 0, 128))
    screen.blit(time_bg, (220, 10))
    
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, NEON_BLUE)
    screen.blit(time_text, (230, 15))

def draw_pause_menu(buttons):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_BG)
    screen.blit(overlay, (0, 0))
    
    # Draw animated title
    title = menu_font.render("PAUSED", True, NEON_BLUE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
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
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(MENU_BG)
        screen.blit(overlay, (0, 0))
        
        title = menu_font.render("LEADERBOARD", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        col_width = WIDTH // 4
        x_positions = [col_width * i + col_width//4 for i in range(4)]
        
        headers = ["Rank", "Score", "Time", "Date"]
        for i, header in enumerate(headers):
            header_text = small_font.render(header, True, GOLD)
            screen.blit(header_text, (x_positions[i], 100))
        
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
        
        back_button = Button(WIDTH//2 - 100, HEIGHT - 50, 200, 40, "Back", lambda: None)
        back_button.draw(screen)
        
        pygame.display.flip()
        
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
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_BG)
    screen.blit(overlay, (0, 0))
    
    about_text = [
        "Smart Snake Game",
        "",
        "A Python implementation of the classic Snake game",
        "with AI-powered movement and modern features.",
        "",
        "Developer:",
        "- Your very own trusty Computer Scientist Chauadhry Muhammad Abu-Bakr",
        "GitHub profile:",
        "- https://github.com/MuhammadAbu-Bakr",
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
    
    title = menu_font.render("ABOUT", True, GOLD)
    title_rect = title.get_rect(center=(WIDTH//2, 50))
    screen.blit(title, title_rect)
    
    
    line_height = 25
    total_content_height = len(about_text) * line_height
    visible_height = HEIGHT - 200  
    
    
    scroll_y = 0
    max_scroll = max(0, total_content_height - visible_height)
    
    
    content_width = min(WIDTH - 200, 600)  
    content_surface = pygame.Surface((content_width, total_content_height), pygame.SRCALPHA)
    content_surface.fill((0, 0, 0, 0))
    
    
    for i, line in enumerate(about_text):
        text = small_font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(content_width//2, i * line_height + line_height//2))
        content_surface.blit(text, text_rect)
    
    
    back_button = Button(WIDTH//2 - 100, HEIGHT - 50, 200, 40, "Back", lambda: None)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - line_height)
                elif event.key == pygame.K_DOWN:
                    scroll_y = min(max_scroll, scroll_y + line_height)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    waiting = False
                elif event.button == 4:  # Mouse wheel up
                    scroll_y = max(0, scroll_y - line_height)
                elif event.button == 5:  # Mouse wheel down
                    scroll_y = min(max_scroll, scroll_y + line_height)
        
        # Draw everything
        screen.blit(overlay, (0, 0))
        screen.blit(title, title_rect)
        
        # Draw scrollable content centered
        content_x = (WIDTH - content_width) // 2
        visible_rect = pygame.Rect(0, 0, content_width, visible_height)
        screen.blit(content_surface, (content_x, 150 - scroll_y), visible_rect)
        
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def get_food_position(snake):
    while True:
        pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
               random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        if pos not in snake:
            return pos

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
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    text = menu_font.render("Game Over!", True, NEON_PINK)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text, text_rect)
    
    score_text = font.render(f"Final Score: {score}", True, NEON_BLUE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(score_text, score_rect)
    
    exit_text = font.render("Press ESC to Quit", True, WHITE)
    exit_rect = exit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()
    pygame.time.wait(1000)
    
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
    title = menu_font.render("SETTINGS", True, GOLD)
    title_rect = title.get_rect(center=(WIDTH//2, 50))
    screen.blit(title, title_rect)
    
    # Draw screen size options
    size_text = small_font.render("Screen Size:", True, GOLD)
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
            screen.fill(DARK_BLUE)
            draw_grid()
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