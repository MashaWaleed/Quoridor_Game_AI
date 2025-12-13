"""
Save and load game functionality.
"""

import json
import os
from datetime import datetime


def save_game(game_state, filename=None):
    """
    Save game state to a file.
    
    Args:
        game_state: GameState object to save
        filename: Optional filename, defaults to timestamped file
        
    Returns:
        True if save successful, False otherwise
    """
    try:
        # Create saves directory if it doesn't exist
        os.makedirs('saves', exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'saves/quoridor_save_{timestamp}.json'
        elif not filename.startswith('saves/'):
            filename = f'saves/{filename}'
        
        # Convert game state to dictionary
        save_data = game_state.to_dict()
        
        # Write to file
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"Game saved to {filename}")
        return True
    
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def load_game(filename=None):
    """
    Load game state from a file.
    
    Args:
        filename: Filename to load from, or None to load most recent
        
    Returns:
        GameState object or None if load failed
    """
    try:
        # If no filename provided, find most recent save
        if filename is None:
            if not os.path.exists('saves'):
                print("No saves directory found")
                return None
            
            saves = [f for f in os.listdir('saves') if f.endswith('.json')]
            if not saves:
                print("No save files found")
                return None
            
            # Get most recent save
            saves.sort(reverse=True)
            filename = f'saves/{saves[0]}'
        elif not filename.startswith('saves/'):
            filename = f'saves/{filename}'
        
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Save file not found: {filename}")
            return None
        
        # Load from file
        with open(filename, 'r') as f:
            save_data = json.load(f)
        
        # Import here to avoid circular dependency
        from game.game_state import GameState
        
        # Reconstruct game state
        game_state = GameState.from_dict(save_data)
        
        print(f"Game loaded from {filename}")
        return game_state
    
    except Exception as e:
        print(f"Error loading game: {e}")
        return None


def get_save_files():
    """
    Get list of available save files.
    
    Returns:
        List of save filenames
    """
    if not os.path.exists('saves'):
        return []
    
    saves = [f for f in os.listdir('saves') if f.endswith('.json')]
    saves.sort(reverse=True)
    return saves
