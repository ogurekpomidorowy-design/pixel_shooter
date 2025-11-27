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
        padding_y = 100
        start_y = 120

        for i, item in enumerate(self.items):
            col = i % cols
            row = i // cols
            
            item_x = padding_x + col * (WEAPON_WIDTH + padding_x)
            item_y = start_y + row * (WEAPON_HEIGHT + padding_y)

            # Draw weapon image
            weapon_image = assets.weapon_images.get(item["name"])
            if weapon_image:
                screen.blit(weapon_image, (item_x, item_y))

            # Draw item name
            name_surface = assets.font_button.render(item["name"], True, BUTTON_TEXT)
            name_rect = name_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT + 20))
            screen.blit(name_surface, name_rect)

            # Draw item price
            price_surface = assets.font_button.render(f"${item['price']}", True, BUTTON_TEXT)
            price_rect = price_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT + 50))
            screen.blit(price_surface, price_rect)