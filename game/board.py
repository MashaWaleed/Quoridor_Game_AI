"""
Board class with game logic and pathfinding for Quoridor.
"""

from collections import deque
from .wall import Wall


class Board:
    """Manages the Quoridor game board, moves, and wall placements."""
    
    BOARD_SIZE = 9
    
    def __init__(self):
        """Initialize the game board."""
        self.walls = []  # List of Wall objects
        
    def is_valid_position(self, row, col):
        """
        Check if position is within board bounds.
        
        Args:
            row, col: Position to check
            
        Returns:
            True if position is valid
        """
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def get_valid_moves(self, player_pos, opponent_pos):
        """
        Get all valid moves for a player.
        
        Args:
            player_pos: (row, col) current player position
            opponent_pos: (row, col) opponent position
            
        Returns:
            List of valid (row, col) positions
        """
        valid_moves = []
        row, col = player_pos
        
        # Four orthogonal directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds
            if not self.is_valid_position(new_row, new_col):
                continue
            
            # Check if blocked by wall
            if self.is_blocked_by_wall(player_pos, (new_row, new_col)):
                continue
            
            # If opponent is in this position, handle jumping
            if (new_row, new_col) == opponent_pos:
                # Try to jump over opponent
                jump_row, jump_col = new_row + dr, new_col + dc
                
                # Check if can jump straight over
                if (self.is_valid_position(jump_row, jump_col) and
                    not self.is_blocked_by_wall(opponent_pos, (jump_row, jump_col))):
                    valid_moves.append((jump_row, jump_col))
                else:
                    # Blocked behind opponent, try diagonal moves
                    perpendicular = [(dc, dr), (-dc, -dr)]  # 90 degree rotations
                    for dpr, dpc in perpendicular:
                        diag_row, diag_col = new_row + dpr, new_col + dpc
                        if (self.is_valid_position(diag_row, diag_col) and
                            not self.is_blocked_by_wall(opponent_pos, (diag_row, diag_col))):
                            valid_moves.append((diag_row, diag_col))
            else:
                # Normal move to empty square
                valid_moves.append((new_row, new_col))
        
        return valid_moves
    
    def is_blocked_by_wall(self, from_pos, to_pos):
        """
        Check if movement from one position to another is blocked by a wall.
        
        Args:
            from_pos: (row, col) starting position
            to_pos: (row, col) ending position
            
        Returns:
            True if blocked by any wall
        """
        for wall in self.walls:
            if wall.blocks_movement(from_pos, to_pos):
                return True
        return False
    
    def can_place_wall(self, wall, players):
        """
        Check if a wall can be legally placed.
        
        Args:
            wall: Wall object to place
            players: List of Player objects
            
        Returns:
            True if wall placement is valid
        """
        # Check if wall is within bounds
        if wall.is_horizontal:
            if wall.row < 0 or wall.row >= self.BOARD_SIZE - 1:
                return False
            if wall.col < 0 or wall.col >= self.BOARD_SIZE - 1:
                return False
        else:
            if wall.row < 0 or wall.row >= self.BOARD_SIZE - 1:
                return False
            if wall.col < 0 or wall.col >= self.BOARD_SIZE - 1:
                return False
        
        # Check if wall overlaps or crosses existing walls
        if self._wall_conflicts(wall):
            return False
        
        # Check if wall blocks all paths for any player (temporarily place wall)
        self.walls.append(wall)
        
        for player in players:
            if not self.has_path_to_goal(player.position, player.goal_row):
                self.walls.remove(wall)
                return False
        
        self.walls.remove(wall)
        return True
    
    def _wall_conflicts(self, new_wall):
        """
        Check if new wall conflicts with existing walls.
        
        Args:
            new_wall: Wall object to check
            
        Returns:
            True if there's a conflict
        """
        new_positions = set(new_wall.get_occupied_positions())
        
        for wall in self.walls:
            # Check for exact overlap
            if wall == new_wall:
                return True
            
            # Check if same orientation and any overlap
            if wall.is_horizontal == new_wall.is_horizontal:
                existing_positions = set(wall.get_occupied_positions())
                if new_positions & existing_positions:  # Any intersection
                    return True
            
            # Check for crossing walls (different orientations)
            if self._walls_cross(wall, new_wall):
                return True
        
        return False
    
    def _walls_cross(self, wall1, wall2):
        """
        Check if two walls cross each other.
        
        Args:
            wall1, wall2: Wall objects
            
        Returns:
            True if walls cross
        """
        # Walls cross if they have different orientations and intersect
        if wall1.is_horizontal == wall2.is_horizontal:
            return False
        
        if wall1.is_horizontal:
            h_wall, v_wall = wall1, wall2
        else:
            h_wall, v_wall = wall2, wall1
        
        # Check if they meet at the center intersection point
        if (h_wall.row == v_wall.row and h_wall.col == v_wall.col):
            return True
        
        return False
    
    def place_wall(self, wall):
        """
        Place a wall on the board.
        
        Args:
            wall: Wall object to place
        """
        self.walls.append(wall)
    
    def has_path_to_goal(self, start_pos, goal_row):
        """
        Use BFS to check if there's a valid path from start position to goal row.
        
        Args:
            start_pos: (row, col) starting position
            goal_row: Target row number
            
        Returns:
            True if path exists
        """
        if start_pos[0] == goal_row:
            return True
        
        visited = set()
        queue = deque([start_pos])
        visited.add(start_pos)
        
        while queue:
            current = queue.popleft()
            row, col = current
            
            # Check if reached goal
            if row == goal_row:
                return True
            
            # Explore neighbors (without considering opponent, just walls)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                new_pos = (new_row, new_col)
                
                if (self.is_valid_position(new_row, new_col) and
                    new_pos not in visited and
                    not self.is_blocked_by_wall(current, new_pos)):
                    
                    visited.add(new_pos)
                    queue.append(new_pos)
        
        return False
    
    def get_shortest_path_length(self, start_pos, goal_row):
        """
        Get length of shortest path to goal using BFS.
        
        Args:
            start_pos: (row, col) starting position
            goal_row: Target row
            
        Returns:
            Shortest path length, or infinity if no path
        """
        if start_pos[0] == goal_row:
            return 0
        
        visited = set()
        queue = deque([(start_pos, 0)])
        visited.add(start_pos)
        
        while queue:
            current, dist = queue.popleft()
            row, col = current
            
            # Explore neighbors
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                new_pos = (new_row, new_col)
                
                if (self.is_valid_position(new_row, new_col) and
                    new_pos not in visited and
                    not self.is_blocked_by_wall(current, new_pos)):
                    
                    if new_row == goal_row:
                        return dist + 1
                    
                    visited.add(new_pos)
                    queue.append((new_pos, dist + 1))
        
        return float('inf')
    
    def to_dict(self):
        """Convert board state to dictionary for saving."""
        return {
            'walls': [(w.row, w.col, w.is_horizontal) for w in self.walls]
        }
    
    @staticmethod
    def from_dict(data):
        """Create board from dictionary."""
        board = Board()
        board.walls = [Wall(w[0], w[1], w[2]) for w in data['walls']]
        return board
