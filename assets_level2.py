import pygame
from config import *

class Level2AssetLoader:
    def __init__(self):
        self.background_img = None
        self.load_assets()

    def load_assets(self):
        import os
        path = 'grafiki/2poziom.png'
        print(f"[DEBUG] Próba ładowania: {os.path.abspath(path)}")
        print(f"[DEBUG] Plik istnieje: {os.path.exists(path)}")
        try:
            self.background_img = pygame.image.load(path).convert()
            print(f"[DEBUG] Typ załadowanego obrazu: {type(self.background_img)}")
            self.background_img = pygame.transform.scale(self.background_img, WINDOW_SIZE)
            print("Level 2 background loaded successfully")
        except Exception as e:
            print(f"Error loading level 2 background: {e}")
            self.background_img = None

level2_assets = Level2AssetLoader()
