"""
Renderer class for Quoridor game using Pygame.
"""

import pygame
from .colors import Colors
from game.wall import Wall


class Renderer:
    """Handles all rendering for the Quoridor game."""
    
    def __init__(self, width, height):
        """
        Initialize renderer.
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        
        # Board dimensions
        self.board_size = 9
        self.margin = 80
        self.info_panel_width = 250
        
        # Calculate cell size to fit board
        available_width = width - 2 * self.margin - self.info_panel_width
        available_height = height - 2 * self.margin
        self.cell_size = min(available_width, available_height) // self.board_size
        
        # Board offset
        self.board_x = self.margin
        self.board_y = (height - self.cell_size * self.board_size) // 2
        
        # Info panel
        self.info_x = self.board_x + self.cell_size * self.board_size + 40
        
        # Wall dimensions
        self.wall_thickness = 8
        self.wall_length = self.cell_size * 2
        
        # Fonts (will be initialized after pygame.init)
        self.font_large = None
        self.font_medium = None
        self.font_small = None
    
    def init_fonts(self):
        """Initialize fonts after pygame is initialized."""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
    
    def draw_board(self, screen):
        """Draw the game board."""
        # Draw board background
        board_rect = pygame.Rect(
            self.board_x - 10,
            self.board_y - 10,
            self.cell_size * self.board_size + 20,
            self.cell_size * self.board_size + 20
        )
        pygame.draw.rect(screen, Colors.BOARD, board_rect, border_radius=5)
        
        # Draw grid squares
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.board_x + col * self.cell_size
                y = self.board_y + row * self.cell_size
                
                # Alternate colors for checkerboard pattern
                color = Colors.SQUARE_LIGHT if (row + col) % 2 == 0 else Colors.SQUARE_DARK
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size))
                
                # Draw grid lines
                pygame.draw.rect(screen, Colors.GRID_LINE, 
                               (x, y, self.cell_size, self.cell_size), 1)
        
        # Draw goal lines
        # Player 1 goal (top row)
        pygame.draw.line(screen, Colors.PLAYER1,
                        (self.board_x, self.board_y),
                        (self.board_x + self.cell_size * self.board_size, self.board_y),
                        4)
        
        # Player 2 goal (bottom row)
        y_bottom = self.board_y + self.cell_size * self.board_size
        pygame.draw.line(screen, Colors.PLAYER2,
                        (self.board_x, y_bottom),
                        (self.board_x + self.cell_size * self.board_size, y_bottom),
                        4)
    
    def draw_valid_moves(self, screen, valid_moves):
        """Draw highlights for valid moves."""
        for row, col in valid_moves:
            x = self.board_x + col * self.cell_size
            y = self.board_y + row * self.cell_size
            
            # Create surface with alpha
            s = pygame.Surface((self.cell_size, self.cell_size))
            s.set_alpha(128)
            s.fill(Colors.VALID_MOVE[:3])
            screen.blit(s, (x, y))
            
            # Draw border
            pygame.draw.rect(screen, (50, 205, 50), 
                           (x, y, self.cell_size, self.cell_size), 3)
    
    def draw_pawns(self, screen, players):
        """Draw player pawns."""
        for player in players:
            row, col = player.position
            x = self.board_x + col * self.cell_size + self.cell_size // 2
            y = self.board_y + row * self.cell_size + self.cell_size // 2
            
            # Draw pawn as circle
            radius = self.cell_size // 3
            pygame.draw.circle(screen, player.color, (x, y), radius)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), radius, 3)
            
            # Draw player number
            text = self.font_small.render(str(player.player_id + 1), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
    
    def draw_walls(self, screen, walls):
        """Draw walls on the board."""
        for wall in walls:
            if wall.is_horizontal:
                # Horizontal wall
                x = self.board_x + wall.col * self.cell_size
                y = self.board_y + (wall.row + 1) * self.cell_size - self.wall_thickness // 2
                width = self.wall_length
                height = self.wall_thickness
            else:
                # Vertical wall
                x = self.board_x + (wall.col + 1) * self.cell_size - self.wall_thickness // 2
                y = self.board_y + wall.row * self.cell_size
                width = self.wall_thickness
                height = self.wall_length
            
            pygame.draw.rect(screen, Colors.WALL_NEUTRAL, (x, y, width, height), border_radius=3)
            pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2, border_radius=3)
    
    def draw_wall_preview(self, screen, wall):
        """Draw preview of wall being placed."""
        if wall.is_horizontal:
            x = self.board_x + wall.col * self.cell_size
            y = self.board_y + (wall.row + 1) * self.cell_size - self.wall_thickness // 2
            width = self.wall_length
            height = self.wall_thickness
        else:
            x = self.board_x + (wall.col + 1) * self.cell_size - self.wall_thickness // 2
            y = self.board_y + wall.row * self.cell_size
            width = self.wall_thickness
            height = self.wall_length
        
        # Draw semi-transparent preview
        s = pygame.Surface((width, height))
        s.set_alpha(150)
        s.fill(Colors.WALL_PREVIEW[:3])
        screen.blit(s, (x, y))
        
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height), 2, border_radius=3)
    
    def draw_info_panel(self, screen, game_state, message=""):
        """Draw information panel."""
        x = self.info_x
        y = self.board_y
        
        # Current turn
        current_player = game_state.get_current_player()
        turn_text = f"{current_player.name}'s Turn"
        turn_surf = self.font_medium.render(turn_text, True, current_player.color)
        screen.blit(turn_surf, (x, y))
        
        y += 60
        
        # Player info
        for i, player in enumerate(game_state.players):
            # Player name and color indicator
            pygame.draw.circle(screen, player.color, (x + 15, y + 15), 12)
            
            name_surf = self.font_small.render(player.name, True, Colors.TEXT)
            screen.blit(name_surf, (x + 35, y + 5))
            
            # Walls remaining
            y += 35
            walls_text = f"Walls: {player.walls_remaining}"
            walls_surf = self.font_small.render(walls_text, True, Colors.TEXT)
            screen.blit(walls_surf, (x + 35, y))
            
            y += 50
        
        # Controls
        y += 30
        controls_title = self.font_small.render("Controls:", True, Colors.TEXT)
        screen.blit(controls_title, (x, y))
        y += 35
        
        controls = [
            "Click: Move pawn",
            "W: Place wall",
            "R: Rotate wall",
            "S: Save game",
            "L: Load game",
            "ESC: Menu"
        ]
        
        for control in controls:
            control_surf = self.font_small.render(control, True, Colors.TEXT_LIGHT)
            screen.blit(control_surf, (x, y))
            y += 30
        
        # Message
        if message:
            y = self.board_y + self.cell_size * self.board_size - 80
            
            # Determine message color
            if "Invalid" in message or "Cannot" in message or "blocked" in message:
                color = Colors.ERROR
            elif "wins" in message or "Won" in message:
                color = Colors.WIN
            else:
                color = Colors.INFO
            
            msg_surf = self.font_small.render(message, True, color)
            msg_rect = msg_surf.get_rect(center=(x + 100, y))
            
            # Draw background for message
            bg_rect = msg_rect.inflate(20, 10)
            pygame.draw.rect(screen, Colors.BACKGROUND, bg_rect, border_radius=5)
            pygame.draw.rect(screen, color, bg_rect, 2, border_radius=5)
            
            screen.blit(msg_surf, msg_rect)
    
    def draw_game_over(self, screen, winner):
        """Draw game over overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Winner message
        winner_text = f"{winner.name} Wins!"
        text_surf = self.font_large.render(winner_text, True, winner.color)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(text_surf, text_rect)
        
        # Restart instruction
        restart_text = "Press R to restart or ESC for menu"
        restart_surf = self.font_medium.render(restart_text, True, Colors.TEXT_LIGHT)
        restart_rect = restart_surf.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(restart_surf, restart_rect)
    
    def get_board_position(self, mouse_pos):
        """
        Convert mouse position to board coordinates.
        
        Args:
            mouse_pos: (x, y) mouse position
            
        Returns:
            (row, col) or None if outside board
        """
        mx, my = mouse_pos
        
        # Check if within board bounds
        if (mx < self.board_x or 
            mx >= self.board_x + self.cell_size * self.board_size or
            my < self.board_y or 
            my >= self.board_y + self.cell_size * self.board_size):
            return None
        
        col = (mx - self.board_x) // self.cell_size
        row = (my - self.board_y) // self.cell_size
        
        return (row, col)
    
    def get_wall_position(self, mouse_pos, is_horizontal):
        """
        Convert mouse position to wall coordinates.
        
        Args:
            mouse_pos: (x, y) mouse position
            is_horizontal: True for horizontal wall
            
        Returns:
            Wall object or None
        """
        mx, my = mouse_pos
        
        # Calculate which wall intersection point is closest
        col = round((mx - self.board_x) / self.cell_size) - 1
        row = round((my - self.board_y) / self.cell_size) - 1
        
        # Ensure valid range
        if row < 0 or row >= self.board_size - 1 or col < 0 or col >= self.board_size - 1:
            return None
        
        return Wall(row, col, is_horizontal)
