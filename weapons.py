import pygame
from config import *

class Weapons:
    def __init__(self):
        self.fireballs = []
        self.speed = 15  # Zwiększona prędkość pocisków
        self.radius = 5

    def add_fireball(self, x, y):
        self.fireballs.append({"x": x, "y": y})

    def update(self):
        for fireball in self.fireballs[:]:
            fireball["x"] += self.speed
            if fireball["x"] > WINDOW_SIZE[0]:
                self.fireballs.remove(fireball)

    def draw(self, screen):
        for fireball in self.fireballs:
            pygame.draw.circle(screen, (255, 100, 0), 
                             (int(fireball["x"]), int(fireball["y"])), 
                             self.radius)