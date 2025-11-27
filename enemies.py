import pygame
import random
from config import *

class Enemy:
    def __init__(self):
        self.enemies = []
        self.spawn_time = 0

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

    def check_collisions(self, fireballs):
        for enemy in self.enemies[:]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
            for fireball in fireballs[:]:
                fireball_rect = pygame.Rect(fireball["x"] - 5, fireball["y"] - 5, 10, 10)
                if enemy_rect.colliderect(fireball_rect):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if fireball in fireballs:
                        fireballs.remove(fireball)
                    break

    def draw(self, screen, enemy_img):
        for enemy in self.enemies:
            if enemy_img:
                screen.blit(enemy_img, (enemy["x"], enemy["y"]))