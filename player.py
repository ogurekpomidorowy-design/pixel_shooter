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
        
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True
            
    def update(self):
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y
            if self.y >= 400:
                self.y = 400
                self.is_jumping = False
                self.velocity_y = 0.0
                
    def shoot(self):
        self.is_shooting = True
        self.shoot_start_time = pygame.time.get_ticks()
        return {"x": self.x + 80, "y": self.y + 40}  # Return fireball starting position