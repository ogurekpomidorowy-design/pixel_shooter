import pygame
import time
import random

pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound playback

# --- Tunable constants for very slow jump & fall ---
FPS = 200
JUMP_VELOCITY = -5   # very small (slower ascent)
GRAVITY = 0.08         # very small (slower descent)
# --------------------------------------------------

# Adjusted window size for a widescreen look
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pixel Shooter")

# Clock to stabilize framerate
clock = pygame.time.Clock()

# Colors
BG_COLOR = (10, 15, 40)
BUTTON_COLOR = (30, 40, 80)
BUTTON_OUTLINE = (80, 110, 180)
BUTTON_TEXT = (220, 230, 255)

# Load fonts
font_title = pygame.font.SysFont("Arial", 120, bold=True)
font_button = pygame.font.SysFont("Arial", 40, bold=True)
font_game_over = pygame.font.SysFont("Arial", 80, bold=True)

# Load assets
try:
    background_img = pygame.image.load('grafiki/tlo_gry.png').convert()
    background_img = pygame.transform.scale(background_img, window_size)
except pygame.error:
    print("Error loading background image.")
    background_img = None

try:
    enemy_img = pygame.image.load('grafiki/enemy.png').convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (80, 80))
except pygame.error:
    print("Error loading enemy image.")
    enemy_img = None

try:
    main_character_img = pygame.image.load('grafiki/main_character.png').convert_alpha()
    main_character_img = pygame.transform.scale(main_character_img, (80, 80))
except pygame.error:
    print("Error loading main character image.")
    main_character_img = None

try:
    shoot_character_img = pygame.image.load('grafiki/shoot_ch.png').convert_alpha()
    shoot_character_img = pygame.transform.scale(shoot_character_img, (80, 80))
except pygame.error:
    print("Error loading shooting character image.")
    shoot_character_img = None

try:
    shoot_sound = pygame.mixer.Sound('grafiki/strzal.mp3')
except pygame.error:
    print("Error loading shooting sound.")
    shoot_sound = None

# Ensure button positions are consistent
btn_w, btn_h = 220, 70
btn_y = 380
btn_gap = 30
play_btn_rect = pygame.Rect(window_size[0] // 2 - btn_w - btn_gap // 2, btn_y, btn_w, btn_h)
settings_btn_rect = pygame.Rect(window_size[0] // 2 + btn_gap // 2, btn_y, btn_w, btn_h)
shop_btn_rect = pygame.Rect(window_size[0] // 2 - 100, btn_y + btn_h + btn_gap, 200, 50)  # Adjusted shop button position

# Game state
GAME_STATE = "menu"

# Enemy properties
enemies = []
enemy_spawn_time = 0

# Main character properties
main_character_x = 100
main_character_y = 400
main_character_velocity_y = 0.0
is_jumping = False

# Shooting state
is_shooting = False
shoot_start_time = 0

# Fireball properties
fireballs = []  # List to store active fireballs
fireball_speed = 20  # Speed of the fireball
fireball_radius = 5  # Reduced radius of the fireball

# Define standard size for all weapon images
WEAPON_WIDTH = 120
WEAPON_HEIGHT = 80

# Define shop items with updated images
shop_items = [
    {"name": "Weapon 1", "price": 100, "image": pygame.transform.scale(pygame.image.load('grafiki/1.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 2", "price": 250, "image": pygame.transform.scale(pygame.image.load('grafiki/2.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 3", "price": 500, "image": pygame.transform.scale(pygame.image.load('grafiki/3.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 4", "price": 750, "image": pygame.transform.scale(pygame.image.load('grafiki/4.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 5", "price": 1000, "image": pygame.transform.scale(pygame.image.load('grafiki/5.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 6", "price": 1200, "image": pygame.transform.scale(pygame.image.load('grafiki/6.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 7", "price": 1500, "image": pygame.transform.scale(pygame.image.load('grafiki/7.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))},
    {"name": "Weapon 8", "price": 3000, "image": pygame.transform.scale(pygame.image.load('grafiki/8.png').convert_alpha(), (WEAPON_WIDTH, WEAPON_HEIGHT))}
]

# Reset game variables
def reset_game():
    global enemies, fireballs
    enemies = []
    fireballs = []  # Clear fireballs on reset

# Spawn a new enemy
def spawn_enemy():
    global enemies
    enemy_x = 1200
    enemy_y = 400
    enemy_speed = random.uniform(2, 3)  # Random speed
    enemies.append({"x": enemy_x, "y": enemy_y, "speed": enemy_speed})

# Draw and move enemies
def draw_and_move_enemies():
    global enemies
    for enemy in enemies[:]:
        enemy["x"] -= enemy["speed"]
        if enemy["x"] + 80 < 0:
            enemies.remove(enemy)
        else:
            if enemy_img:
                screen.blit(enemy_img, (int(enemy["x"]), int(enemy["y"])))

# Function to draw and move fireballs
def draw_and_move_fireballs():
    global fireballs, enemies
    for fireball in fireballs[:]:  # Iterate over a copy of the list
        fireball["x"] += fireball_speed  # Move the fireball to the right
        if fireball["x"] > window_size[0]:  # Remove fireball if it goes off-screen
            fireballs.remove(fireball)
        else:
            pygame.draw.circle(screen, (255, 100, 0), (int(fireball["x"]), int(fireball["y"])), fireball_radius)  # Draw the fireball

            # Check collision with enemies
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)  # Assuming enemy size is 80x80
                fireball_rect = pygame.Rect(fireball["x"] - fireball_radius, fireball["y"] - fireball_radius, fireball_radius * 2, fireball_radius * 2)
                if fireball_rect.colliderect(enemy_rect):
                    enemies.remove(enemy)  # Remove enemy on collision
                    if fireball in fireballs:
                        fireballs.remove(fireball)  # Remove fireball on collision
                    break

# Check for collisions
def check_collisions():
    global enemies, is_shooting
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
        main_character_rect = pygame.Rect(main_character_x, main_character_y, 80, 80)

        # Collision with main character
        if main_character_rect.colliderect(enemy_rect):
            display_game_over()
            reset_game()
            return

        # Collision with shot
        if is_shooting:
            if enemy["x"] < main_character_x + 80 and enemy["x"] + 80 > main_character_x:
                if enemy["y"] < main_character_y + 80 and enemy["y"] + 80 > main_character_y:
                    enemies.remove(enemy)

# Display "Game Over"
def display_game_over():
    game_over_text = font_game_over.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Draw the menu
def draw_menu():
    screen.fill(BG_COLOR)
    title_text = "PIXEL SHOOTER"
    title_surface = font_title.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(window_size[0] // 2, 150))
    screen.blit(title_surface, title_rect)

    pygame.draw.rect(screen, BUTTON_COLOR, play_btn_rect, border_radius=10)
    pygame.draw.rect(screen, BUTTON_OUTLINE, play_btn_rect, 4, border_radius=10)
    play_text = font_button.render("PLAY", True, BUTTON_TEXT)
    play_text_rect = play_text.get_rect(center=play_btn_rect.center)
    screen.blit(play_text, play_text_rect)

    pygame.draw.rect(screen, BUTTON_COLOR, settings_btn_rect, border_radius=10)
    pygame.draw.rect(screen, BUTTON_OUTLINE, settings_btn_rect, 4, border_radius=10)
    settings_text = font_button.render("SETTINGS", True, BUTTON_TEXT)
    settings_text_rect = settings_text.get_rect(center=settings_btn_rect.center)
    screen.blit(settings_text, settings_text_rect)

    # Draw the shop button
    pygame.draw.rect(screen, BUTTON_COLOR, shop_btn_rect, border_radius=10)
    pygame.draw.rect(screen, BUTTON_OUTLINE, shop_btn_rect, 4, border_radius=10)
    shop_text = font_button.render("SHOP", True, BUTTON_TEXT)
    shop_text_rect = shop_text.get_rect(center=shop_btn_rect.center)
    screen.blit(shop_text, shop_text_rect)

# Draw the game
def draw_game():
    global enemy_spawn_time, is_shooting, shoot_start_time

    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((50, 50, 50))  # Fallback background color

    # Spawn a new enemy every 0.5 to 1 second
    current_time = pygame.time.get_ticks()
    if current_time - enemy_spawn_time > random.randint(500, 1000):
        spawn_enemy()
        enemy_spawn_time = current_time

    # Draw and move all enemies
    draw_and_move_enemies()

    # Draw and move all fireballs
    draw_and_move_fireballs()

    # Draw the main character
    if is_shooting and time.time() - shoot_start_time < 0.1:  # Check if shooting state is active
        if shoot_character_img:
            screen.blit(shoot_character_img, (int(main_character_x), int(main_character_y)))
    else:
        is_shooting = False  # Reset shooting state after 0.1 seconds
        if main_character_img:
            screen.blit(main_character_img, (int(main_character_x), int(main_character_y)))

    # Check for collisions with all enemies
    check_collisions()

# Draw the shop screen
def draw_shop():
    screen.fill(BG_COLOR)
    title_text = "SHOP"
    title_surface = font_title.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(window_size[0] // 2, 50))
    screen.blit(title_surface, title_rect)

    # Display shop items in a grid
    rows, cols = 2, 4  # 2 rows and 4 columns
    total_padding_x = window_size[0] - (cols * WEAPON_WIDTH)
    padding_x = total_padding_x // (cols + 1)  # Distribute padding evenly
    padding_y = 100  # Vertical padding between rows
    start_y = 120  # Starting Y position

    for i, item in enumerate(shop_items):
        col = i % cols
        row = i // cols
        
        # Calculate position for perfect symmetry
        item_x = padding_x + col * (WEAPON_WIDTH + padding_x)
        item_y = start_y + row * (WEAPON_HEIGHT + padding_y)

        # Draw weapon image
        screen.blit(item["image"], (item_x, item_y))

        # Draw item name
        name_surface = font_button.render(item["name"], True, BUTTON_TEXT)
        name_rect = name_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT + 20))
        screen.blit(name_surface, name_rect)

        # Draw item price
        price_surface = font_button.render(f"${item['price']}", True, BUTTON_TEXT)
        price_rect = price_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT + 50))
        screen.blit(price_surface, price_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC key pressed
                if GAME_STATE in ["shop", "game", "settings"]:  # If in shop, game, or settings
                    GAME_STATE = "menu"  # Return to main menu
            if GAME_STATE == "game" and event.key == pygame.K_x:  # X key pressed
                is_shooting = True
                shoot_start_time = time.time()  # Record the time when shooting starts
                if shoot_sound:  # Play the shooting sound
                    shoot_sound.play()
                # Add a new fireball
                fireballs.append({"x": main_character_x + 80, "y": main_character_y + 40})  # Fireball starts at the gun position
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE == "menu":
                if play_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "game"
                elif settings_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "settings"
                elif shop_btn_rect.collidepoint(event.pos):
                    GAME_STATE = "shop"  # Navigate to the shop screen

    if GAME_STATE == "menu":
        draw_menu()
    elif GAME_STATE == "game":
        draw_game()
    elif GAME_STATE == "shop":
        draw_shop()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
