import pygame
import random
from config import *

class Coin:
    def __init__(self, x, y, player_y, player_height):
        self.x = x
        # Position coin so its top edge aligns with player's feet
        self.y = player_y + player_height - 30  # 30 is coin height
        self.image = pygame.image.load("grafiki/moneta.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.speed_y = 2  # Gravity effect
        self.on_ground = False
        self.ground_level = self.y

    def update(self, player):
        if not self.on_ground:
            self.y += self.speed_y
            if self.y >= self.ground_level:
                self.y = self.ground_level
                self.on_ground = True
        else:
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            coin_rect = pygame.Rect(self.x, self.y, 30, 30)
            if player_rect.colliderect(coin_rect):
                player.coins += 1
                return False
        return True

    def draw(self, screen, y_offset=0):
        screen.blit(self.image, (self.x, self.y + y_offset))

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("grafiki/wybuch-bomby-na-przezroczystym-tle_84443-2542-removebg-preview.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (700, 700))
        self.timer = 30  # liczba klatek wybuchu

    def update(self):
        self.timer -= 1
        return self.timer > 0

    def draw(self, screen, y_offset=0):
        screen.blit(self.image, (self.x-350, self.y-350 + y_offset))

class Enemy:
    def __init__(self):
        self.enemies = []
        self.spawn_time = 0
        self.coins = []  # List to store coins
        self.explosions = []  # List to store explosions
        self.stopped = False  # For 'debilny' mode

    def stop(self):
        self.stopped = True

    def resume(self):
        self.stopped = False

    def spawn(self, difficulty='łatwy', level2=False):
        enemy_x = 1200
        enemy_y = 400
        base_speed = random.uniform(3, 6)
        if difficulty == 'debilny':
            hp = 1
            enemy_speed = base_speed * 0.8
        elif difficulty == 'łatwy':
            hp = 10
            enemy_speed = base_speed * 0.8
        elif difficulty == 'średni':
            hp = 20
            enemy_speed = base_speed * 0.9
        elif difficulty == 'trudny':
            hp = 30
            enemy_speed = base_speed
        else:
            hp = 50
            enemy_speed = base_speed
        if level2:
            # Ułatw poziom 2: mniej HP i wolniej
            hp = max(5, hp - 10)
            enemy_speed = base_speed * 0.7
        self.enemies.append({
            "x": enemy_x,
            "y": enemy_y,
            "speed": enemy_speed,
            "hp": hp,
            "max_hp": hp
        })

    def update(self, player, level2=False):
        for enemy in self.enemies[:]:
            if not self.stopped:
                enemy["x"] -= enemy["speed"]
            if enemy["x"] + 80 < 0:
                self.enemies.remove(enemy)

        # Update coins
        import assets
        for coin in self.coins[:]:
            if not coin.update(player):
                try:
                    # Zawsze 2 monety na level2
                    if level2:
                        player.coins += 2
                        print(f"Player collected 2 coins. Total: {player.coins}")
                    else:
                        player.coins += 1
                        print(f"Player collected a coin. Total: {player.coins}")
                    if hasattr(assets.assets, 'coin_sound') and assets.assets.coin_sound:
                        assets.assets.coin_sound.play()
                except Exception:
                    print("Warning: could not increment player.coins")
                self.coins.remove(coin)

        # Update explosions
        for explosion in self.explosions[:]:
            if not explosion.update():
                self.explosions.remove(explosion)

    def check_collisions(self, fireballs, player_y, player_height, weapon_name="Glock", level2=False):
        # Weapon damage mapping
        weapon_damage = {
            "Glock": 5,
            "Rewolwer": 7,
            "Strzelba Pompka": 10,
            "Pistolet Maszynowy": 6,
            "AK-47": 8,
            "Tomson": 9,
            "Karabin Szturmowy MP5": 5,
            "Wyrzutnia Rakiet": 51
        }
        area_damage = 12
        for enemy in self.enemies[:]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
            for fireball in fireballs[:]:
                fireball_rect = pygame.Rect(fireball["x"] - 5, fireball["y"] - 5, 10, 10)
                if enemy_rect.colliderect(fireball_rect):
                    dmg = weapon_damage.get(weapon_name, 5)
                    if weapon_name == "Wyrzutnia Rakiet":
                        # Wybuch: natychmiast zabija wszystkich wrogów w dużym obszarze
                        explosion_rect = pygame.Rect(fireball["x"]-350, fireball["y"]-350, 700, 700)
                        for e2 in self.enemies[:]:
                            e2_rect = pygame.Rect(e2["x"], e2["y"], 80, 80)
                            if e2_rect.colliderect(explosion_rect):
                                e2["hp"] = 0  # eksplozja zawsze zabija
                        self.explosions.append(Explosion(fireball["x"], fireball["y"]))
                        # Usuń wszystkich wrogów z hp <= 0
                        for enemy in self.enemies[:]:
                            if enemy["hp"] <= 0:
                                self.coins.append(Coin(enemy["x"], enemy["y"], player_y, player_height))
                                self.enemies.remove(enemy)
                    else:
                        enemy["hp"] -= dmg
                    if enemy["hp"] <= 0:
                        self.coins.append(Coin(enemy["x"], enemy["y"], player_y, player_height))
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                    if fireball in fireballs:
                        fireballs.remove(fireball)
                    break

    def draw(self, screen, enemy_img, y_offset=0):
        for enemy in self.enemies:
            if enemy_img:
                screen.blit(enemy_img, (enemy["x"], enemy["y"] + y_offset))
            # Draw health bar
            bar_width = 80
            bar_height = 8
            bar_x = enemy["x"]
            bar_y = enemy["y"] - 16 + y_offset
            hp_ratio = max(enemy["hp"], 0) / enemy["max_hp"]
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (200, 40, 40), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))

        # Draw coins
        for coin in self.coins:
            coin.draw(screen, y_offset=y_offset)

        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(screen, y_offset=y_offset)