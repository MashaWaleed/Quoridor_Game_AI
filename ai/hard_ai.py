"""
Hard AI - Based on proven Quoridor AI research.

References:
- Martijn van Steenbergen's SmartBrain (negamax depth 4)
- Monte Carlo Tree Search for Quoridor (2018 paper)

Key insight: The evaluation function should be SIMPLE:
  score = opponent_path_length - my_path_length

Wall placement should be SELECTIVE:
  Only consider walls along players' shortest paths
"""

from .base_ai import BaseAI
from game.wall import Wall
from game.board import Board


class HardAI(BaseAI):
    """
    Hard AI using negamax with alpha-beta pruning.
    
    Based on SmartBrain 4 which uses:
    - Negamax depth 4
    - Simple path differential heuristic
    - Strategic wall selection (only along shortest paths)
    """
    
    def __init__(self):
        super().__init__("hard")
        self.max_depth = 4
        self.ai_player_idx = 1
        self.last_positions = []  # Track recent positions to avoid oscillation
    
    def get_move(self, game_state):
        """Get best move using negamax search."""
        self.ai_player_idx = game_state.current_player_idx
        
        best_move = self._negamax_root(game_state)
        
        if best_move is None:
            best_move = self._get_fallback_move(game_state)
        
        return best_move
    
    def _negamax_root(self, game_state):
        """Root-level negamax to find best move."""
        ai_player = game_state.players[self.ai_player_idx]
        opponent = game_state.players[1 - self.ai_player_idx]
        
        # Get candidate moves
        moves = self._get_moves(game_state, ai_player, opponent)
        
        if not moves:
            return None
        
        best_value = float('-inf')
        best_moves = []  # Track all moves with best value for randomization
        
        alpha = float('-inf')
        beta = float('inf')
        
        for move_type, move_data in moves:
            old_state = self._save_state(game_state)
            self._apply_move(game_state, move_type, move_data)
            
            # Negamax: negate the value from opponent's perspective
            value = -self._negamax(game_state, self.max_depth - 1, -beta, -alpha)
            
            self._restore_state(game_state, old_state)
            
            if value > best_value:
                best_value = value
                best_moves = [(move_type, move_data)]
            elif value == best_value:
                best_moves.append((move_type, move_data))
            
            alpha = max(alpha, value)
        
        # Select best move - prefer moves toward goal, avoid oscillation
        if not best_moves:
            return None
        
        # Filter out moves that would return to recent positions
        non_oscillating = []
        for move_type, move_data in best_moves:
            if move_type == 'move' and move_data in self.last_positions:
                continue  # Skip recently visited positions
            non_oscillating.append((move_type, move_data))
        
        # Use non-oscillating moves if available
        candidates = non_oscillating if non_oscillating else best_moves
        
        # Among equal moves, prefer pawn moves over walls at game start
        pawn_moves = [(t, d) for t, d in candidates if t == 'move']
        if pawn_moves:
            # Prefer move that makes most progress toward goal
            best = min(pawn_moves, key=lambda m: game_state.board.get_shortest_path_length(
                m[1], ai_player.goal_row
            ))
            # Track position
            self.last_positions.append(best[1])
            if len(self.last_positions) > 4:
                self.last_positions.pop(0)
            return best
        
        # Otherwise take first wall
        return candidates[0]
    
    def _negamax(self, game_state, depth, alpha, beta):
        """Negamax with alpha-beta pruning."""
        # Terminal check
        if game_state.game_over:
            winner = game_state.winner
            current = game_state.get_current_player()
            return 10000 if winner == current else -10000
        
        if depth == 0:
            return self._evaluate(game_state)
        
        current = game_state.get_current_player()
        opponent = game_state.get_opponent()
        
        moves = self._get_moves(game_state, current, opponent)
        
        if not moves:
            return self._evaluate(game_state)
        
        best_value = float('-inf')
        
        for move_type, move_data in moves:
            old_state = self._save_state(game_state)
            self._apply_move(game_state, move_type, move_data)
            
            value = -self._negamax(game_state, depth - 1, -beta, -alpha)
            
            self._restore_state(game_state, old_state)
            
            best_value = max(best_value, value)
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break  # Pruning
        
        return best_value
    
    def _evaluate(self, game_state):
        """
        Simple evaluation: opponent_path - my_path
        
        This is the PROVEN heuristic from SmartBrain.
        """
        current = game_state.get_current_player()
        opponent = game_state.get_opponent()
        
        # Check terminal states
        if current.position[0] == current.goal_row:
            return 10000
        if opponent.position[0] == opponent.goal_row:
            return -10000
        
        my_path = game_state.board.get_shortest_path_length(
            current.position, current.goal_row
        )
        opp_path = game_state.board.get_shortest_path_length(
            opponent.position, opponent.goal_row
        )
        
        # Simple path differential - this is the key!
        return opp_path - my_path
    
    def _get_moves(self, game_state, player, opponent):
        """
        Get moves to consider.
        
        Key optimization from SmartBrain:
        1. Always consider the best pawn move (toward goal)
        2. Only consider walls along players' shortest paths
        """
        moves = []
        
        # Get valid pawn moves
        valid_positions = game_state.board.get_valid_moves(
            player.position, opponent.position
        )
        
        # Find the best pawn move (one that reduces path most)
        if valid_positions:
            # Check for immediate win
            for pos in valid_positions:
                if pos[0] == player.goal_row:
                    return [('move', pos)]  # Winning move!
            
            # Find move that gets us closest to goal
            best_pos = None
            best_path = float('inf')
            
            for pos in valid_positions:
                path = game_state.board.get_shortest_path_length(
                    pos, player.goal_row
                )
                if path < best_path:
                    best_path = path
                    best_pos = pos
            
            if best_pos:
                moves.append(('move', best_pos))
            
            # Also add other valid moves (for flexibility)
            for pos in valid_positions:
                if pos != best_pos:
                    moves.append(('move', pos))
        
        # Strategic walls - but NOT in early game (first few moves should be racing)
        # Count total moves made (approximated by walls placed)
        total_walls_placed = (10 - player.walls_remaining) + (10 - opponent.walls_remaining)
        early_game = total_walls_placed < 2
        
        # Calculate path situation
        my_path = game_state.board.get_shortest_path_length(player.position, player.goal_row)
        opp_path = game_state.board.get_shortest_path_length(opponent.position, opponent.goal_row)
        
        # Only consider walls if:
        # 1. Not early game
        # 2. We have walls to place
        # 3. Opponent is getting close OR we're behind
        should_consider_walls = (
            not early_game and
            player.can_place_wall() and
            (opp_path <= 5 or my_path > opp_path)
        )
        
        if should_consider_walls:
            strategic_walls = self._get_path_blocking_walls(game_state, player, opponent)
            
            # Limit walls to prevent search explosion
            for wall in strategic_walls[:4]:
                moves.append(('wall', wall))
        
        return moves
    
    def _get_path_blocking_walls(self, game_state, player, opponent):
        """
        Get walls that block opponent's path toward their goal.
        
        Key insight: Only place walls BETWEEN opponent and their goal,
        never behind the opponent!
        """
        walls = []
        
        opp_row, opp_col = opponent.position
        opp_goal = opponent.goal_row
        
        # Direction opponent needs to travel
        goal_direction = 1 if opp_goal > opp_row else -1
        
        current_opp_path = game_state.board.get_shortest_path_length(
            opponent.position, opponent.goal_row
        )
        current_my_path = game_state.board.get_shortest_path_length(
            player.position, player.goal_row
        )
        
        # Only consider walls IN FRONT of opponent (between them and goal)
        # Check rows from opponent toward their goal
        if goal_direction == 1:  # Opponent going down (increasing row)
            rows_to_check = range(opp_row, min(opp_row + 4, Board.BOARD_SIZE - 1))
        else:  # Opponent going up (decreasing row)
            rows_to_check = range(max(0, opp_row - 3), opp_row + 1)
        
        checked = set()
        for row in rows_to_check:
            for col in range(max(0, opp_col - 2), min(Board.BOARD_SIZE - 1, opp_col + 3)):
                if (row, col) in checked:
                    continue
                checked.add((row, col))
                
                # Try horizontal walls first (better for blocking forward progress)
                for is_horizontal in [True, False]:
                    wall = Wall(row, col, is_horizontal)
                    
                    if not game_state.board.can_place_wall(wall, game_state.players):
                        continue
                    
                    # Test the wall's effectiveness
                    game_state.board.walls.append(wall)
                    
                    new_opp_path = game_state.board.get_shortest_path_length(
                        opponent.position, opponent.goal_row
                    )
                    new_my_path = game_state.board.get_shortest_path_length(
                        player.position, player.goal_row
                    )
                    
                    game_state.board.walls.pop()
                    
                    # Calculate net benefit
                    opp_increase = new_opp_path - current_opp_path
                    my_increase = new_my_path - current_my_path
                    net_benefit = opp_increase - my_increase
                    
                    # Only keep walls that actually slow down opponent more than us
                    if net_benefit >= 1:
                        walls.append((net_benefit, wall))
        
        # Sort by effectiveness
        walls.sort(key=lambda x: x[0], reverse=True)
        
        return [w for _, w in walls]
    
    def _get_path_positions(self, game_state, player):
        """Get positions along player's shortest path using BFS."""
        from collections import deque
        
        start = player.position
        goal_row = player.goal_row
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            pos, path = queue.popleft()
            
            if pos[0] == goal_row:
                return path
            
            # Check all directions
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_pos = (pos[0] + dr, pos[1] + dc)
                
                if new_pos in visited:
                    continue
                
                if not (0 <= new_pos[0] < Board.BOARD_SIZE and 
                        0 <= new_pos[1] < Board.BOARD_SIZE):
                    continue
                
                if game_state.board.is_blocked_by_wall(pos, new_pos):
                    continue
                
                visited.add(new_pos)
                queue.append((new_pos, path + [new_pos]))
        
        return [start]  # Fallback
    
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
        """Restore game state."""
        for i, player in enumerate(game_state.players):
            player.position = saved_state['player_positions'][i]
            player.walls_remaining = saved_state['walls_remaining'][i]
        
        game_state.board.walls = saved_state['walls']
        game_state.current_player_idx = saved_state['current_player_idx']
        game_state.game_over = saved_state['game_over']
        game_state.winner = saved_state['winner']
    
    def _apply_move(self, game_state, move_type, move_data):
        """Apply a move."""
        current = game_state.get_current_player()
        
        if move_type == 'move':
            current.position = move_data
            if current.position[0] == current.goal_row:
                game_state.game_over = True
                game_state.winner = current
        elif move_type == 'wall':
            game_state.board.walls.append(move_data)
            current.walls_remaining -= 1
        
        game_state.current_player_idx = 1 - game_state.current_player_idx
    
    def _get_fallback_move(self, game_state):
        """Fallback: move toward goal."""
        player = game_state.players[self.ai_player_idx]
        opponent = game_state.players[1 - self.ai_player_idx]
        
        valid = game_state.board.get_valid_moves(
            player.position, opponent.position
        )
        
        if valid:
            # Pick move closest to goal
            best = min(valid, key=lambda p: game_state.board.get_shortest_path_length(
                p, player.goal_row
            ))
            return ('move', best)
        
        return None
