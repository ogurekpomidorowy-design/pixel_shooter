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

class Game:
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
        
        self.game_state = "menu"
        self.player = Player()
        self.enemies = Enemy()
        self.weapons = Weapons()
        self.menu = Menu()
        self.shop = Shop()
        self.ekwipunek = Ekwipunek(self.player)
        self.alt_controls = False  # Control scheme toggle
        self.difficulty = 'łatwy'
        self.settings = Settings(self.alt_controls, self.difficulty)
        print("Game initialization complete")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state in ["shop", "game", "settings"]:
                        self.game_state = "menu"
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
                        self.game_state = new_state
                        if new_state == "ekwipunek":
                            self.ekwipunek.make_buttons()  # Refresh buttons for new weapons
                elif self.game_state == "shop":
                    result = self.shop.handle_click(event.pos, self.player)
                    if result:
                        print(result)
                elif self.game_state == "ekwipunek":
                    new_state = self.ekwipunek.handle_click(event.pos)
                    if new_state:
                        self.game_state = new_state
                if self.game_state == "settings":
                    if self.settings.handle_click(event.pos):
                        self.alt_controls = self.settings.alt_controls
                        self.difficulty = self.settings.difficulty
        
        return True

    def update(self):
        if self.game_state == "game":
            self.player.update(self.difficulty)
            self.player.handle_input(self.alt_controls)
            # Spawn enemies
            current_time = pygame.time.get_ticks()
            # Adjust spawn rate and speed by difficulty
            if self.difficulty == 'łatwy':
                spawn_interval = random.randint(1000, 2000)  # 2x rzadziej
            elif self.difficulty == 'średni':
                spawn_interval = random.randint(670, 1330)   # 1.33x rzadziej
            else:
                spawn_interval = random.randint(500, 1000)
            if current_time - self.enemies.spawn_time > spawn_interval:
                self.enemies.spawn(self.difficulty)
                self.enemies.spawn_time = current_time
                
            # Pass the player object to the enemies' update method
            self.enemies.update(self.player)
            self.weapons.update()

            # Check collisions between player and enemies
            if not (self.difficulty == 'debilny' and self.enemies.stopped):
                for enemy in self.enemies.enemies:
                    enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
                    player_rect = pygame.Rect(self.player.x, self.player.y, 80, 80)
                    if enemy_rect.colliderect(player_rect):
                        print("Game Over")
                        self.game_state = "game_over"
                        self.game_over_time = pygame.time.get_ticks()
                        return

            # Check collisions between fireballs and enemies
            self.enemies.check_collisions(self.weapons.fireballs, self.player.y, self.player.height, getattr(self.player, 'current_weapon', 'Glock'))

    def draw(self):
        if self.game_state == "menu":
            self.menu.draw(self.screen)
        elif self.game_state == "settings":
            self.settings.alt_controls = self.alt_controls
            self.settings.difficulty = self.difficulty
            self.settings.draw(self.screen)
        elif self.game_state == "game":
            # Draw background
            if assets.background_img:
                try:
                    self.screen.blit(assets.background_img, (0, 0))
                except Exception as e:
                    print(f"Error drawing background: {e}")
            else:
                self.screen.fill(BG_COLOR)

            self.enemies.draw(self.screen, assets.enemy_img)
            self.weapons.draw(self.screen)

            # Draw player
            if self.player.is_shooting and (pygame.time.get_ticks() - self.player.shoot_start_time) < 100:
                if assets.shoot_character_img:
                    self.screen.blit(assets.shoot_character_img, (int(self.player.x), int(self.player.y)))
            else:
                self.player.is_shooting = False
                if assets.main_character_img:
                    self.screen.blit(assets.main_character_img, (int(self.player.x), int(self.player.y)))

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
            if assets.background_img:
                self.screen.blit(assets.background_img, (0, 0))
            else:
                self.screen.fill(BG_COLOR)

            self.enemies.draw(self.screen, assets.enemy_img)
            self.weapons.draw(self.screen)
            if assets.main_character_img:
                self.screen.blit(assets.main_character_img, (int(self.player.x), int(self.player.y)))

            # Draw 'Game Over' text with a larger font size
            font = pygame.font.Font(None, 100)  # Increased font size to 100
            text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))

            # Check if 3 seconds have passed
            if pygame.time.get_ticks() - self.game_over_time > 3000:
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