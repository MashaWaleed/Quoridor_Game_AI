"""
Color constants for the UI.
"""


class Colors:
    """Color palette for the game."""
    
    # Background colors
    BACKGROUND = (245, 245, 245)
    BOARD = (240, 230, 210)
    
    # Grid colors
    GRID_LINE = (200, 180, 150)
    SQUARE_LIGHT = (245, 235, 215)
    SQUARE_DARK = (230, 220, 200)
    
    # Player colors
    PLAYER1 = (65, 105, 225)  # Royal blue
    PLAYER2 = (220, 20, 60)   # Crimson
    
    # Highlight colors
    VALID_MOVE = (144, 238, 144, 128)  # Light green with transparency
    SELECTED = (255, 215, 0, 100)       # Gold with transparency
    WALL_PREVIEW = (100, 100, 100, 150) # Gray with transparency
    
    # Wall colors
    WALL_P1 = (65, 105, 225)  # Player 1 wall color
    WALL_P2 = (220, 20, 60)   # Player 2 wall color
    WALL_NEUTRAL = (80, 80, 80)  # Neutral wall color
    
    # UI colors
    TEXT = (50, 50, 50)
    TEXT_LIGHT = (150, 150, 150)
    BUTTON = (100, 149, 237)
    BUTTON_HOVER = (135, 170, 245)
    BUTTON_TEXT = (255, 255, 255)
    
    # Message colors
    WIN = (34, 139, 34)
    ERROR = (178, 34, 34)
    INFO = (70, 130, 180)
