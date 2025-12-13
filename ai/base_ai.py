"""
Base AI class for Quoridor.
"""

from abc import ABC, abstractmethod


class BaseAI(ABC):
    """Abstract base class for AI players."""
    
    def __init__(self, difficulty="medium"):
        """
        Initialize AI.
        
        Args:
            difficulty: Difficulty level string
        """
        self.difficulty = difficulty
    
    @abstractmethod
    def get_move(self, game_state):
        """
        Get the AI's move.
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Tuple of ('move', position) or ('wall', Wall object)
        """
        pass
    
    def _get_player_and_opponent(self, game_state):
        """
        Helper to get AI player and opponent.
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Tuple of (ai_player, opponent_player)
        """
        return game_state.get_current_player(), game_state.get_opponent()
