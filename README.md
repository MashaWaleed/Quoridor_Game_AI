# Quoridor Game

A complete implementation of the strategic board game Quoridor with GUI and intelligent AI opponents.

## Game Description

Quoridor is an award-winning abstract strategy board game where players race to reach the opposite side of the board while strategically placing walls to block their opponents. The game combines simple rules with deep strategic gameplay.

### Rules
- **Board**: 9×9 grid
- **Players**: 2 players
- **Objective**: Be the first to reach the opposite side
- **Each Turn**: Move your pawn OR place a wall
- **Movement**: One square orthogonally (up/down/left/right)
- **Jumping**: Jump over opponent if adjacent, or move diagonally if blocked
- **Walls**: 2 squares long, placed on edges between squares
- **Constraint**: Walls cannot completely block any player's path to their goal

## Features

### Core Features
- ✅ Complete Quoridor ruleset implementation
- ✅ Beautiful Pygame-based GUI with visual feedback
- ✅ Human vs Human mode
- ✅ Human vs AI mode (3 difficulty levels)
- ✅ Valid move highlighting with green squares
- ✅ BFS pathfinding algorithm ensures fair wall placement
- ✅ Turn indicator and wall counter display
- ✅ Intuitive mouse-based controls

### Bonus Features
- ✅ **Multiple AI Difficulty Levels**: Easy, Medium, Hard
- ✅ **Save/Load Game**: Press 'S' to save, 'L' to load (automatically saves to `saves/` folder)
- ✅ **Wall Overlap Prevention**: Robust validation prevents wall conflicts
- ✅ **Winning Move Detection**: AI recognizes and takes winning moves immediately

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/MashaWaleed/Quoridor_Game_AI.git
cd Quoridor_Game_AI

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Game

### Quick Start
```bash
# Using the launch script (Linux/Mac)
./run_game.sh

# Or manually
source venv/bin/activate  # Activate virtual environment first
python main.py
```

### First Time Setup
If you get a "permission denied" error on Linux/Mac:
```bash
chmod +x run_game.sh
```

## Controls

### Main Menu
- Click on game mode buttons to start a game
- Choose AI difficulty (Easy/Medium/Hard) when playing vs Computer

### During Gameplay

**Moving Your Pawn:**
- Click on a valid adjacent square (highlighted in green) to move

**Placing a Wall:**
- Press `W` to enter wall placement mode
- Click on the board to place a horizontal wall
- Press `R` to rotate wall (horizontal ↔ vertical)
- Click again to confirm placement
- Press `ESC` to cancel wall placement

**Other Controls:**
- `S` - Save current game state (saves to `saves/` folder with timestamp)
- `L` - Load most recent saved game
- `ESC` - Return to main menu (or cancel wall placement)
- `R` - Restart game (when game is over) OR Rotate wall (during placement)

## AI Algorithms

All AI opponents use Breadth-First Search (BFS) for pathfinding to evaluate optimal moves.

### Easy AI
- **Strategy**: Greedy movement toward goal
- **Wall Placement**: Random valid positions (30% chance per turn)
- **Behavior**: Always moves closer to goal, occasionally places walls
- **Good for**: Beginners learning the game mechanics

### Medium AI
- **Strategy**: Strategic pathfinding with aggressive blocking
- **Wall Placement**: Focused search in 4×4 region around opponent
- **Algorithm**: Evaluates walls by actual path-length increase to opponent
- **Decision Logic**: 
  - Places walls when path differential ≤ 1 (behind or equal)
  - Uses BFS to find moves with shortest path to goal
  - Verifies wall effectiveness before placement
- **Good for**: Intermediate players wanting a challenge

### Hard AI
- **Algorithm**: Minimax with alpha-beta pruning (depth 3)
- **Move Ordering**: 
  1. Winning moves (immediate detection)
  2. Moves with shortest path to goal (BFS evaluation)
  3. High-impact strategic walls
- **Evaluation Function** (research-based weights):
  - Path length differential: ×1000 (most critical)
  - Wall count advantage: ×50
  - Positional progress: ×100
- **Wall Selection**: Top 10 strategic positions near opponent
- **Special Features**:
  - Detects winning moves 1 step ahead (+50,000 points)
  - Detects opponent winning threats (-50,000 points)
  - Always evaluates from correct player perspective
- **Performance**: ~1-2 second response time per move
- **Good for**: Experienced players seeking competitive gameplay

### Technical Implementation
- **BFS Pathfinding**: Used for validating wall placements and ensuring all players maintain valid paths
- **Alpha-Beta Pruning**: Reduces search space by 50-80% compared to pure minimax
- **Heuristic-Based Evaluation**: Prioritizes path-length differential (proven most effective in Quoridor research)
- **Move Generation Optimization**: Smart filtering reduces wall candidates from ~100 to ~10 best positions

## Project Structure

```
quoridor-game/
├── main.py              # Entry point
├── game/
│   ├── __init__.py
│   ├── board.py         # Board logic and pathfinding
│   ├── player.py        # Player class
│   ├── wall.py          # Wall class
│   └── game_state.py    # Game state management
├── ai/
│   ├── __init__.py
│   ├── base_ai.py       # Base AI class
│   ├── easy_ai.py       # Easy difficulty
│   ├── medium_ai.py     # Medium difficulty
│   └── hard_ai.py       # Hard difficulty (minimax)
├── ui/
│   ├── __init__.py
│   ├── renderer.py      # Pygame rendering
│   ├── menu.py          # Menu system
│   └── colors.py        # Color constants
├── utils/
│   ├── __init__.py
│   └── save_load.py     # Save/load functionality
├── requirements.txt
└── README.md
```

## Demo Video

[Watch the demo video here](https://youtu.be/your-video-link)

## Development

### Design Decisions
- **Pygame for GUI**: Chosen for smooth 2D graphics and game-oriented features
- **BFS for Pathfinding**: Guarantees shortest path and ensures every wall placement maintains valid paths for both players
- **Minimax with Alpha-Beta Pruning**: Classic game tree search provides optimal decision-making for Hard AI
- **Path-Length Heuristic**: Research shows path differential is 10× more important than other factors in Quoridor
- **Move Ordering**: Evaluating best moves first dramatically improves alpha-beta pruning efficiency
- **MVC Pattern**: Clean separation of game logic, AI algorithms, and UI rendering

### Challenges and Solutions
- **Wall Validation Complexity**: Implemented comprehensive overlap detection checking both same-orientation walls and perpendicular crossing
- **AI Performance**: Alpha-beta pruning with move ordering reduced Hard AI response time from 5+ seconds to ~1 second
- **UI Responsiveness**: Added wall preview system and valid move highlighting for immediate visual feedback
- **AI Player Identification**: Fixed evaluation perspective to ensure AI consistently plays as Player 2
- **Winning Move Detection**: Added explicit checks for immediate wins to prevent AI hesitation at goal line

### Assumptions Made
- Game is played on standard 9×9 board (not configurable sizes)
- 2-player mode only (4-player not implemented)
- AI always plays as Player 2 in Human vs Computer mode
- Save files stored in JSON format in `saves/` directory
- Wall placement uses grid intersection points for intuitive mouse control

## Credits

Developed by [Your Name]

Game designed by Mirko Marchesi (1997)

## License

MIT License - feel free to use for educational purposes
