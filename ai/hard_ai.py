"""
Hard AI - Optimized Minimax with alpha-beta pruning and advanced heuristics.
Based on Quoridor AI research: Glendenning thesis and academic papers.
"""

import random
from .base_ai import BaseAI
from game.wall import Wall
from game.board import Board


class HardAI(BaseAI):
    """
    Hard difficulty AI using minimax algorithm with alpha-beta pruning.
    
    Key optimizations:
    - Depth 3 search with aggressive pruning
    - Superior move ordering for better alpha-beta cuts
    - Strategic wall candidate filtering (only best positions)
    - Path-length-based evaluation (core Quoridor strategy)
    - Win-detection bonuses for immediate victories
    """
    
    def __init__(self):
        super().__init__("hard")
        self.max_depth = 3  # Increased depth for stronger play
    
    def get_move(self, game_state):
        """
        Get move using minimax algorithm with alpha-beta pruning.
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Tuple of ('move', position) or ('wall', Wall object)
        """
        best_move = self._minimax_decision(game_state)
        return best_move if best_move else self._get_fallback_move(game_state)
    
    def _minimax_decision(self, game_state):
        """
        Use minimax to find best move with move ordering for efficiency.
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Best move tuple
        """
        ai_player, opponent = self._get_player_and_opponent(game_state)
        best_value = float('-inf')
        best_move = None
        
        # Get all possible moves with ordering (better moves first for pruning)
        possible_moves = self._get_ordered_moves(game_state, ai_player, opponent)
        
        alpha = float('-inf')
        beta = float('inf')
        
        # Evaluate each move
        for move_type, move_data in possible_moves:
            # Make move
            old_state = self._save_state(game_state)
            self._apply_move(game_state, move_type, move_data)
            
            # Evaluate with minimax
            value = self._minimax(game_state, self.max_depth - 1, alpha, beta, False)
            
            # Restore state
            self._restore_state(game_state, old_state)
            
            if value > best_value:
                best_value = value
                best_move = (move_type, move_data)
                alpha = max(alpha, value)
        
        return best_move
    
    def _minimax(self, game_state, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            game_state: Current GameState object
            depth: Remaining depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player's turn
            
        Returns:
            Evaluation score
        """
        # Terminal state or depth limit
        if depth == 0 or game_state.game_over:
            return self._evaluate_state(game_state)
        
        current_player = game_state.get_current_player()
        opponent = game_state.get_opponent()
        
        # Get ordered moves for better pruning
        possible_moves = self._get_ordered_moves(game_state, current_player, opponent)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move_type, move_data in possible_moves:
                old_state = self._save_state(game_state)
                self._apply_move(game_state, move_type, move_data)
                
                eval_score = self._minimax(game_state, depth - 1, alpha, beta, False)
                
                self._restore_state(game_state, old_state)
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for move_type, move_data in possible_moves:
                old_state = self._save_state(game_state)
                self._apply_move(game_state, move_type, move_data)
                
                eval_score = self._minimax(game_state, depth - 1, alpha, beta, True)
                
                self._restore_state(game_state, old_state)
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def _evaluate_state(self, game_state):
        """
        Evaluate game state using Quoridor-specific heuristics.
        
        Based on research, the most important metric is path length differential.
        Secondary factors: wall advantage, positional control.
        
        Args:
            game_state: Current GameState object
            
        Returns:
            Evaluation score (positive favors AI, negative favors opponent)
        """
        # AI is ALWAYS player 1 (index 1) in PvC mode
        ai_player = game_state.players[1]
        opponent = game_state.players[0]
        
        # Check win/loss (terminal states)
        if game_state.game_over:
            if game_state.winner == ai_player:
                return 100000
            else:
                return -100000
        
        # Check if AI can win next move (immediate win is best)
        if ai_player.position[0] == ai_player.goal_row:
            return 100000
        
        # Check if opponent can win next move (immediate loss is worst)
        if opponent.position[0] == opponent.goal_row:
            return -100000
        
        # Calculate shortest path lengths using BFS
        ai_path = game_state.board.get_shortest_path_length(
            ai_player.position, ai_player.goal_row
        )
        opp_path = game_state.board.get_shortest_path_length(
            opponent.position, opponent.goal_row
        )
        
        # If AI is one move away from winning, heavily favor it
        if ai_path == 1:
            return 50000
        
        # If opponent is one move away, heavily penalize
        if opp_path == 1:
            return -50000
        
        # Primary heuristic: path length differential (most important in Quoridor)
        # Prefer shorter path for AI, longer for opponent
        path_differential = opp_path - ai_path
        
        # Secondary heuristic: wall advantage
        # Having more walls is valuable for future blocking
        wall_differential = ai_player.walls_remaining - opponent.walls_remaining
        
        # Tertiary heuristic: progress toward goal
        # Closer to goal row is better
        ai_distance = abs(ai_player.position[0] - ai_player.goal_row)
        opp_distance = abs(opponent.position[0] - opponent.goal_row)
        progress_differential = opp_distance - ai_distance
        
        # Combined evaluation with weights from Quoridor research
        # Path differential is 10x more important than other factors
        score = (path_differential * 1000 +      # Most critical factor
                 wall_differential * 50 +         # Wall economy
                 progress_differential * 100)     # Positional advantage
        
        return score
    
    def _get_ordered_moves(self, game_state, player, opponent):
        """
        Get moves ordered by likely quality for better alpha-beta pruning.
        
        Move ordering is critical - good moves first = more pruning.
        Priority: 
        1) Winning moves
        2) Moves toward goal  
        3) High-impact walls
        
        Args:
            game_state: Current GameState object
            player: Current Player
            opponent: Opponent Player
            
        Returns:
            List of (move_type, move_data) tuples, ordered by priority
        """
        moves = []
        
        # Pawn moves (try these first)
        valid_positions = game_state.board.get_valid_moves(player.position, opponent.position)
        
        # Order pawn moves by actual path length to goal (best first)
        pawn_moves = []
        for pos in valid_positions:
            # Check if this is a winning move
            if pos[0] == player.goal_row:
                # Winning move - highest priority
                return [('move', pos)]
            
            # Temporarily move to calculate actual path length
            old_pos = player.position
            player.position = pos
            
            path_length = game_state.board.get_shortest_path_length(
                pos, player.goal_row
            )
            
            player.position = old_pos
            
            pawn_moves.append((path_length, ('move', pos)))
        
        # Sort by path length (shorter path = higher priority)
        pawn_moves.sort(key=lambda x: x[0])
        moves.extend([move for _, move in pawn_moves])
        
        # Wall placements (if available and strategic)
        if player.can_place_wall():
            strategic_walls = self._get_strategic_walls(game_state, opponent)
            
            # Limit wall candidates for performance but keep best ones
            for wall in strategic_walls[:10]:  # Top 10 strategic walls
                moves.append(('wall', wall))
        
        return moves
    
    def _get_strategic_walls(self, game_state, opponent):
        """
        Get strategic wall positions using smart filtering.
        
        Strategy from research:
        - Place walls near opponent's current position
        - Block opponent's likely paths to goal
        - Focus on horizontal walls (more effective for blocking forward progress)
        
        Args:
            game_state: Current GameState object
            opponent: Opponent Player
            
        Returns:
            List of Wall objects, ordered by strategic value
        """
        walls = []
        opp_row, opp_col = opponent.position
        
        # Get current opponent path length
        current_opp_path = game_state.board.get_shortest_path_length(
            opponent.position, opponent.goal_row
        )
        
        # Focus on area near opponent (3x3 region around opponent)
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                row = opp_row + dr
                col = opp_col + dc
                
                if 0 <= row < Board.BOARD_SIZE - 1 and 0 <= col < Board.BOARD_SIZE - 1:
                    # Try horizontal walls first (typically more effective)
                    for is_horizontal in [True, False]:
                        wall = Wall(row, col, is_horizontal)
                        
                        if game_state.board.can_place_wall(wall, game_state.players):
                            # Evaluate wall quality by path length increase
                            game_state.board.walls.append(wall)
                            
                            new_opp_path = game_state.board.get_shortest_path_length(
                                opponent.position, opponent.goal_row
                            )
                            
                            increase = new_opp_path - current_opp_path
                            
                            game_state.board.walls.remove(wall)
                            
                            # Add wall with its effectiveness score
                            walls.append((increase, wall))
        
        # Also check walls directly blocking opponent's progress toward goal
        goal_direction = 1 if opponent.goal_row > opp_row else -1
        
        # Walls immediately ahead of opponent
        for dc in range(-2, 3):
            col = opp_col + dc
            row = opp_row + goal_direction
            
            if 0 <= row < Board.BOARD_SIZE - 1 and 0 <= col < Board.BOARD_SIZE - 1:
                wall = Wall(row, col, True)  # Horizontal wall ahead
                
                if game_state.board.can_place_wall(wall, game_state.players):
                    game_state.board.walls.append(wall)
                    
                    new_opp_path = game_state.board.get_shortest_path_length(
                        opponent.position, opponent.goal_row
                    )
                    
                    increase = new_opp_path - current_opp_path
                    
                    game_state.board.walls.remove(wall)
                    
                    walls.append((increase, wall))
        
        # Sort by effectiveness (highest increase first)
        walls.sort(key=lambda x: x[0], reverse=True)
        
        # Return just the wall objects, ordered by quality
        return [wall for _, wall in walls]
    
    def _save_state(self, game_state):
        """Save game state for rollback."""
        return {
            'player_positions': [p.position for p in game_state.players],
            'walls_remaining': [p.walls_remaining for p in game_state.players],
            'walls': list(game_state.board.walls),
            'current_player_idx': game_state.current_player_idx,
            'game_over': game_state.game_over,
            'winner': game_state.winner
        }
    
    def _restore_state(self, game_state, saved_state):
        """Restore game state from saved state."""
        for i, player in enumerate(game_state.players):
            player.position = saved_state['player_positions'][i]
            player.walls_remaining = saved_state['walls_remaining'][i]
        
        game_state.board.walls = saved_state['walls']
        game_state.current_player_idx = saved_state['current_player_idx']
        game_state.game_over = saved_state['game_over']
        game_state.winner = saved_state['winner']
    
    def _apply_move(self, game_state, move_type, move_data):
        """Apply a move to game state."""
        current_player = game_state.get_current_player()
        
        if move_type == 'move':
            current_player.position = move_data
            if current_player.position[0] == current_player.goal_row:
                game_state.game_over = True
                game_state.winner = current_player
        elif move_type == 'wall':
            game_state.board.walls.append(move_data)
            current_player.walls_remaining -= 1
        
        game_state.current_player_idx = 1 - game_state.current_player_idx
    
    def _get_fallback_move(self, game_state):
        """Get fallback move if minimax fails."""
        ai_player, opponent = self._get_player_and_opponent(game_state)
        valid_moves = game_state.board.get_valid_moves(ai_player.position, opponent.position)
        
        if valid_moves:
            # Choose move that advances toward goal
            best_move = min(valid_moves, key=lambda pos: abs(pos[0] - ai_player.goal_row))
            return ('move', best_move)
        
        return None
