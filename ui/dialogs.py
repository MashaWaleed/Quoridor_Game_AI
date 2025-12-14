"""
Simple dialog boxes for Pygame.
"""

import pygame
import os


class InputDialog:
    """Simple text input dialog."""
    
    def __init__(self, screen, title, prompt, default_text=""):
        self.screen = screen
        self.title = title
        self.prompt = prompt
        self.text = default_text
        self.active = True
        self.result = None
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.border_color = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.button_color = (70, 130, 180)
        self.button_hover = (100, 149, 237)
        
        # Font
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 40)
        
        # Dialog dimensions
        self.width = 500
        self.height = 250
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        
        # Input box
        self.input_rect = pygame.Rect(self.x + 30, self.y + 100, self.width - 60, 40)
        
        # Buttons
        button_width = 100
        button_height = 40
        button_y = self.y + self.height - 60
        self.ok_button = pygame.Rect(self.x + self.width // 2 - button_width - 10, 
                                      button_y, button_width, button_height)
        self.cancel_button = pygame.Rect(self.x + self.width // 2 + 10, 
                                          button_y, button_width, button_height)
        
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.result = self.text
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.result = None
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Add character if it's printable
                if event.unicode.isprintable() and len(self.text) < 30:
                    self.text += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.ok_button.collidepoint(event.pos):
                self.result = self.text
                self.active = False
            elif self.cancel_button.collidepoint(event.pos):
                self.result = None
                self.active = False
    
    def update(self):
        """Update cursor blinking."""
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self):
        """Draw the dialog."""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog background
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, dialog_rect)
        pygame.draw.rect(self.screen, self.border_color, dialog_rect, 3)
        
        # Title
        title_surf = self.title_font.render(self.title, True, self.text_color)
        title_x = self.x + (self.width - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, self.y + 20))
        
        # Prompt
        prompt_surf = self.font.render(self.prompt, True, self.text_color)
        self.screen.blit(prompt_surf, (self.x + 30, self.y + 70))
        
        # Input box
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)
        pygame.draw.rect(self.screen, self.border_color, self.input_rect, 2)
        
        # Text
        text_surf = self.font.render(self.text, True, self.text_color)
        self.screen.blit(text_surf, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # Cursor
        if self.cursor_visible:
            cursor_x = self.input_rect.x + 5 + text_surf.get_width()
            pygame.draw.line(self.screen, self.text_color, 
                           (cursor_x, self.input_rect.y + 5),
                           (cursor_x, self.input_rect.y + 35), 2)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # OK button
        ok_color = self.button_hover if self.ok_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, ok_color, self.ok_button)
        ok_text = self.font.render("OK", True, (255, 255, 255))
        ok_x = self.ok_button.x + (self.ok_button.width - ok_text.get_width()) // 2
        ok_y = self.ok_button.y + (self.ok_button.height - ok_text.get_height()) // 2
        self.screen.blit(ok_text, (ok_x, ok_y))
        
        # Cancel button
        cancel_color = self.button_hover if self.cancel_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, cancel_color, self.cancel_button)
        cancel_text = self.font.render("Cancel", True, (255, 255, 255))
        cancel_x = self.cancel_button.x + (self.cancel_button.width - cancel_text.get_width()) // 2
        cancel_y = self.cancel_button.y + (self.cancel_button.height - cancel_text.get_height()) // 2
        self.screen.blit(cancel_text, (cancel_x, cancel_y))


class FileSelectDialog:
    """Simple file selection dialog."""
    
    def __init__(self, screen, title, directory='saves'):
        self.screen = screen
        self.title = title
        self.directory = directory
        self.active = True
        self.result = None
        
        # Get list of save files
        self.files = []
        if os.path.exists(directory):
            files = [f for f in os.listdir(directory) if f.endswith('.json')]
            # Sort by modification time (newest first)
            files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
            self.files = files
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.border_color = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.button_color = (70, 130, 180)
        self.button_hover = (100, 149, 237)
        self.select_color = (200, 220, 255)
        
        # Font
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 40)
        
        # Dialog dimensions
        self.width = 600
        self.height = 500
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2
        
        # File list area
        self.list_rect = pygame.Rect(self.x + 20, self.y + 70, self.width - 40, self.height - 150)
        self.selected_index = 0 if self.files else -1
        self.scroll_offset = 0
        self.item_height = 40
        
        # Buttons
        button_width = 120
        button_height = 40
        button_y = self.y + self.height - 60
        self.load_button = pygame.Rect(self.x + self.width // 2 - button_width - 10, 
                                        button_y, button_width, button_height)
        self.cancel_button = pygame.Rect(self.x + self.width // 2 + 10, 
                                          button_y, button_width, button_height)
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.selected_index >= 0:
                self.result = self.files[self.selected_index]
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.result = None
                self.active = False
            elif event.key == pygame.K_UP and self.selected_index > 0:
                self.selected_index -= 1
                self._ensure_visible()
            elif event.key == pygame.K_DOWN and self.selected_index < len(self.files) - 1:
                self.selected_index += 1
                self._ensure_visible()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.load_button.collidepoint(event.pos) and self.selected_index >= 0:
                self.result = self.files[self.selected_index]
                self.active = False
            elif self.cancel_button.collidepoint(event.pos):
                self.result = None
                self.active = False
            elif self.list_rect.collidepoint(event.pos):
                # Click on file list
                rel_y = event.pos[1] - self.list_rect.y
                index = (rel_y + self.scroll_offset) // self.item_height
                if 0 <= index < len(self.files):
                    self.selected_index = index
        
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll the file list
            if self.list_rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset = max(0, self.scroll_offset - event.y * 20)
                max_scroll = max(0, len(self.files) * self.item_height - self.list_rect.height)
                self.scroll_offset = min(self.scroll_offset, max_scroll)
    
    def _ensure_visible(self):
        """Ensure selected item is visible."""
        item_top = self.selected_index * self.item_height
        item_bottom = item_top + self.item_height
        
        if item_top < self.scroll_offset:
            self.scroll_offset = item_top
        elif item_bottom > self.scroll_offset + self.list_rect.height:
            self.scroll_offset = item_bottom - self.list_rect.height
    
    def draw(self):
        """Draw the dialog."""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog background
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, dialog_rect)
        pygame.draw.rect(self.screen, self.border_color, dialog_rect, 3)
        
        # Title
        title_surf = self.title_font.render(self.title, True, self.text_color)
        title_x = self.x + (self.width - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, self.y + 20))
        
        # File list background
        pygame.draw.rect(self.screen, (255, 255, 255), self.list_rect)
        pygame.draw.rect(self.screen, self.border_color, self.list_rect, 2)
        
        # Draw files
        if not self.files:
            no_files_surf = self.font.render("No save files found", True, (128, 128, 128))
            no_files_x = self.list_rect.x + (self.list_rect.width - no_files_surf.get_width()) // 2
            no_files_y = self.list_rect.y + (self.list_rect.height - no_files_surf.get_height()) // 2
            self.screen.blit(no_files_surf, (no_files_x, no_files_y))
        else:
            # Clip drawing to list area
            clip_rect = self.screen.get_clip()
            self.screen.set_clip(self.list_rect)
            
            for i, filename in enumerate(self.files):
                item_y = self.list_rect.y + i * self.item_height - self.scroll_offset
                item_rect = pygame.Rect(self.list_rect.x, item_y, self.list_rect.width, self.item_height)
                
                # Only draw if visible
                if item_rect.bottom < self.list_rect.top or item_rect.top > self.list_rect.bottom:
                    continue
                
                # Highlight selected
                if i == self.selected_index:
                    pygame.draw.rect(self.screen, self.select_color, item_rect)
                
                # Draw filename
                text_surf = self.font.render(filename, True, self.text_color)
                self.screen.blit(text_surf, (item_rect.x + 10, item_rect.y + 8))
                
                # Draw separator
                pygame.draw.line(self.screen, (200, 200, 200),
                               (item_rect.x, item_rect.bottom),
                               (item_rect.right, item_rect.bottom))
            
            self.screen.set_clip(clip_rect)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Load button
        load_enabled = self.selected_index >= 0
        load_color = self.button_hover if self.load_button.collidepoint(mouse_pos) and load_enabled else self.button_color
        if not load_enabled:
            load_color = (150, 150, 150)
        pygame.draw.rect(self.screen, load_color, self.load_button)
        load_text = self.font.render("Load", True, (255, 255, 255))
        load_x = self.load_button.x + (self.load_button.width - load_text.get_width()) // 2
        load_y = self.load_button.y + (self.load_button.height - load_text.get_height()) // 2
        self.screen.blit(load_text, (load_x, load_y))
        
        # Cancel button
        cancel_color = self.button_hover if self.cancel_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, cancel_color, self.cancel_button)
        cancel_text = self.font.render("Cancel", True, (255, 255, 255))
        cancel_x = self.cancel_button.x + (self.cancel_button.width - cancel_text.get_width()) // 2
        cancel_y = self.cancel_button.y + (self.cancel_button.height - cancel_text.get_height()) // 2
        self.screen.blit(cancel_text, (cancel_x, cancel_y))


def show_input_dialog(screen, title, prompt, default_text=""):
    """
    Show an input dialog and return the user's input.
    
    Returns:
        str or None: The user's input, or None if cancelled
    """
    dialog = InputDialog(screen, title, prompt, default_text)
    clock = pygame.time.Clock()
    
    while dialog.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dialog.result = None
                dialog.active = False
            else:
                dialog.handle_event(event)
        
        dialog.update()
        dialog.draw()
        pygame.display.flip()
        clock.tick(60)
    
    return dialog.result


def show_file_select_dialog(screen, title, directory='saves'):
    """
    Show a file selection dialog.
    
    Returns:
        str or None: The selected filename, or None if cancelled
    """
    dialog = FileSelectDialog(screen, title, directory)
    clock = pygame.time.Clock()
    
    while dialog.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dialog.result = None
                dialog.active = False
            else:
                dialog.handle_event(event)
        
        dialog.draw()
        pygame.display.flip()
        clock.tick(60)
    
    return dialog.result
