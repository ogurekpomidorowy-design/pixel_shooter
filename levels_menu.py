import pygame
from assets import assets
from config import WINDOW_SIZE

class LevelsMenu:
    def __init__(self, player, unlocked_level2=False):
        self.player = player
        self.unlocked_level2 = unlocked_level2
        self.selected_level = 1
        self.btn_w, self.btn_h = 300, 60
        self.btn_gap = 20
        self.level_btns = []
        self.make_buttons()
        self.back_btn_rect = pygame.Rect(WINDOW_SIZE[0]//2-100, 600, 200, 50)
        self.unlock_btn_rect = pygame.Rect(WINDOW_SIZE[0]//2-100, 400, 200, 50)

    def make_buttons(self):
        self.level_btns = []
        y = 200
        rect1 = pygame.Rect(WINDOW_SIZE[0]//2-self.btn_w//2, y, self.btn_w, self.btn_h)
        self.level_btns.append((1, rect1))
        y += self.btn_h + self.btn_gap
        rect2 = pygame.Rect(WINDOW_SIZE[0]//2-self.btn_w//2, y, self.btn_w, self.btn_h)
        self.level_btns.append((2, rect2))

    def draw(self, screen):
        screen.fill((30, 30, 30))
        title = assets.font_title.render("POZIOMY", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0]//2, 100)))
        for level, rect in self.level_btns:
            if level == 2 and not self.unlocked_level2:
                color = (100, 100, 100)
            else:
                color = (80, 200, 80) if level == self.selected_level else (60, 60, 60)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255,255,255), rect, 3, border_radius=10)
            text = assets.font_button.render(f"POZIOM {level}", True, (255,255,255))
            screen.blit(text, text.get_rect(center=rect.center))
        # Unlock button for level 2
        if not self.unlocked_level2:
            pygame.draw.rect(screen, (200, 180, 40), self.unlock_btn_rect, border_radius=10)
            pygame.draw.rect(screen, (255,255,255), self.unlock_btn_rect, 3, border_radius=10)
            unlock_text = assets.font_button.render("ODBLOCKUJ 2 POZIOM (50 MONET)", True, (0,0,0))
            screen.blit(unlock_text, unlock_text.get_rect(center=self.unlock_btn_rect.center))
        # Back button
        pygame.draw.rect(screen, (100,100,100), self.back_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.back_btn_rect, 3, border_radius=10)
        back_text = assets.font_button.render("WRÓĆ", True, (255,255,255))
        screen.blit(back_text, back_text.get_rect(center=self.back_btn_rect.center))

    def handle_click(self, pos):
        for level, rect in self.level_btns:
            if rect.collidepoint(pos):
                if level == 2 and not self.unlocked_level2:
                    return None
                self.selected_level = level
                return None
        if not self.unlocked_level2 and self.unlock_btn_rect.collidepoint(pos):
            if self.player.coins >= 50:
                self.player.coins -= 50
                self.unlocked_level2 = True
                return "unlocked"
            else:
                return "no_money"
        if self.back_btn_rect.collidepoint(pos):
            return "menu"
        return None
