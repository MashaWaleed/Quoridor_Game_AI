"""
Quoridor Game - Main entry point

A complete implementation of the strategic board game Quoridor.
Features Human vs Human and Human vs AI gameplay with multiple difficulty levels.
"""

import pygame
import sys
from game.game_state import GameState
from ui.renderer import Renderer
from ui.menu import Menu
from ui.colors import Colors
from ai.easy_ai import EasyAI
from ai.medium_ai import MediumAI
from ai.hard_ai import HardAI
from utils.save_load import save_game, load_game
from game.wall import Wall


class QuoridorGame:
    """Main game controller."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        
        # Screen setup
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quoridor")
        
        # Game components
        self.game_state = GameState()
        self.renderer = Renderer(self.width, self.height)
        self.renderer.init_fonts()
        self.menu = Menu(self.width, self.height)
        
        # Game mode
        self.mode = None  # 'pvp' or 'pvc'
        self.ai = None
        self.ai_thinking = False
        
        # UI state
        self.in_menu = True
        self.in_difficulty_select = False
        self.wall_placement_mode = False
        self.wall_preview = None
        self.wall_is_horizontal = True
        self.message = ""
        self.message_timer = 0
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Setup main menu
        self._setup_main_menu()
    
    def _setup_main_menu(self):
        """Setup main menu callbacks."""
        self.menu.setup_main_menu({
            'pvp': self._start_pvp,
            'pvc': self._show_difficulty_select
        })
    
    def _show_difficulty_select(self):
        """Show difficulty selection menu."""
        self.in_difficulty_select = True
        self.menu.setup_difficulty_menu({
            'easy': lambda: self._start_pvc('easy'),
            'medium': lambda: self._start_pvc('medium'),
            'hard': lambda: self._start_pvc('hard'),
            'back': self._setup_main_menu
        })
    
    def _start_pvp(self):
        """Start Player vs Player game."""
        self.mode = 'pvp'
        self.ai = None
        self.in_menu = False
        self.in_difficulty_select = False
        self.wall_placement_mode = False
        self.wall_preview = None
        self.game_state = GameState()  # Create fresh game state
        self.game_state.setup_game("Player 1", "Player 2")
        self.set_message("Player vs Player - Player 1's turn")
    def _start_pvc(self, difficulty):
        """Start Player vs Computer game."""
        self.mode = 'pvc'
        self.in_menu = False
        self.in_difficulty_select = False
        self.wall_placement_mode = False
        self.wall_preview = None
        
        # Create AI based on difficulty
        if difficulty == 'easy':
            self.ai = EasyAI()
        elif difficulty == 'medium':
            self.ai = MediumAI()
        else:
            self.ai = HardAI()
        
        self.game_state = GameState()  # Create fresh game state
        self.game_state.setup_game("Player", f"AI ({difficulty.capitalize()})")
        self.set_message(f"Player vs AI ({difficulty.capitalize()}) - Your turn")
        
        self.game_state.setup_game("Player", f"AI ({difficulty.capitalize()})")
        self.set_message(f"Player vs AI ({difficulty.capitalize()}) - Your turn")
    
    def set_message(self, msg, duration=180):
        """
        Set a temporary message.
        
        Args:
            msg: Message text
            duration: Duration in frames (180 = 3 seconds at 60 fps)
        """
        self.message = msg
        self.message_timer = duration
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Menu handling
            if self.in_menu or self.in_difficulty_select:
                self.menu.handle_event(event)
                continue
            
            # Game events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to menu
                    self.in_menu = True
                    self._setup_main_menu()
                    self.wall_placement_mode = False
                    
                elif event.key == pygame.K_r:
                    if self.game_state.game_over:
                        # Restart game
                        if self.mode == 'pvp':
                            self._start_pvp()
                        else:
                            # Restart with same AI
                            difficulty = self.ai.difficulty
                            self._start_pvc(difficulty)
                    else:
                        # Toggle wall rotation
                        if self.wall_placement_mode:
                            self.wall_is_horizontal = not self.wall_is_horizontal
                            self.set_message(f"Wall orientation: {'Horizontal' if self.wall_is_horizontal else 'Vertical'}", 60)
                
                elif event.key == pygame.K_w:
                    # Enter wall placement mode
                    if not self.game_state.game_over and not self.ai_thinking:
                        current_player = self.game_state.get_current_player()
                        if current_player.can_place_wall():
                            self.wall_placement_mode = True
                            self.set_message("Wall placement mode - Click to place, R to rotate, ESC to cancel", 180)
                        else:
                            self.set_message("No walls remaining!", 120)
                
                elif event.key == pygame.K_s:
                    # Save game
                    if not self.game_state.game_over:
                        if save_game(self.game_state):
                            self.set_message("Game saved!", 120)
                        else:
                            self.set_message("Save failed!", 120)
                
                elif event.key == pygame.K_l:
                    # Load game
                    loaded_state = load_game()
                    if loaded_state:
                        self.game_state = loaded_state
                        self.mode = 'pvp'  # Loaded games default to PvP
                        self.ai = None
                        self.in_menu = False
                        self.set_message("Game loaded!", 120)
                    else:
                        self.set_message("Load failed!", 120)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.game_state.game_over and not self.ai_thinking:
                    self._handle_click(event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                if self.wall_placement_mode:
                    self._update_wall_preview(event.pos)
        
        return True
    
    def _handle_click(self, pos):
        """Handle mouse click."""
        # Check if in PvC mode and it's AI's turn
        if self.mode == 'pvc' and self.game_state.current_player_idx == 1:
            return
        
        if self.wall_placement_mode:
            # Place wall
            self._place_wall(pos)
        else:
            # Move pawn
            self._move_pawn(pos)
    
    def _move_pawn(self, pos):
        """Attempt to move pawn to clicked position."""
        board_pos = self.renderer.get_board_position(pos)
        if board_pos is None:
            return
        
        if self.game_state.make_move(board_pos):
            self.set_message(f"{self.game_state.get_opponent().name} moved", 60)
            
            # Check if game is over
            if self.game_state.game_over:
                self.set_message(f"{self.game_state.winner.name} wins!", 999999)
        else:
            self.set_message("Invalid move!", 90)
    
    def _place_wall(self, pos):
        """Attempt to place wall at clicked position."""
        wall = self.renderer.get_wall_position(pos, self.wall_is_horizontal)
        
        if wall is None:
            self.set_message("Invalid wall position!", 90)
            return
        
        if self.game_state.place_wall(wall):
            self.wall_placement_mode = False
            self.wall_preview = None
            self.set_message(f"{self.game_state.get_opponent().name} placed wall", 60)
        else:
            self.set_message("Cannot place wall here!", 90)
    
    def _update_wall_preview(self, pos):
        """Update wall preview position."""
        self.wall_preview = self.renderer.get_wall_position(pos, self.wall_is_horizontal)
    
    def update(self):
        """Update game state."""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""
        
        # Handle AI turn
        if (self.mode == 'pvc' and 
            not self.game_state.game_over and 
            not self.ai_thinking and
            self.game_state.current_player_idx == 1):
            self._ai_make_move()
    
    def _ai_make_move(self):
        """Let AI make its move."""
        self.ai_thinking = True
        self.set_message("AI is thinking...", 999999)
        
        # Get AI move
        move = self.ai.get_move(self.game_state)
        
        if move:
            move_type, move_data = move
            
            if move_type == 'move':
                self.game_state.make_move(move_data)
                self.set_message("AI moved", 90)
            elif move_type == 'wall':
                self.game_state.place_wall(move_data)
                self.set_message("AI placed wall", 90)
        
        self.ai_thinking = False
        
        # Check if game is over
        if self.game_state.game_over:
            self.set_message(f"{self.game_state.winner.name} wins!", 999999)
    
    def render(self):
        """Render the game."""
        self.screen.fill(Colors.BACKGROUND)
        
        if self.in_menu or self.in_difficulty_select:
            # Render menu
            self.menu.draw(self.screen, self.renderer.font_large, self.renderer.font_medium)
        else:
            # Only render game if players are initialized
            if not self.game_state.players:
                pygame.display.flip()
                return
            
            # Render game
            self.renderer.draw_board(self.screen)
            
            # Draw valid moves if not in wall placement mode
            if not self.wall_placement_mode and not self.game_state.game_over:
                current_player = self.game_state.get_current_player()
                opponent = self.game_state.get_opponent()
                
                # Only show valid moves for human player
                if self.mode == 'pvp' or self.game_state.current_player_idx == 0:
                    valid_moves = self.game_state.board.get_valid_moves(
                        current_player.position,
                        opponent.position
                    )
                    self.renderer.draw_valid_moves(self.screen, valid_moves)
            
            # Draw walls
            self.renderer.draw_walls(self.screen, self.game_state.board.walls)
            
            # Draw wall preview
            if self.wall_placement_mode and self.wall_preview:
                # Check if valid before drawing
                if self.game_state.board.can_place_wall(self.wall_preview, self.game_state.players):
                    self.renderer.draw_wall_preview(self.screen, self.wall_preview)
            
            # Draw pawns
            self.renderer.draw_pawns(self.screen, self.game_state.players)
            
            # Draw info panel
            self.renderer.draw_info_panel(self.screen, self.game_state, self.message)
            
            # Draw game over overlay
            if self.game_state.game_over:
                self.renderer.draw_game_over(self.screen, self.game_state.winner)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = QuoridorGame()
    game.run()


if __name__ == "__main__":
    main()
