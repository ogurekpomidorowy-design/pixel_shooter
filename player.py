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