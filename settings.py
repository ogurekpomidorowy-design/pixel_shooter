import pygame
from config import *
from assets import assets

class Settings:
    def __init__(self, alt_controls, difficulty='łatwy', muted=False):
        self.alt_controls = alt_controls
        self.difficulty = difficulty
        self.muted = muted
        self.toggle_rect = pygame.Rect(WINDOW_SIZE[0]//2-250, 270, 500, 120)  # Maximum enlargement for text
        # 4 difficulty buttons for 4 modes
        self.diff_rects = [
            pygame.Rect(WINDOW_SIZE[0]//2-250 + i*170, 420, 160, 70) for i in range(4)
        ]
        self.diff_names = ['debilny', 'łatwy', 'średni', 'trudny']
        # Przycisk mute/unmute
        self.mute_btn_rect = pygame.Rect(WINDOW_SIZE[0]//2-100, 520, 200, 50)

    def update_mute_state(self):
        # Ustaw głośność dźwięku na 0 lub 1
        if assets.shoot_sound:
            assets.shoot_sound.set_volume(0.0 if self.muted else 1.0)

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

        # Przycisk mute/unmute
        pygame.draw.rect(screen, (100, 100, 100), self.mute_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (180, 180, 180), self.mute_btn_rect, 3, border_radius=10)
        mute_text = "WYCISZONY" if self.muted else "DŹWIĘK: WŁĄCZONY"
        mute_surface = assets.font_button.render(mute_text, True, (255,255,255))
        mute_rect = mute_surface.get_rect(center=self.mute_btn_rect.center)
        screen.blit(mute_surface, mute_rect)

        # Dodaj przycisk WYJDŹ
        self.exit_btn = pygame.Rect(WINDOW_SIZE[0]//2+120, 650, 200, 50)
        pygame.draw.rect(screen, (100,100,100), self.exit_btn, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.exit_btn, 2, border_radius=10)
        exit_txt = assets.font_button.render("WYJDŹ", True, (255,255,255))
        screen.blit(exit_txt, exit_txt.get_rect(center=self.exit_btn.center))

    def handle_click(self, pos, button=1):
        # button=1 to lewy przycisk myszy
        if button != 1:
            return False
        if self.toggle_rect.collidepoint(pos):
            self.alt_controls = not self.alt_controls
            return True
        for i, rect in enumerate(self.diff_rects):
            if rect.collidepoint(pos):
                self.difficulty = self.diff_names[i]
                return True
        # Przycisk mute/unmute
        if self.mute_btn_rect.collidepoint(pos):
            self.muted = not self.muted
            self.update_mute_state()
            return True
        # Obsługa przycisku WYJDŹ
        if hasattr(self, 'exit_btn') and self.exit_btn.collidepoint(pos):
            return "menu"
        return False
