import pygame

# Window configuration
WINDOW_SIZE = (1280, 720)
FPS = 200

# Physics
JUMP_VELOCITY = -5
GRAVITY = 0.08

# Colors
BG_COLOR = (10, 15, 40)
BUTTON_COLOR = (30, 40, 80)
BUTTON_OUTLINE = (80, 110, 180)
BUTTON_TEXT = (220, 230, 255)

# Weapon configuration
WEAPON_WIDTH = 120
WEAPON_HEIGHT = 80

# Shop items configuration
SHOP_ITEMS = [
    {"name": "Weapon 1", "price": 100, "image_path": 'grafiki/1.png'},
    {"name": "Weapon 2", "price": 250, "image_path": 'grafiki/2.png'},
    {"name": "Weapon 3", "price": 500, "image_path": 'grafiki/3.png'},
    {"name": "Weapon 4", "price": 750, "image_path": 'grafiki/4.png'},
    {"name": "Weapon 5", "price": 1000, "image_path": 'grafiki/5.png'},
    {"name": "Weapon 6", "price": 1200, "image_path": 'grafiki/6.png'},
    {"name": "Weapon 7", "price": 1500, "image_path": 'grafiki/7.png'},
    {"name": "Weapon 8", "price": 3000, "image_path": 'grafiki/8.png'}
]