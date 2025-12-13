"""
Wall class for Quoridor game.
"""

class Wall:
    """Represents a wall on the Quoridor board."""
    
    def __init__(self, row, col, is_horizontal):
        """
        Initialize a wall.
        
        Args:
            row: Row position of the wall
            col: Column position of the wall
            is_horizontal: True if horizontal, False if vertical
        """
        self.row = row
        self.col = col
        self.is_horizontal = is_horizontal
    
    def get_occupied_positions(self):
        """
        Get the two positions occupied by this wall.
        
        Returns:
            List of tuples representing wall segments
        """
        if self.is_horizontal:
            return [(self.row, self.col), (self.row, self.col + 1)]
        else:
            return [(self.row, self.col), (self.row + 1, self.col)]
    
    def blocks_movement(self, from_pos, to_pos):
        """
        Check if this wall blocks movement between two positions.
        
        Args:
            from_pos: (row, col) starting position
            to_pos: (row, col) ending position
            
        Returns:
            True if wall blocks this movement
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if self.is_horizontal:
            # Horizontal wall blocks vertical movement
            if from_col == to_col:  # Moving vertically
                wall_col = self.col
                # Check if moving across this wall
                if ((from_row == self.row and to_row == self.row + 1) or
                    (from_row == self.row + 1 and to_row == self.row)):
                    if from_col == wall_col or from_col == wall_col + 1:
                        return True
        else:
            # Vertical wall blocks horizontal movement
            if from_row == to_row:  # Moving horizontally
                wall_row = self.row
                # Check if moving across this wall
                if ((from_col == self.col and to_col == self.col + 1) or
                    (from_col == self.col + 1 and to_col == self.col)):
                    if from_row == wall_row or from_row == wall_row + 1:
                        return True
        
        return False
    
    def __eq__(self, other):
        """Check if two walls are equal."""
        if not isinstance(other, Wall):
            return False
        return (self.row == other.row and 
                self.col == other.col and 
                self.is_horizontal == other.is_horizontal)
    
    def __hash__(self):
        """Hash function for wall."""
        return hash((self.row, self.col, self.is_horizontal))
    
    def __repr__(self):
        """String representation of wall."""
        orientation = "H" if self.is_horizontal else "V"
        return f"Wall({self.row}, {self.col}, {orientation})"
