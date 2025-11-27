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
        # Adjusted padding and alignment for better centering
        total_padding_x = WINDOW_SIZE[0] - (cols * WEAPON_WIDTH)
        padding_x = total_padding_x // (cols + 1)
        # Increase padding between items for better spacing
        padding_x += 20  # Add extra horizontal spacing
        total_padding_y = WINDOW_SIZE[1] - 120 - (rows * WEAPON_HEIGHT)
        padding_y = total_padding_y // (rows + 1)
        # Increase padding between items for better spacing
        padding_y += 20  # Add extra vertical spacing
        # Calculate padding for symmetric alignment
        total_width = cols * WEAPON_WIDTH + (cols - 1) * padding_x
        start_x = (WINDOW_SIZE[0] - total_width) // 2

        total_height = rows * WEAPON_HEIGHT + (rows - 1) * padding_y
        start_y = (WINDOW_SIZE[1] - total_height) // 2

        for i, item in enumerate(self.items):
            col = i % cols
            row = i // cols
            
            item_x = start_x + col * (WEAPON_WIDTH + padding_x)
            item_y = start_y + row * (WEAPON_HEIGHT + padding_y)

            # Draw weapon image
            weapon_image = assets.weapon_images.get(item["name"])
            # Resize weapon image proportionally to fit within the grid cell with maximum possible size
            if weapon_image:
                image_width, image_height = weapon_image.get_size()
                scale_factor = min((WEAPON_WIDTH + 50) / image_width, (WEAPON_HEIGHT + 50) / image_height)  # Final increase in scaling
                new_width = int(image_width * scale_factor)
                new_height = int(image_height * scale_factor)
                scaled_weapon_image = pygame.transform.scale(weapon_image, (new_width, new_height))
                weapon_rect = scaled_weapon_image.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT // 2))
                screen.blit(scaled_weapon_image, weapon_rect.topleft)

            # Draw item name above the weapon image with slightly smaller font
            font = pygame.font.Font(None, 40)  # Very slightly reduced font size for weapon names
            name_surface = font.render(item["name"], True, BUTTON_TEXT)
            name_rect = name_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y - 25))  # Adjusted position above the image
            screen.blit(name_surface, name_rect)

            # Draw item price
            price_surface = assets.font_button.render(f"${item['price']}", True, BUTTON_TEXT)
            price_rect = price_surface.get_rect(center=(item_x + WEAPON_WIDTH // 2, item_y + WEAPON_HEIGHT + 50))
            screen.blit(price_surface, price_rect)