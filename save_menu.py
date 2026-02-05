import pygame
from config import WINDOW_SIZE
from assets import assets
from save_system_multi import list_saves

class SaveNameInput:
    def __init__(self):
        self.text = ""
        self.active = True
        self.rect = pygame.Rect(WINDOW_SIZE[0]//2-150, WINDOW_SIZE[1]//2-40, 300, 60)
        self.ok_btn = pygame.Rect(WINDOW_SIZE[0]//2-60, WINDOW_SIZE[1]//2+30, 120, 50)

    def draw(self, screen):
        screen.fill((30,30,30))
        title = assets.font_title.render("NAZWA SEJWA", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0]//2, 150)))
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        font = pygame.font.Font(None, 48)
        txt = font.render(self.text, True, (255,255,255))
        screen.blit(txt, (self.rect.x+10, self.rect.y+10))
        pygame.draw.rect(screen, (80,200,80), self.ok_btn, border_radius=10)
        ok_txt = assets.font_button.render("ZAPISZ", True, (0,0,0))
        screen.blit(ok_txt, ok_txt.get_rect(center=self.ok_btn.center))

        # Dodaj przycisk WYJDŹ
        self.exit_btn = pygame.Rect(WINDOW_SIZE[0]//2+120, 650, 200, 50)
        pygame.draw.rect(screen, (100,100,100), self.exit_btn, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.exit_btn, 2, border_radius=10)
        exit_txt = assets.font_button.render("WYJDŹ", True, (255,255,255))
        screen.blit(exit_txt, exit_txt.get_rect(center=self.exit_btn.center))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return "ok"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 20 and event.unicode.isprintable():
                self.text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.ok_btn.collidepoint(event.pos):
                return "ok"
            if hasattr(self, 'exit_btn') and self.exit_btn.collidepoint(event.pos):
                return "menu"
        return None

class LoadSaveMenu:
    def __init__(self):
        self.saves = list_saves()
        self.btns = []
        y = 200
        for name in self.saves:
            rect = pygame.Rect(WINDOW_SIZE[0]//2-150, y, 300, 50)
            self.btns.append((name, rect))
            y += 70
        self.back_btn = pygame.Rect(WINDOW_SIZE[0]//2-100, y+30, 200, 50)

    def draw(self, screen):
        screen.fill((30,30,30))
        title = assets.font_title.render("WCZYTAJ SEJWA", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0]//2, 100)))
        for name, rect in self.btns:
            pygame.draw.rect(screen, (80,200,80), rect, border_radius=10)
            pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=10)
            txt = assets.font_button.render(name, True, (0,0,0))
            screen.blit(txt, txt.get_rect(center=rect.center))
        pygame.draw.rect(screen, (100,100,100), self.back_btn, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.back_btn, 2, border_radius=10)
        back_txt = assets.font_button.render("WRÓĆ", True, (255,255,255))
        screen.blit(back_txt, back_txt.get_rect(center=self.back_btn.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in self.btns:
                if rect.collidepoint(event.pos):
                    return name
            if self.back_btn.collidepoint(event.pos):
                return "menu"
        return None
