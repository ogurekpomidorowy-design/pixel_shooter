import pygame
from config import *
from assets import assets

class Menu:
    def __init__(self):
        self.btn_w, self.btn_h = 220, 70
        self.btn_y = 380
        self.btn_gap = 30
        
        # Create button rectangles
        self.play_btn_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - self.btn_w - self.btn_gap // 2,
            self.btn_y,
            self.btn_w,
            self.btn_h
        )
        
        self.settings_btn_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 + self.btn_gap // 2,
            self.btn_y,
            self.btn_w,
            self.btn_h
        )
        
        self.shop_btn_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - 100,
            500,
            200,
            50
        )

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        # Draw title
        title_text = "PIXEL SHOOTER"
        title_surface = assets.font_title.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 150))
        screen.blit(title_surface, title_rect)

        # Draw PLAY button
        pygame.draw.rect(screen, BUTTON_COLOR, self.play_btn_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_OUTLINE, self.play_btn_rect, 4, border_radius=10)
        play_text = assets.font_button.render("PLAY", True, BUTTON_TEXT)
        play_text_rect = play_text.get_rect(center=self.play_btn_rect.center)
        screen.blit(play_text, play_text_rect)

        # Draw SETTINGS button
        pygame.draw.rect(screen, BUTTON_COLOR, self.settings_btn_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_OUTLINE, self.settings_btn_rect, 4, border_radius=10)
        settings_text = assets.font_button.render("SETTINGS", True, BUTTON_TEXT)
        settings_text_rect = settings_text.get_rect(center=self.settings_btn_rect.center)
        screen.blit(settings_text, settings_text_rect)

        # Draw SHOP button
        pygame.draw.rect(screen, BUTTON_COLOR, self.shop_btn_rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_OUTLINE, self.shop_btn_rect, 4, border_radius=10)
        shop_text = assets.font_button.render("SHOP", True, BUTTON_TEXT)
        shop_text_rect = shop_text.get_rect(center=self.shop_btn_rect.center)
        screen.blit(shop_text, shop_text_rect)

    def handle_click(self, pos):
        if self.play_btn_rect.collidepoint(pos):
            return "game"
        elif self.settings_btn_rect.collidepoint(pos):
            return "settings"
        elif self.shop_btn_rect.collidepoint(pos):
            return "shop"
        return None