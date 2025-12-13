"""
Easy AI - Greedy with occasional walls.
"""

import random
from .base_ai import BaseAI
from game.wall import Wall
from game.board import Board


class EasyAI(BaseAI):
    """Easy difficulty AI that uses simple greedy moves with basic wall placement."""
    
    def __init__(self):
        super().__init__("easy")
    
    def get_move(self, game_state):
        """
        Get a greedy move with occasional wall placement.
        
        Strategy:
        - Always move toward goal (greedy)
        - 30% chance to place a wall if available
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Tuple of ('move', position) or ('wall', Wall object)
        """
        ai_player, opponent = self._get_player_and_opponent(game_state)
        
        # 30% chance to try placing a wall if available
        if ai_player.can_place_wall() and random.random() < 0.3:
            wall = self._get_random_wall(game_state)
            if wall:
                return ('wall', wall)
        
        # Move toward goal (greedy)
        valid_moves = game_state.board.get_valid_moves(
            ai_player.position,
            opponent.position
        )
        
        if valid_moves:
            # Choose move closest to goal
            best_move = min(valid_moves, key=lambda pos: abs(pos[0] - ai_player.goal_row))
            return ('move', best_move)
        
        # Fallback: try wall if can't move
        if ai_player.can_place_wall():
            wall = self._get_random_wall(game_state)
            if wall:
                return ('wall', wall)
        
        return None
    
    def _get_random_wall(self, game_state):
        """
        Get a random valid wall position.
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Valid Wall object or None
        """
        # Try random positions (limited attempts for performance)
        max_attempts = 20
        for _ in range(max_attempts):
            row = random.randint(0, Board.BOARD_SIZE - 2)
            col = random.randint(0, Board.BOARD_SIZE - 2)
            is_horizontal = random.choice([True, False])
            
            wall = Wall(row, col, is_horizontal)
            if game_state.board.can_place_wall(wall, game_state.players):
                return wall
        
        return None
