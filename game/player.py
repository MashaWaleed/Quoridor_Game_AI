"""
Player class for Quoridor game.
"""

class Player:
    """Represents a player in the Quoridor game."""
    
    def __init__(self, player_id, start_pos, goal_row, color, name="Player"):
        """
        Initialize a player.
        
        Args:
            player_id: Unique identifier (0 or 1)
            start_pos: (row, col) starting position
            goal_row: Target row to reach to win
            color: RGB tuple for player color
            name: Player name
        """
        self.player_id = player_id
        self.position = start_pos
        self.goal_row = goal_row
        self.walls_remaining = 10
        self.color = color
        self.name = name
    
    def move(self, new_position):
        """
        Move player to new position.
        
        Args:
            new_position: (row, col) tuple
        """
        self.position = new_position
    
    def place_wall(self):
        """Decrease wall count when a wall is placed."""
        if self.walls_remaining > 0:
            self.walls_remaining -= 1
            return True
        return False
    
    def has_won(self):
        """
        Check if player has reached their goal.
        
        Returns:
            True if player's row equals goal row
        """
        return self.position[0] == self.goal_row
    
    def can_place_wall(self):
        """
        Check if player has walls remaining.
        
        Returns:
            True if player can place a wall
        """
        return self.walls_remaining > 0
    
    def to_dict(self):
        """Convert player to dictionary for saving."""
        return {
            'player_id': self.player_id,
            'position': self.position,
            'goal_row': self.goal_row,
            'walls_remaining': self.walls_remaining,
            'color': self.color,
            'name': self.name
        }
    
    @staticmethod
    def from_dict(data):
        """Create player from dictionary."""
        player = Player(
            data['player_id'],
            tuple(data['position']),
            data['goal_row'],
            tuple(data['color']),
            data['name']
        )
        player.walls_remaining = data['walls_remaining']
        return player
    
    def __repr__(self):
        """String representation of player."""
        return f"Player({self.name}, pos={self.position}, walls={self.walls_remaining})"
