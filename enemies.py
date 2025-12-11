import pygame
import random
from config import *

class Coin:
    def __init__(self, x, y, player_y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("grafiki/moneta.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.speed_y = 2  # Gravity effect
        self.on_ground = False
        self.ground_level = player_y + 60  # Coin stops slightly lower than before

    def update(self):
        if not self.on_ground:
            self.y += self.speed_y  # Coin falls downward due to gravity
            if self.y >= self.ground_level:  # Coin stops slightly below the player
                self.y = self.ground_level
                self.on_ground = True  # Coin stops falling when it hits the ground
        return True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Enemy:
    def __init__(self):
        self.enemies = []
        self.spawn_time = 0
        self.coins = []  # List to store coins

    def spawn(self):
        enemy_x = 1200
        enemy_y = 400
        enemy_speed = random.uniform(3, 6)  # Zwiększona prędkość wrogów
        self.enemies.append({"x": enemy_x, "y": enemy_y, "speed": enemy_speed})

    def update(self):
        for enemy in self.enemies[:]:
            enemy["x"] -= enemy["speed"]
            if enemy["x"] + 80 < 0:
                self.enemies.remove(enemy)

        # Update coins
        self.coins = [coin for coin in self.coins if coin.update()]

    def check_collisions(self, fireballs, player_y):
        for enemy in self.enemies[:]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
            for fireball in fireballs[:]:
                fireball_rect = pygame.Rect(fireball["x"] - 5, fireball["y"] - 5, 10, 10)
                if enemy_rect.colliderect(fireball_rect):
                    if enemy in self.enemies:
                        self.coins.append(Coin(enemy["x"], enemy["y"], player_y))  # Spawn coin slightly below player
                        self.enemies.remove(enemy)
                    if fireball in fireballs:
                        fireballs.remove(fireball)
                    break

    def draw(self, screen, enemy_img):
        for enemy in self.enemies:
            if enemy_img:
                screen.blit(enemy_img, (enemy["x"], enemy["y"]))

        # Draw coins
        for coin in self.coins:
            coin.draw(screen)