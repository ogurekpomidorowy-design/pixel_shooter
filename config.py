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
    {"name": "Glock", "price": 50, "image_path": 'grafiki/1.png'},
    {"name": "Rewolwer", "price": 125, "image_path": 'grafiki/2.png'},
    {"name": "Strzelba Pompka", "price": 250, "image_path": 'grafiki/3.png'},
    {"name": "Pistolet Maszynowy", "price": 375, "image_path": 'grafiki/4.png'},
    {"name": "AK-47", "price": 500, "image_path": 'grafiki/5.png'},
    {"name": "Tomson", "price": 600, "image_path": 'grafiki/6.png'},
    {"name": "Karabin Szturmowy MP5", "price": 750, "image_path": 'grafiki/7.png'},
    {"name": "Wyrzutnia Rakiet", "price": 1500, "image_path": 'grafiki/8.png'}
]