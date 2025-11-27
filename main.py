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
        print("Game initialization complete")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state in ["shop", "game", "settings"]:
                        self.game_state = "menu"
                if self.game_state == "game":
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_x:
                        fireball_pos = self.player.shoot()
                        self.weapons.add_fireball(fireball_pos["x"], fireball_pos["y"])
                        if assets.shoot_sound:
                            assets.shoot_sound.play()
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "menu":
                    new_state = self.menu.handle_click(event.pos)
                    if new_state:
                        self.game_state = new_state
        
        return True

    def update(self):
        if self.game_state == "game":
            self.player.update()
            
            # Spawn enemies
            current_time = pygame.time.get_ticks()
            if current_time - self.enemies.spawn_time > random.randint(500, 1000):
                self.enemies.spawn()
                self.enemies.spawn_time = current_time
                
            self.enemies.update()
            self.weapons.update()

            # Check collisions between player and enemies
            for enemy in self.enemies.enemies:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 80, 80)
                player_rect = pygame.Rect(self.player.x, self.player.y, 80, 80)
                if enemy_rect.colliderect(player_rect):
                    print("Game Over")
                    self.game_state = "game_over"
                    self.game_over_time = pygame.time.get_ticks()
                    return

            # Check collisions between fireballs and enemies
            self.enemies.check_collisions(self.weapons.fireballs)

    def draw(self):
        if self.game_state == "menu":
            self.menu.draw(self.screen)
        elif self.game_state == "game":
            # Draw background
            if assets.background_img:
                try:
                    self.screen.blit(assets.background_img, (0, 0))
                except Exception as e:
                    print(f"Error drawing background: {e}")
                    self.screen.fill(BG_COLOR)  # Use the configured background color instead of gray
            else:
                self.screen.fill(BG_COLOR)  # Use the configured background color instead of gray
                
            self.enemies.draw(self.screen, assets.enemy_img)
            self.weapons.draw(self.screen)
            
            # Draw player
            if self.player.is_shooting and (pygame.time.get_ticks() - self.player.shoot_start_time) < 100:  # 100ms = 0.1s
                if assets.shoot_character_img:
                    self.screen.blit(assets.shoot_character_img, 
                                   (int(self.player.x), int(self.player.y)))
            else:
                self.player.is_shooting = False
                if assets.main_character_img:
                    self.screen.blit(assets.main_character_img, 
                                   (int(self.player.x), int(self.player.y)))
        
        elif self.game_state == "shop":
            self.shop.draw(self.screen)
            
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
                self.reset_game()  # Reset the game state before returning to the menu
                self.game_state = "menu"

        pygame.display.flip()

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.player = Player()  # Reset player position and state
        self.enemies = Enemy()  # Clear all enemies
        self.weapons = Weapons()  # Clear all fireballs
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