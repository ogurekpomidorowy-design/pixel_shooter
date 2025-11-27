import pygame

pygame.init()
# Adjusted window size for a widescreen look
window_size = (1280, 720)
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
    print("Error loading background image. Ensure 'grafika/tlo_gry.png' exists.")
    background_img = None

# Define button properties and create the rectangles
btn_w, btn_h = 220, 70
btn_y = 380
btn_gap = 30
play_btn_rect = pygame.Rect(window_size[0]//2 - btn_w - btn_gap//2, btn_y, btn_w, btn_h)
settings_btn_rect = pygame.Rect(window_size[0]//2 + btn_gap//2, btn_y, btn_w, btn_h)

# Game state variable
GAME_STATE = "menu"  # Can be "menu" or "game"

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

    # --- Sprites (replace with your images) ---
    pygame.draw.rect(screen, (60, 80, 200), (100, 550, 120, 100)) # Placeholder for left characters
    pygame.draw.rect(screen, (60, 80, 200), (window_size[0] - 220, 550, 120, 100)) # Placeholder for right characters
    pygame.draw.circle(screen, (40, 50, 100), (window_size[0] - 100, 100), 30, 4) # Placeholder for skull icon

def draw_game():
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((50, 50, 50))  # Fallback background color

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

    pygame.display.flip()

pygame.quit()