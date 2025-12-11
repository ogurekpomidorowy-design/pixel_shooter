import pygame
from config import *
from assets import assets

class Settings:
    def __init__(self, alt_controls):
        self.alt_controls = alt_controls
        self.toggle_rect = pygame.Rect(WINDOW_SIZE[0]//2-250, 270, 500, 120)  # Maximum enlargement for text

    def draw(self, screen):
        screen.fill(BG_COLOR)
        title_text = "USTAWIENIA"
        title_surface = assets.font_title.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WINDOW_SIZE[0]//2, 150))
        screen.blit(title_surface, title_rect)

        # Draw toggle button
        pygame.draw.rect(screen, BUTTON_COLOR, self.toggle_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_OUTLINE, self.toggle_rect, 4, border_radius=10)
        mode = "Strzałki" if self.alt_controls else "Klasyczne"
        toggle_text = assets.font_button.render(f"Sterowanie: {mode}", True, BUTTON_TEXT)
        toggle_text_rect = toggle_text.get_rect(center=self.toggle_rect.center)
        screen.blit(toggle_text, toggle_text_rect)

    def handle_click(self, pos):
        if self.toggle_rect.collidepoint(pos):
            self.alt_controls = not self.alt_controls
            return True
        return False
