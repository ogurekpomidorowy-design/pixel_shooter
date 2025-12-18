import pygame
from config import *
from assets import assets

class Shop:
    def __init__(self):
        self.items = SHOP_ITEMS

    def draw(self, screen):
        screen.fill(BG_COLOR)
        # Draw title
        title_text = "SHOP"
        title_surface = assets.font_title.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 50))
        screen.blit(title_surface, title_rect)

        # Display shop items in a grid
        rows, cols = 2, 4
        total_padding_x = WINDOW_SIZE[0] - (cols * WEAPON_WIDTH)
        padding_x = total_padding_x // (cols + 1)
        padding_x += 20
        total_padding_y = WINDOW_SIZE[1] - 120 - (rows * WEAPON_HEIGHT)
        padding_y = total_padding_y // (rows + 1)
        padding_y += 20
        total_width = cols * WEAPON_WIDTH + (cols - 1) * padding_x
        start_x = (WINDOW_SIZE[0] - total_width) // 2
        total_height = rows * WEAPON_HEIGHT + (rows - 1) * padding_y
        start_y = (WINDOW_SIZE[1] - total_height) // 2

        # Create clickable rects for each weapon
        self.weapon_btns = []
        for i, item in enumerate(self.items):
            col = i % cols
            row = i // cols
            item_x = start_x + col * (WEAPON_WIDTH + padding_x)
            item_y = start_y + row * (WEAPON_HEIGHT + padding_y)
            # Weapon button rect (covers the weapon image area)
            btn_rect = pygame.Rect(item_x, item_y, WEAPON_WIDTH, WEAPON_HEIGHT)
            self.weapon_btns.append((item, btn_rect))

            # Draw weapon image
            weapon_image = assets.weapon_images.get(item["name"])
            if weapon_image:
                image_width, image_height = weapon_image.get_size()
                scale_factor = min((WEAPON_WIDTH + 50) / image_width, (WEAPON_HEIGHT + 50) / image_height)
                new_width = int(image_width * scale_factor)
                new_height = int(image_height * scale_factor)
                scaled_weapon_image = pygame.transform.scale(weapon_image, (new_width, new_height))
                weapon_rect = scaled_weapon_image.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT // 2))
                screen.blit(scaled_weapon_image, weapon_rect.topleft)

            # Draw item name above the weapon image
            font = pygame.font.Font(None, 40)
            name_surface = font.render(item["name"], True, BUTTON_TEXT)
            name_rect = name_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y - 25))
            screen.blit(name_surface, name_rect)

            # Draw item price
            price_surface = assets.font_button.render(f"${item['price']}", True, BUTTON_TEXT)
            price_rect = price_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT + 50))
            screen.blit(price_surface, price_rect)

        # Draw back button
        self.back_btn_rect = pygame.Rect(WINDOW_SIZE[0]//2-100, 650, 200, 50)
        pygame.draw.rect(screen, (100,100,100), self.back_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.back_btn_rect, 3, border_radius=10)
        back_text = assets.font_button.render("WRÓĆ", True, (255,255,255))
        screen.blit(back_text, back_text.get_rect(center=self.back_btn_rect.center))

    def handle_click(self, pos, player):
        # Assume self.weapon_btns is a list of (item, rect) tuples, matching self.items
        for i, item in enumerate(self.items):
            btn_rect = self.weapon_btns[i][1] if hasattr(self, 'weapon_btns') and i < len(self.weapon_btns) else None
            if btn_rect and btn_rect.collidepoint(pos):
                from shop import buy_weapon
                success, msg = buy_weapon(player, item['name'], item['price'])
                return msg
        if hasattr(self, 'back_btn_rect') and self.back_btn_rect.collidepoint(pos):
            return "menu"
        return None

def buy_weapon(player, weapon_name, price):
    if weapon_name in player.owned_weapons:
        return False, 'Masz już tę broń!'
    if player.coins >= price:
        player.coins -= price
        player.owned_weapons.add(weapon_name)
        return True, 'Zakupiono!'
    else:
        return False, 'Za mało monet!'