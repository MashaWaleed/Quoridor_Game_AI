"""
Menu system for Quoridor game.
"""

import pygame
from .colors import Colors


class Button:
    """Simple button class."""
    
    def __init__(self, x, y, width, height, text, callback):
        """Initialize button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
    
    def draw(self, screen, font):
        """Draw button."""
        color = Colors.BUTTON_HOVER if self.hovered else Colors.BUTTON
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, Colors.TEXT, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, Colors.BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        """Handle mouse events."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.callback()
                return True
        return False


class Menu:
    """Main menu for game mode selection."""
    
    def __init__(self, width, height):
        """Initialize menu."""
        self.width = width
        self.height = height
        self.buttons = []
        self.active = True
        self.selected_mode = None
        self.selected_difficulty = None
        
    def setup_main_menu(self, callbacks):
        """
        Setup main menu buttons.
        
        Args:
            callbacks: Dict with 'pvp' and 'pvc' callback functions
        """
        self.buttons = []
        
        button_width = 300
        button_height = 60
        button_x = self.width // 2 - button_width // 2
        start_y = self.height // 2 - 100
        spacing = 80
        
        # Player vs Player button
        pvp_button = Button(
            button_x, start_y,
            button_width, button_height,
            "Player vs Player",
            callbacks['pvp']
        )
        self.buttons.append(pvp_button)
        
        # Player vs Computer button
        pvc_button = Button(
            button_x, start_y + spacing,
            button_width, button_height,
            "Player vs Computer",
            callbacks['pvc']
        )
        self.buttons.append(pvc_button)
    
    def setup_difficulty_menu(self, callbacks):
        """
        Setup difficulty selection menu.
        
        Args:
            callbacks: Dict with 'easy', 'medium', 'hard', 'back' callbacks
        """
        self.buttons = []
        
        button_width = 300
        button_height = 60
        button_x = self.width // 2 - button_width // 2
        start_y = self.height // 2 - 150
        spacing = 80
        
        # Easy button
        easy_button = Button(
            button_x, start_y,
            button_width, button_height,
            "Easy AI",
            callbacks['easy']
        )
        self.buttons.append(easy_button)
        
        # Medium button
        medium_button = Button(
            button_x, start_y + spacing,
            button_width, button_height,
            "Medium AI",
            callbacks['medium']
        )
        self.buttons.append(medium_button)
        
        # Hard button
        hard_button = Button(
            button_x, start_y + spacing * 2,
            button_width, button_height,
            "Hard AI",
            callbacks['hard']
        )
        self.buttons.append(hard_button)
        
        # Back button
        back_button = Button(
            button_x, start_y + spacing * 3 + 20,
            button_width, button_height // 2 + 10,
            "Back",
            callbacks['back']
        )
        self.buttons.append(back_button)
    
    def draw(self, screen, font_large, font_medium):
        """Draw menu."""
        screen.fill(Colors.BACKGROUND)
        
        # Title
        title = font_large.render("QUORIDOR", True, Colors.TEXT)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Subtitle
        if len(self.buttons) == 2:  # Main menu
            subtitle = font_medium.render("Select Game Mode", True, Colors.TEXT_LIGHT)
        else:  # Difficulty menu
            subtitle = font_medium.render("Select Difficulty", True, Colors.TEXT_LIGHT)
        
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 160))
        screen.blit(subtitle, subtitle_rect)
        
        # Buttons
        for button in self.buttons:
            button.draw(screen, font_medium)
    
    def handle_event(self, event):
        """Handle events for menu."""
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
