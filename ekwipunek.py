import pygame
from assets import assets
from config import WINDOW_SIZE

class Ekwipunek:
    def __init__(self, player):
        self.player = player
        self.selected_weapon = player.current_weapon
        self.btn_w, self.btn_h = 300, 60
        self.btn_gap = 20
        self.weapon_btns = []
        self.make_buttons()
        self.back_btn_rect = pygame.Rect(WINDOW_SIZE[0]//2-100, 600, 200, 50)

    def make_buttons(self):
        self.weapon_btns = []
        y = 200
        for weapon in sorted(self.player.owned_weapons):
            rect = pygame.Rect(WINDOW_SIZE[0]//2-self.btn_w//2, y, self.btn_w, self.btn_h)
            self.weapon_btns.append((weapon, rect))
            y += self.btn_h + self.btn_gap

    def draw(self, screen):
        screen.fill((30, 30, 30))
        title = assets.font_title.render("EKWIPUNEK", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0]//2, 100)))
        for weapon, rect in self.weapon_btns:
            color = (80, 200, 80) if weapon == self.player.current_weapon else (60, 60, 60)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255,255,255), rect, 3, border_radius=10)
            text = assets.font_button.render(weapon, True, (255,255,255))
            screen.blit(text, text.get_rect(center=rect.center))
        # Back button
        pygame.draw.rect(screen, (100,100,100), self.back_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.back_btn_rect, 3, border_radius=10)
        back_text = assets.font_button.render("WRÓĆ", True, (255,255,255))
        screen.blit(back_text, back_text.get_rect(center=self.back_btn_rect.center))

    def handle_click(self, pos):
        for weapon, rect in self.weapon_btns:
            if rect.collidepoint(pos):
                self.player.current_weapon = weapon
                return None
        if self.back_btn_rect.collidepoint(pos):
            return "menu"
        return None
