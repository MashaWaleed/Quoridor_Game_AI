"""
Medium AI - Strategic pathfinding with aggressive wall placement.
"""

import random
from .base_ai import BaseAI
from game.wall import Wall
from game.board import Board


class MediumAI(BaseAI):
    """Medium difficulty AI using strategic pathfinding and smart blocking."""
    
    def __init__(self):
        super().__init__("medium")
    
    def get_move(self, game_state):
        """
        Get move using strategic approach.
        
        Strategy:
        - Move toward goal when clearly ahead (path diff > 2)
        - Block opponent aggressively when behind or close
        - Prioritize walls that maximize opponent's path length
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Tuple of ('move', position) or ('wall', Wall object)
        """
        ai_player, opponent = self._get_player_and_opponent(game_state)
        
        # Get path lengths
        ai_path_length = game_state.board.get_shortest_path_length(
            ai_player.position, ai_player.goal_row
        )
        opp_path_length = game_state.board.get_shortest_path_length(
            opponent.position, opponent.goal_row
        )
        
        path_diff = ai_path_length - opp_path_length
        
        # Decision logic: be aggressive with walls
        # Place wall if: behind, equal, or only slightly ahead
        if (ai_player.can_place_wall() and 
            path_diff >= -1 and  # Not too far ahead
            ai_player.walls_remaining > 0):
            
            # Try to find a good blocking wall
            wall = self._find_best_blocking_wall(game_state, opponent)
            
            # Use wall if it increases opponent's path by at least 1
            if wall:
                # Verify it actually helps
                game_state.board.walls.append(wall)
                new_opp_path = game_state.board.get_shortest_path_length(
                    opponent.position, opponent.goal_row
                )
                game_state.board.walls.remove(wall)
                
                if new_opp_path > opp_path_length:
                    return ('wall', wall)
        
        # Otherwise, move toward goal strategically
        best_move = self._find_best_move(game_state, ai_player, opponent)
        if best_move:
            return ('move', best_move)
        
        # Fallback: random valid move
        valid_moves = game_state.board.get_valid_moves(
            ai_player.position,
            opponent.position
        )
        if valid_moves:
            return ('move', random.choice(valid_moves))
        
        return None
    
    def _find_best_move(self, game_state, ai_player, opponent):
        """
        Find move that minimizes path length to goal (not just distance).
        
        Args:
            game_state: Current GameState object
            ai_player: AI Player object
            opponent: Opponent Player object
            
        Returns:
            Best position tuple or None
        """
        valid_moves = game_state.board.get_valid_moves(
            ai_player.position,
            opponent.position
        )
        
        if not valid_moves:
            return None
        
        # If only one move from winning, take it!
        for move in valid_moves:
            if move[0] == ai_player.goal_row:
                return move
        
        # Otherwise, choose move that results in shortest path to goal
        best_move = None
        best_path_length = float('inf')
        
        for move in valid_moves:
            # Temporarily move to check path length
            old_pos = ai_player.position
            ai_player.position = move
            
            path_length = game_state.board.get_shortest_path_length(
                move, ai_player.goal_row
            )
            
            ai_player.position = old_pos
            
            if path_length < best_path_length:
                best_path_length = path_length
                best_move = move
        
        return best_move
    
    def _find_best_blocking_wall(self, game_state, opponent):
        """
        Find wall that maximizes opponent's path length.
        
        More thorough search than Easy AI.
        
        Args:
            game_state: Current GameState object
            opponent: Opponent Player object
            
        Returns:
            Wall object or None
        """
        current_opp_length = game_state.board.get_shortest_path_length(
            opponent.position, opponent.goal_row
        )
        
        best_wall = None
        best_increase = 0
        
        # Try walls near opponent (4x4 region)
        opp_row, opp_col = opponent.position
        
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                row = opp_row + dr
                col = opp_col + dc
                
                if 0 <= row < Board.BOARD_SIZE - 1 and 0 <= col < Board.BOARD_SIZE - 1:
                    # Try horizontal first (usually better for blocking)
                    for is_horizontal in [True, False]:
                        wall = Wall(row, col, is_horizontal)
                        
                        if game_state.board.can_place_wall(wall, game_state.players):
                            # Temporarily place wall to test
                            game_state.board.walls.append(wall)
                            
                            new_opp_length = game_state.board.get_shortest_path_length(
                                opponent.position, opponent.goal_row
                            )
                            
                            increase = new_opp_length - current_opp_length
                            
                            if increase > best_increase:
                                best_increase = increase
                                best_wall = Wall(row, col, is_horizontal)
                            
                            # Remove wall
                            game_state.board.walls.remove(wall)
        
        return best_wall
