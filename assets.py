import pygame
from config import *

class AssetLoader:
    def __init__(self):
        # Initialize pygame font module
        pygame.font.init()
        
        self.background_img = None
        self.enemy_img = None
        self.main_character_img = None
        self.shoot_character_img = None
        self.shoot_sound = None
        self.weapon_images = {}
        
        # Load fonts
        self.font_title = pygame.font.SysFont("Arial", 120, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_game_over = pygame.font.SysFont("Arial", 80, bold=True)
        
        self.load_assets()

    def load_assets(self):
        try:
            self.background_img = pygame.image.load('grafiki/tlo_gry.png').convert()
            self.background_img = pygame.transform.scale(self.background_img, WINDOW_SIZE)
            print("Background image loaded successfully")  # Debug message
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background_img = None
            
        try:
            self.enemy_img = pygame.image.load('grafiki/enemy.png').convert_alpha()
            self.enemy_img = pygame.transform.scale(self.enemy_img, (80, 80))
            print("Enemy image loaded successfully")  # Debug message
        except pygame.error as e:
            print(f"Error loading enemy image: {e}")
            self.enemy_img = None
            
        try:
            self.main_character_img = pygame.image.load('grafiki/main_character.png').convert_alpha()
            self.main_character_img = pygame.transform.scale(self.main_character_img, (80, 80))
            print("Main character image loaded successfully")
        except pygame.error as e:
            print(f"Error loading main character image: {e}")
            self.main_character_img = None
            
        try:
            self.shoot_character_img = pygame.image.load('grafiki/shoot_ch.png').convert_alpha()
            self.shoot_character_img = pygame.transform.scale(self.shoot_character_img, (80, 80))
            print("Shooting character image loaded successfully")
        except pygame.error as e:
            print(f"Error loading shooting character image: {e}")
            self.shoot_character_img = None
            
        try:
            pygame.mixer.init()  # Make sure mixer is initialized
            self.shoot_sound = pygame.mixer.Sound('grafiki/strzal.mp3')
            print("Shooting sound loaded successfully")
        except pygame.error as e:
            print(f"Error loading shooting sound: {e}")
            self.shoot_sound = None

        # Load weapon images
        for item in SHOP_ITEMS:
            try:
                image = pygame.image.load(item['image_path']).convert_alpha()
                self.weapon_images[item['name']] = image
            except pygame.error:
                print(f"Error loading weapon image: {item['image_path']}")

assets = AssetLoader()