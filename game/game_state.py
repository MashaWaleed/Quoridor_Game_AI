"""
GameState class to manage the overall game state.
"""

from .board import Board
from .player import Player


class GameState:
    """Manages the overall game state including players, turns, and win conditions."""
    
    def __init__(self):
        """Initialize game state."""
        self.board = Board()
        self.players = []
        self.current_player_idx = 0
        self.game_over = False
        self.winner = None
        self.move_history = []
        
    def setup_game(self, player1_name="Player 1", player2_name="Player 2"):
        """
        Set up a new game with two players.
        
        Args:
            player1_name: Name of player 1
            player2_name: Name of player 2
        """
        # Player 1 starts at bottom, tries to reach top
        player1 = Player(
            player_id=0,
            start_pos=(8, 4),  # Bottom center
            goal_row=0,  # Top row
            color=(65, 105, 225),  # Royal blue
            name=player1_name
        )
        
        # Player 2 starts at top, tries to reach bottom
        player2 = Player(
            player_id=1,
            start_pos=(0, 4),  # Top center
            goal_row=8,  # Bottom row
            color=(220, 20, 60),  # Crimson
            name=player2_name
        )
        
        self.players = [player1, player2]
        self.current_player_idx = 0
        self.game_over = False
        self.winner = None
        self.move_history = []
        
    def get_current_player(self):
        """Get the current player."""
        return self.players[self.current_player_idx]
    
    def get_opponent(self):
        """Get the opponent of current player."""
        return self.players[1 - self.current_player_idx]
    
    def make_move(self, new_position):
        """
        Move current player's pawn.
        
        Args:
            new_position: (row, col) tuple
            
        Returns:
            True if move was successful
        """
        current_player = self.get_current_player()
        opponent = self.get_opponent()
        
        valid_moves = self.board.get_valid_moves(
            current_player.position,
            opponent.position
        )
        
        if new_position in valid_moves:
            old_pos = current_player.position
            current_player.move(new_position)
            
            # Record move
            self.move_history.append(('move', self.current_player_idx, old_pos, new_position))
            
            # Check win condition
            if current_player.has_won():
                self.game_over = True
                self.winner = current_player
                return True
            
            # Switch turns
            self.next_turn()
            return True
        
        return False
    
    def place_wall(self, wall):
        """
        Place a wall for current player.
        
        Args:
            wall: Wall object
            
        Returns:
            True if wall was placed successfully
        """
        current_player = self.get_current_player()
        
        if not current_player.can_place_wall():
            return False
        
        if self.board.can_place_wall(wall, self.players):
            self.board.place_wall(wall)
            current_player.place_wall()
            
            # Record move
            self.move_history.append(('wall', self.current_player_idx, wall))
            
            # Switch turns
            self.next_turn()
            return True
        
        return False
    
    def next_turn(self):
        """Switch to next player."""
        self.current_player_idx = 1 - self.current_player_idx
    
    def get_valid_wall_positions(self):
        """
        Get all valid wall positions for current player.
        This is expensive, so use sparingly.
        
        Returns:
            List of valid Wall objects
        """
        from .wall import Wall
        
        valid_walls = []
        
        # Only check if player has walls
        if not self.get_current_player().can_place_wall():
            return valid_walls
        
        # Check all possible positions (this is expensive)
        for row in range(Board.BOARD_SIZE - 1):
            for col in range(Board.BOARD_SIZE - 1):
                for is_horizontal in [True, False]:
                    wall = Wall(row, col, is_horizontal)
                    if self.board.can_place_wall(wall, self.players):
                        valid_walls.append(wall)
        
        return valid_walls
    
    def reset(self):
        """Reset the game to initial state."""
        self.__init__()
        self.setup_game()
    
    def to_dict(self):
        """Convert game state to dictionary for saving."""
        return {
            'board': self.board.to_dict(),
            'players': [p.to_dict() for p in self.players],
            'current_player_idx': self.current_player_idx,
            'game_over': self.game_over,
            'winner_id': self.winner.player_id if self.winner else None
        }
    
    @staticmethod
    def from_dict(data):
        """Create game state from dictionary."""
        game_state = GameState()
        game_state.board = Board.from_dict(data['board'])
        game_state.players = [Player.from_dict(p) for p in data['players']]
        game_state.current_player_idx = data['current_player_idx']
        game_state.game_over = data['game_over']
        if data['winner_id'] is not None:
            game_state.winner = game_state.players[data['winner_id']]
        return game_state
