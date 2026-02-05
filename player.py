import pygame
from config import *

class Player:
    def __init__(self, x=100, y=400):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_shooting = False
        self.shoot_start_time = 0
        self.width = 50
        self.height = 50
        self.coins = 0  # Player's collected coins
        self.current_weapon = 'Glock'
        self.owned_weapons = {'Glock'}  # Player always owns Glock by default
        self.magazine_sizes = {
            'Glock': 12,
            'Rewolwer': 20,
            'Strzelba Pompka': 10,
            'Pistolet Maszynowy': 7,
            'AK-47': 8,
            'Tomson': 9,
            'Karabin Szturmowy MP5': 20,
            'Wyrzutnia Rakiet': 1
        }

        self.ammo = {w: self.magazine_sizes[w] for w in self.magazine_sizes}
        self.is_reloading = False
        self.reload_start_time = 0
        self.reload_time = 2000  # ms, default for easy
        self.last_shot_time = 0
        self.cooldowns = {
            'Glock': int(500 * 0.7),
            'Rewolwer': int(500 * 0.7),
            'Strzelba Pompka': 650,
            'Pistolet Maszynowy': int(300 * 0.7),
            'AK-47': int(200 * 0.7),
            'Tomson': int(300 * 0.7),
            'Karabin Szturmowy MP5': int(100 * 0.7),
            'Wyrzutnia Rakiet': 0
        }

    def auto_shoot(self, difficulty='łatwy', alt_controls=False):
        keys = pygame.key.get_pressed()
        auto_weapons = [
            'Pistolet Maszynowy',
            'AK-47',
            'Tomson',
            'Karabin Szturmowy MP5'
        ]
        if self.current_weapon not in auto_weapons:
            return None
        if not alt_controls:
            if keys[pygame.K_x]:
                result = self.shoot(difficulty)
                if result:
                    return result
        else:
            if keys[pygame.K_DOWN]:
                result = self.shoot(difficulty)
                if result:
                    return result
        return None

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True
            
    def start_reload(self, difficulty='łatwy'):
        if not self.is_reloading:
            self.is_reloading = True
            self.reload_start_time = pygame.time.get_ticks()
            if difficulty == 'łatwy':
                self.reload_time = 1000
            elif difficulty == 'średni':
                self.reload_time = 2000
            elif difficulty == 'trudny':
                self.reload_time = 3000
            else:
                self.reload_time = 1000

    def update(self, difficulty='łatwy'):
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y
            if self.y >= 400:
                self.y = 400
                self.is_jumping = False
                self.velocity_y = 0.0
        if self.is_reloading:
            now = pygame.time.get_ticks()
            if now - self.reload_start_time >= self.reload_time:
                self.ammo[self.current_weapon] = self.magazine_sizes[self.current_weapon]
                self.is_reloading = False

    def shoot(self, difficulty='łatwy'):
        now = pygame.time.get_ticks()
        cooldown = self.cooldowns.get(self.current_weapon, 500)
        if self.is_reloading:
            return None  # Can't shoot while reloading
        if now - self.last_shot_time < cooldown:
            return None  # Can't shoot, cooldown not finished
        if difficulty == 'debilny':
            self.is_shooting = True
            self.shoot_start_time = now
            self.last_shot_time = now
            self.ammo[self.current_weapon] = self.magazine_sizes[self.current_weapon]  # Always full
            return {"x": self.x + 80, "y": self.y + 40}
        if self.ammo[self.current_weapon] > 0:
            self.is_shooting = True
            self.shoot_start_time = now
            self.ammo[self.current_weapon] -= 1
            self.last_shot_time = now
            return {"x": self.x + 80, "y": self.y + 40}
        else:
            self.start_reload(difficulty)
            return None

    def handle_input(self, alt_controls=False):
        keys = pygame.key.get_pressed()
        if not alt_controls:
            if keys[pygame.K_a]:  # Move left
                self.x -= 5
            if keys[pygame.K_d]:  # Move right
                self.x += 5
        else:
            if keys[pygame.K_LEFT]:
                self.x -= 5
            if keys[pygame.K_RIGHT]:
                self.x += 5
        # Keep player inside window bounds
        if self.x < 0:
            self.x = 0
        if self.x > WINDOW_SIZE[0] - self.width:
            self.x = WINDOW_SIZE[0] - self.width