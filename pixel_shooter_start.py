import pygame
import time 

pygame.init()
# Adjusted window size for a widescreen look
window_size = (1920,1080)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pixel Shooter")

# Colors
BG_COLOR = (10, 15, 40)
TITLE_GRADIENT_TOP = (255, 220, 40)
TITLE_GRADIENT_BOTTOM = (255, 60, 40)
OUTLINE_COLOR = (0, 0, 0)
TEXT_COLOR = (160, 200, 220)
BUTTON_COLOR = (30, 40, 80)
BUTTON_OUTLINE = (80, 110, 180)
BUTTON_TEXT = (220, 230, 255)

# Load font (replace with a pixel font file for best results)
font_title = pygame.font.SysFont("Arial", 120, bold=True)
font_subtitle = pygame.font.SysFont("Arial", 32, bold=True)
font_button = pygame.font.SysFont("Arial", 40, bold=True)

# Load the background image for the game
try:
    background_img = pygame.image.load('grafiki/tlo_gry.png').convert()
    background_img = pygame.transform.scale(background_img, window_size)
except pygame.error:
    print("Error loading background image. Ensure 'grafiki/tlo_gry.png' exists.")
    background_img = None

# Load the enemy image
try:
    enemy_img = pygame.image.load('grafiki/enemy.png').convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (80, 80))  # Resize enemy to 80x80
except pygame.error:
    print("Error loading enemy image. Ensure 'grafiki/enemy.png' exists.")
    enemy_img = None

# Define button properties and create the rectangles
btn_w, btn_h = 220, 70
btn_y = 380
btn_gap = 30
play_btn_rect = pygame.Rect(window_size[0]//2 - btn_w - btn_gap//2, btn_y, btn_w, btn_h)
settings_btn_rect = pygame.Rect(window_size[0]//2 + btn_gap//2, btn_y, btn_w, btn_h)

# Game state variable
GAME_STATE = "menu"  # Can be "menu" or "game"

# Enemy properties
enemy_x = 1200
enemy_y = 400

enemy_speed_x = 0.17
enemy_speed_y = 3

def draw_gradient_text(text, font, pos, top_color, bottom_color, outline_color):
    # Render outline by blitting text at offsets
    outline_surface = font.render(text, True, outline_color)
    for dx in [-4, 0, 4]:
        for dy in [-4, 0, 4]:
            if dx != 0 or dy != 0:
                screen.blit(outline_surface, (pos[0] + dx, pos[1] + dy))

    # Render base text with a gradient
    base_surface = font.render(text, True, top_color).convert_alpha()
    gradient_surface = pygame.Surface(base_surface.get_size(), pygame.SRCALPHA)
    for y in range(base_surface.get_height()):
        ratio = y / base_surface.get_height()
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(gradient_surface, (r, g, b, 255), (0, y), (base_surface.get_width(), y))
    
    base_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(base_surface, pos)

def draw_button(text, rect):
    pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=5)
    pygame.draw.rect(screen, BUTTON_OUTLINE, rect, 4, border_radius=5)
    txt = font_button.render(text, True, BUTTON_TEXT)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

def draw_menu():
    screen.fill(BG_COLOR)
    
    # --- Title ---
    title_text = "PIXEL SHOOTER"
    title_surface = font_title.render(title_text, True, (0,0,0)) # for sizing
    title_pos = (window_size[0] // 2 - title_surface.get_width() // 2, 120)
    draw_gradient_text(title_text, font_title, title_pos, TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM, OUTLINE_COLOR)

    # --- Subtitle ---
    subtitle = font_subtitle.render("@AATNDAY & NEOJHADS", True, TEXT_COLOR)
    subtitle_rect = subtitle.get_rect(center=(window_size[0] // 2, 320))
    screen.blit(subtitle, subtitle_rect)

    # --- Buttons ---
    draw_button("PLAY", play_btn_rect)
    draw_button("SETTINGS", settings_btn_rect)

def draw_game():
    global enemy_x, enemy_y, enemy_speed_x

    # Draw the background
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((50, 50, 50))  # Fallback background color

    # Draw the enemy
    if enemy_img:
        screen.blit(enemy_img, (enemy_x, enemy_y))

    # Move the enemy from right to left
    enemy_x -= enemy_speed_x

    # Reset the enemy's position when it goes off-screen
    if enemy_x + 80 < 0:  # 80 is the width of the enemy
        enemy_x = window_size[0]  # Reset to the right side of the screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE == "menu":
                if play_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "game"  # Switch to game state
                elif settings_btn_rect.collidepoint(event.pos):
                    print("Settings button clicked!")

    if GAME_STATE == "menu":
        draw_menu()
    elif GAME_STATE == "game":
        draw_game()

# Load the main character image
try:
    main_character_img = pygame.image.load('grafiki/main_character.png').convert_alpha()
    main_character_img = pygame.transform.scale(main_character_img, (80, 80))  # Resize character to 80x80
except pygame.error:
    print("Error loading main character image. Ensure 'grafiki/main_character.png' exists.")
    main_character_img = None

# Main character properties (fixed position)
main_character_x = 100
main_character_y = 400

def draw_game():
    global enemy_x, enemy_y, enemy_speed_x

    # Draw the background
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((50, 50, 50))  # Fallback background color

    # Draw the enemy
    if enemy_img:
        screen.blit(enemy_img, (enemy_x, enemy_y))

    # Move the enemy from right to left
    enemy_x -= enemy_speed_x

    # Reset the enemy's position when it goes off-screen
    if enemy_x + 80 < 0:  # 80 is the width of the enemy
        enemy_x = window_size[0]  # Reset to the right side of the screen

    # Draw the main character at a fixed position
    if main_character_img:
        screen.blit(main_character_img, (main_character_x, main_character_y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE == "menu":
                if play_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "game"  # Switch to game state
                elif settings_btn_rect.collidepoint(event.pos):
                    print("Settings button clicked!")

    if GAME_STATE == "menu":
        draw_menu()
    elif GAME_STATE == "game":
        draw_game()







# Add a font for the "Game Over" message
font_game_over = pygame.font.SysFont("Arial", 80, bold=True)

# Function to display the "Game Over" message
def display_game_over():
    game_over_text = font_game_over.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    screen.blit(game_over_text, game_over_rect)

def draw_game():
    global enemy_x, enemy_y, enemy_speed_x, running

    # Draw the background
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((50, 50, 50))  # Fallback background color

    # Draw the enemy
    if enemy_img:
        screen.blit(enemy_img, (enemy_x, enemy_y))

    # Move the enemy from right to left
    enemy_x -= enemy_speed_x

    # Reset the enemy's position when it goes off-screen
    if enemy_x + 80 < 0:  # 80 is the width of the enemy
        enemy_x = window_size[0]  # Reset to the right side of the screen

    # Draw the main character at a fixed position
    if main_character_img:
        screen.blit(main_character_img, (main_character_x, main_character_y))

    # Check for collision between the enemy and the main character
    main_character_rect = pygame.Rect(main_character_x, main_character_y, 80, 80)  # Main character's rectangle
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 80, 80)  # Enemy's rectangle

    if main_character_rect.colliderect(enemy_rect):  # Check for collision
        display_game_over()  # Display "Game Over" message
        running = False  # Stop the game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE == "menu":
                if play_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "game"  # Switch to game state
                elif settings_btn_rect.collidepoint(event.pos):
                    print("Settings button clicked!")

    if GAME_STATE == "menu":
        draw_menu()
    elif GAME_STATE == "game":
        draw_game()

# Add a new game state for settings
GAME_STATE = "menu"  # Can be "menu", "game", or "settings"

def draw_settings():
    """Function to draw the settings screen."""
    screen.fill((20, 20, 60))  # Background color for settings
    settings_text = font_title.render("SETTINGS", True, (255, 255, 255))
    settings_rect = settings_text.get_rect(center=(window_size[0] // 2, 100))
    screen.blit(settings_text, settings_rect)

    # Example settings options (you can add more functionality here)
    option_text = font_subtitle.render("Press ESC to return to the menu", True, (200, 200, 200))
    option_rect = option_text.get_rect(center=(window_size[0] // 2, 300))
    screen.blit(option_text, option_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE == "menu":
                if play_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "game"  # Switch to game state
                elif settings_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "settings"  # Switch to settings state
        if event.type == pygame.KEYDOWN:
            if GAME_STATE == "settings" and event.key == pygame.K_ESCAPE:  # Press ESC to return to menu
                GAME_STATE = "menu"

    if GAME_STATE == "menu":
        draw_menu()
    elif GAME_STATE == "game":
        draw_game()
    elif GAME_STATE == "settings":
        draw_settings()

pygame.display.flip()

pygame.quit()