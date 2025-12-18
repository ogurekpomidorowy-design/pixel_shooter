import pygame
from config import *
from assets import assets

class Settings:
    def __init__(self, alt_controls, difficulty='łatwy'):
        self.alt_controls = alt_controls
        self.difficulty = difficulty
        self.toggle_rect = pygame.Rect(WINDOW_SIZE[0]//2-250, 270, 500, 120)  # Maximum enlargement for text
        # 4 difficulty buttons for 4 modes
        self.diff_rects = [
            pygame.Rect(WINDOW_SIZE[0]//2-250 + i*170, 420, 160, 70) for i in range(4)
        ]
        self.diff_names = ['debilny', 'łatwy', 'średni', 'trudny']

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

        # Draw difficulty buttons
        for i, rect in enumerate(self.diff_rects):
            color = (80, 200, 80) if self.difficulty == self.diff_names[i] else BUTTON_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, BUTTON_OUTLINE, rect, 4, border_radius=10)
            diff_text = assets.font_button.render(self.diff_names[i].capitalize(), True, BUTTON_TEXT)
            diff_text_rect = diff_text.get_rect(center=rect.center)
            screen.blit(diff_text, diff_text_rect)

    def handle_click(self, pos):
        if self.toggle_rect.collidepoint(pos):
            self.alt_controls = not self.alt_controls
            return True
        for i, rect in enumerate(self.diff_rects):
            if rect.collidepoint(pos):
                self.difficulty = self.diff_names[i]
                return True
        return False
