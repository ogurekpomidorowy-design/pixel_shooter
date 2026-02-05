from save_system_multi import save_game_named, load_game_named, list_saves
from save_menu import SaveNameInput, LoadSaveMenu
import pygame
import time
import random
from config import *
from assets import assets
from player import Player
from enemies import Enemy
from weapons import Weapons
from menu import Menu
from shop import Shop
from settings import Settings
from ekwipunek import Ekwipunek


from assets_level2 import level2_assets
from levels_menu import LevelsMenu

class Game:
    def update_sound_volumes(self):
        # Ustaw głośność dźwięków na 0 jeśli muted, inaczej na 1
        if hasattr(assets, 'coin_sound') and assets.coin_sound:
            assets.coin_sound.set_volume(0.0 if self.muted else 1.0)
        if hasattr(assets, 'death_sound') and assets.death_sound:
            assets.death_sound.set_volume(0.0 if self.muted else 1.0)

    def __init__(self):
        pygame.init()
        if pygame.mixer.get_init() is None:
            try:
                pygame.mixer.init()
                print("Mixer initialized successfully")
            except pygame.error as e:
                print(f"Error initializing mixer: {e}")
        
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Pixel Shooter")
        self.clock = pygame.time.Clock()
        print("Display initialized")
        
        # Reinitialize assets after display is set up
        assets.__init__()
        print("Assets reinitialized after display setup")
        # Teraz poprawnie ładujemy tło poziomu 2
        from assets_level2 import level2_assets
        level2_assets.load_assets()
        # --- MUZYKA TŁA ---
        try:
            pygame.mixer.music.load("MUZYCZKA/8-Nitowa Przygoda.mp3")
            # Przycisz muzykę do 0.2 (20%)
            pygame.mixer.music.set_volume(0.0 if hasattr(self, 'muted') and self.muted else 0.2)
            pygame.mixer.music.play(-1)  # loop forever
            print("Background music loaded and playing.")
        except Exception as e:
            print(f"Could not load background music: {e}")
        if hasattr(level2_assets, 'background_img') and level2_assets.background_img:
            print("[DEBUG] Level 2 background loaded in main.py!")
        else:
            print("[DEBUG] Level 2 background NOT loaded in main.py!")
        
        self.game_state = "menu"
        self.save_input = None
        self.load_menu = None
        self.player = Player()
        self.player.coins = 50  # 50 monet na start
        self.enemies = Enemy()
        self.weapons = Weapons()
        self.menu = Menu()
        self.shop = Shop()
        self.ekwipunek = Ekwipunek(self.player)
        self.levels_menu = LevelsMenu(self.player)
        self.unlocked_level2 = False
        # Sprawdź czy tło poziomu 2 jest załadowane
        if hasattr(level2_assets, 'background_img') and level2_assets.background_img:
            print("[DEBUG] Level 2 background loaded in main.py!")
        else:
            print("[DEBUG] Level 2 background NOT loaded in main.py!")
        self.alt_controls = False  # Control scheme toggle
        self.difficulty = 'łatwy'
        self.level = 1  # Dodany poziom
        self.muted = False
        self.settings = Settings(self.alt_controls, self.difficulty, self.muted)
        print("Game initialization complete")


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Najpierw obsłuż save_input i load_menu, jeśli aktywne
            if self.game_state == "save_input" and self.save_input:
                result = self.save_input.handle_event(event)
                if result == "ok" and self.save_input.text:
                    save_game_named(self.player, self.unlocked_level2, self.save_input.text)
                    print(f"Gra zapisana jako: {self.save_input.text}")
                    self.save_input = None
                    self.game_state = "menu"
                    return True
                if result == "menu":
                    self.save_input = None
                    self.game_state = "menu"
                    return True
            if self.game_state == "load_menu" and self.load_menu:
                result = self.load_menu.handle_event(event)
                if result == "menu":
                    self.load_menu = None
                    self.game_state = "menu"
                elif result:
                    loaded, unlocked = load_game_named(self.player, result)
                    if loaded:
                        self.unlocked_level2 = unlocked
                        self.levels_menu = LevelsMenu(self.player, unlocked_level2=self.unlocked_level2)
                        print(f"Gra wczytana: {result}")
                    else:
                        print(f"Nie udało się wczytać sejwa: {result}")
                    self.load_menu = None
                    self.game_state = "menu"
                return True

            # Standardowa obsługa eventów
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC działa jak WYJDŹ wszędzie
                    if self.game_state not in ["menu"]:
                        self.save_input = None
                        self.load_menu = None
                        self.game_state = "menu"
                        return True
                if self.game_state == "settings":
                    if event.key == pygame.K_c:
                        self.alt_controls = not self.alt_controls
                        print(f"Alternate controls: {self.alt_controls}")
                if self.game_state == "game":
                    if not self.alt_controls:
                        if event.key == pygame.K_SPACE:
                            self.player.jump()
                        elif event.key == pygame.K_x:
                            fireball_pos = self.player.shoot(self.difficulty)
                            if fireball_pos:
                                self.weapons.add_fireball(fireball_pos["x"], fireball_pos["y"])
                                if assets.shoot_sound:
                                    assets.shoot_sound.play()
                        elif event.key == pygame.K_q and self.difficulty == 'debilny':
                            if not self.enemies.stopped:
                                self.enemies.stop()
                            else:
                                self.enemies.resume()
                    else:
                        if event.key == pygame.K_UP:
                            self.player.jump()
                        elif event.key == pygame.K_DOWN:
                            fireball_pos = self.player.shoot(self.difficulty)
                            if fireball_pos:
                                self.weapons.add_fireball(fireball_pos["x"], fireball_pos["y"])
                                if assets.shoot_sound:
                                    assets.shoot_sound.play()
                        elif event.key == pygame.K_0 and self.difficulty == 'debilny':
                            if not self.enemies.stopped:
                                self.enemies.stop()
                            else:
                                self.enemies.resume()
                        elif event.key == pygame.K_KP0 and self.difficulty == 'debilny':
                            if not self.enemies.stopped:
                                self.enemies.stop()
                            else:
                                self.enemies.resume()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "menu":
                    new_state = self.menu.handle_click(event.pos)
                    if new_state:
                        if new_state == "game":
                            if hasattr(self, 'levels_menu'):
                                self.level = self.levels_menu.selected_level
                            # NIE zmieniaj self.difficulty tutaj!
                            self.game_state = new_state
                        elif new_state == "save":
                            self.save_input = SaveNameInput()
                            self.game_state = "save_input"
                        elif new_state == "load":
                            self.load_menu = LoadSaveMenu()
                            self.game_state = "load_menu"
                        else:
                            self.game_state = new_state
                        if new_state == "ekwipunek":
                            self.ekwipunek.make_buttons()  # Refresh buttons for new weapons
                        if new_state == "levels":
                            self.levels_menu = LevelsMenu(self.player, unlocked_level2=self.unlocked_level2)
                elif self.game_state == "shop":
                    result = self.shop.handle_click(event.pos, self.player)
                    if result == "menu":
                        self.game_state = "menu"
                    elif result:
                        print(result)
                elif self.game_state == "ekwipunek":
                    new_state = self.ekwipunek.handle_click(event.pos)
                    if new_state:
                        self.game_state = new_state
                elif self.game_state == "levels":
                    result = self.levels_menu.handle_click(event.pos)
                    if result == "menu":
                        self.game_state = "menu"
                    elif result == "unlocked":
                        self.unlocked_level2 = True
                    elif result is None:
                        # Zmiana wybranego poziomu (nie zmieniaj difficulty!)
                        self.level = self.levels_menu.selected_level
            if self.game_state == "settings":
                # Zawsze synchronizuj difficulty z Game do Settings
                self.settings.difficulty = self.difficulty
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button = getattr(event, 'button', 1)  # domyślnie 1 jeśli brak
                    result = self.settings.handle_click(event.pos, button)
                    if result == "menu":
                        self.game_state = "menu"
                        return True
                    if result:
                        self.alt_controls = self.settings.alt_controls
                        self.difficulty = self.settings.difficulty
                        self.muted = self.settings.muted
                        # Ustaw mute/unmute dźwięku
                        if assets.shoot_sound:
                            assets.shoot_sound.set_volume(0.0 if self.muted else 1.0)
                        # Ustaw mute/unmute muzyki tła
                        pygame.mixer.music.set_volume(0.0 if self.muted else 0.2)

        return True

    def update(self):
        self.update_sound_volumes()
        if self.game_state == "game":
            self.player.update(self.difficulty)
            self.player.handle_input(self.alt_controls)
            # Automatyczne strzelanie po przytrzymaniu X lub strzałki w dół
            fireball_pos = self.player.auto_shoot(self.difficulty, self.alt_controls)
            if fireball_pos:
                self.weapons.add_fireball(fireball_pos["x"], fireball_pos["y"])
                if assets.shoot_sound:
                    assets.shoot_sound.play()
            current_time = pygame.time.get_ticks()
            # Spawn enemies
            if self.difficulty == 'łatwy':
                spawn_interval = random.randint(1000, 2000)
            elif self.difficulty == 'średni':
                spawn_interval = random.randint(670, 1330)
            else:
                spawn_interval = random.randint(500, 1000)
            if current_time - self.enemies.spawn_time > spawn_interval:
                if self.level == 1:
                    self.enemies.spawn(self.difficulty)
                elif self.level == 2:
                    self.enemies.spawn(self.difficulty, level2=True)
                self.enemies.spawn_time = current_time

            # Pass the player object to the enemies' update method
            self.enemies.update(self.player, level2=(self.level==2))
            self.weapons.update()

            # Check collisions between player and enemies
            if not (self.difficulty == 'debilny' and self.enemies.stopped):
                for enemy in self.enemies.enemies:
                    enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
                    player_rect = pygame.Rect(self.player.x, self.player.y, 80, 80)
                    if enemy_rect.colliderect(player_rect):
                        print("Game Over")
                        # Odtwórz dźwięk śmierci
                        if hasattr(assets, 'death_sound') and assets.death_sound:
                            assets.death_sound.play()
                        self.game_state = "game_over"
                        self.game_over_time = pygame.time.get_ticks()
                        return

            # Dźwięk monety odtwarzany jest teraz w enemies.py

            # Check collisions between fireballs and enemies
            self.enemies.check_collisions(self.weapons.fireballs, self.player.y, self.player.height, getattr(self.player, 'current_weapon', 'Glock'), level2=(self.level==2))

    def draw(self):
        if self.game_state == "menu":
            self.menu.draw(self.screen)
        elif self.game_state == "save_input" and self.save_input:
            self.save_input.draw(self.screen)
        elif self.game_state == "load_menu" and self.load_menu:
            self.load_menu.draw(self.screen)
        elif self.game_state == "settings":
            self.settings.alt_controls = self.alt_controls
            self.settings.difficulty = self.difficulty
            self.settings.muted = self.muted
            self.settings.update_mute_state()
            self.settings.draw(self.screen)
        elif self.game_state == "levels":
            self.levels_menu.unlocked_level2 = self.unlocked_level2
            self.levels_menu.selected_level = self.level
            self.levels_menu.draw(self.screen)
        elif self.game_state == "game":
            # Draw background
            if self.level == 2 and level2_assets.background_img:
                try:
                    self.screen.blit(level2_assets.background_img, (0, 0))
                except Exception as e:
                    print(f"Error drawing level 2 background: {e}")
            elif assets.background_img:
                try:
                    self.screen.blit(assets.background_img, (0, 0))
                except Exception as e:
                    print(f"Error drawing background: {e}")
            else:
                self.screen.fill(BG_COLOR)

            y_offset = 20 if self.level == 2 else 0
            self.enemies.draw(self.screen, assets.enemy_img, y_offset=y_offset)
            self.weapons.draw(self.screen, y_offset=y_offset)

            # Draw player
            if self.player.is_shooting and (pygame.time.get_ticks() - self.player.shoot_start_time) < 100:
                if assets.shoot_character_img:
                    self.screen.blit(assets.shoot_character_img, (int(self.player.x), int(self.player.y) + y_offset))
            else:
                self.player.is_shooting = False
                if assets.main_character_img:
                    self.screen.blit(assets.main_character_img, (int(self.player.x), int(self.player.y) + y_offset))

            # Draw coin counter in top right corner
            font = pygame.font.Font(None, 40)
            coin_text = font.render(f"Monety: {self.player.coins}", True, (255, 215, 0))
            self.screen.blit(coin_text, (WINDOW_SIZE[0] - coin_text.get_width() - 20, 20))

            # Draw ammo and reload status
            ammo = self.player.ammo[self.player.current_weapon]
            mag = self.player.magazine_sizes[self.player.current_weapon]
            weapon = self.player.current_weapon
            ammo_text = font.render(f"{weapon}: {ammo}/{mag}", True, (255,255,255))
            self.screen.blit(ammo_text, (20, 20))
            if self.player.is_reloading:
                reload_text = font.render("Przeładowanie...", True, (255, 100, 100))
                self.screen.blit(reload_text, (20, 60))
        elif self.game_state == "shop":
            self.shop.draw(self.screen)
        elif self.game_state == "ekwipunek":
            self.ekwipunek.draw(self.screen)
        elif self.game_state == "game_over":
            # Keep the current game screen as the background
            if self.level == 2 and level2_assets.background_img:
                self.screen.blit(level2_assets.background_img, (0, 0))
            elif assets.background_img:
                self.screen.blit(assets.background_img, (0, 0))
            else:
                self.screen.fill(BG_COLOR)

            y_offset = 20 if self.level == 2 else 0
            self.enemies.draw(self.screen, assets.enemy_img, y_offset=y_offset)
            self.weapons.draw(self.screen, y_offset=y_offset)
            if assets.main_character_img:
                self.screen.blit(assets.main_character_img, (int(self.player.x), int(self.player.y) + y_offset))

            # Draw 'Game Over' text with a larger font size
            font = pygame.font.Font(None, 100)  # Increased font size to 100
            text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))

            # Check if 0.7 sekundy (700 ms) minęło
            if pygame.time.get_ticks() - self.game_over_time > 700:
                self.reset_game()
                self.game_state = "menu"
        pygame.display.flip()

    def reset_game(self):
        """Reset the game state to start a new game."""
        coins = self.player.coins if hasattr(self.player, 'coins') else 0
        owned_weapons = set(self.player.owned_weapons) if hasattr(self.player, 'owned_weapons') else {'Glock'}
        current_weapon = self.player.current_weapon if hasattr(self.player, 'current_weapon') else 'Glock'
        self.player = Player()
        self.player.coins = coins
        self.player.owned_weapons = owned_weapons
        self.player.current_weapon = current_weapon
        self.enemies = Enemy()
        self.weapons = Weapons()
        self.ekwipunek = Ekwipunek(self.player)
        print("Game has been reset.")

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()