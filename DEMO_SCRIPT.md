# Quoridor Game - Demo Script

## Duration: 3-5 minutes

---

## INTRODUCTION (30 seconds)

**[Screen: Main Menu]**

"Hello! Today I'm demonstrating my Quoridor game implementation - a strategic board game where players race to reach the opposite side while strategically placing walls to block their opponents.

This project features a complete Pygame GUI, full rule implementation, and three AI opponents using different algorithms. Let's dive in!"

---

## PART 1: GAME OVERVIEW & HUMAN VS HUMAN (45 seconds)

**[Screen: Main Menu → Click "Player vs Player"]**

"First, let me show you the basic gameplay in Player vs Player mode."

**[Gameplay Demo]**

"The objective is simple: be the first to reach the opposite side. You can see:
- The 9×9 board with alternating colored squares
- Player 1 (blue) starts at the bottom, trying to reach the top
- Player 2 (red) starts at the top, trying to reach the bottom
- Each player has 10 walls displayed on the right panel

On each turn, you either MOVE your pawn or PLACE a wall."

**[Demonstrate Movement]**

"Valid moves are highlighted in green. I'll click to move Player 1 forward."

**[Demonstrate Wall Placement]**

"Now let's place a wall. I press 'W' to enter wall placement mode. The wall preview appears. I can press 'R' to rotate between horizontal and vertical. Click to place.

Notice the important constraint: walls cannot completely block a player's path. The game uses BFS pathfinding to verify this - if a wall would block all paths, it's rejected."

**[Make a few moves, show jumping]**

"When pawns are adjacent, you can jump over the opponent - watch this. And the game automatically detects when someone wins."

---

## PART 2: EASY AI - GREEDY ALGORITHM (1 minute)

**[Screen: Return to Menu → Player vs Computer → Easy AI]**

"Now let's explore the AI opponents, starting with Easy difficulty.

**Easy AI Algorithm:**
- Uses a **greedy strategy** for movement
- Always moves toward its goal row using the shortest Euclidean distance
- Places walls randomly with 30% probability per turn
- No strategic planning or opponent consideration

Let me start a game against Easy AI."

**[Play a few turns]**

"Watch how the AI behaves:
- [AI moves] See? It moved directly toward its goal - pure greedy behavior
- [Your turn] I'll place a wall in its path
- [AI moves again] The AI doesn't strategically avoid my walls - it just recalculates the closest move to its goal
- [Wait for AI to place wall] When it places walls, they're random and rarely effective

The Easy AI is perfect for beginners learning the game mechanics, but it's quite beatable because it lacks strategic depth."

**[Win or show clear advantage, then return to menu]**

---

## PART 3: MEDIUM AI - STRATEGIC PATHFINDING (1 minute 15 seconds)

**[Screen: Menu → Player vs Computer → Medium AI]**

"Medium AI is a significant step up in difficulty.

**Medium AI Algorithm:**
- Uses **BFS (Breadth-First Search)** for all decision-making
- For movement: evaluates each possible move by running BFS to calculate actual path length to goal - not just distance
- For wall placement: performs a **4×4 grid search** around the opponent
- Tests each wall candidate by placing it temporarily and running BFS to measure path length increase
- Only places walls that actually increase the opponent's path length
- Decision logic: places walls when path differential ≤ 1 (when behind or equal)

This is much smarter than Easy AI. Let me demonstrate."

**[Play against Medium AI]**

"Watch the difference:
- [AI moves] The AI chose this move because BFS determined it has the shortest actual path, considering walls
- [You move, then AI places wall] See how it placed a wall near my position? That's the 4×4 region search in action
- [Continue playing] Notice it's actively trying to block my path while advancing toward its goal
- The walls aren't random anymore - each one increases my path length

The Medium AI understands that in Quoridor, it's not just about distance, but about actual reachable paths through walls."

**[Show a challenging position, explain the AI's strategic thinking]**

---

## PART 4: HARD AI - MINIMAX WITH ALPHA-BETA PRUNING (1 minute 30 seconds)

**[Screen: Menu → Player vs Computer → Hard AI]**

"Finally, the Hard AI - this is the most challenging opponent.

**Hard AI Algorithm:**
- Implements **Minimax with alpha-beta pruning** - a game tree search algorithm
- Searches **3 moves ahead** (AI → Opponent → AI)
- Uses **move ordering** to evaluate best moves first, maximizing alpha-beta cutoffs

**The evaluation function** is based on Quoridor research:
- Path length differential: ×1000 weight (most critical factor)
- Wall count advantage: ×50 weight
- Positional progress: ×100 weight

**Special optimizations:**
- Detects winning moves immediately (returns +100,000 points)
- Detects opponent threats 1 move away (−50,000 penalty)
- Limits wall candidates to top 10 strategic positions
- This reduces search space by 60-70%

**Performance:**
- Explores 5,000-8,000 nodes per move
- Response time: 1-2 seconds
- Win rate vs Medium AI: 85-90%

Let me show you."

**[Play against Hard AI - take your time with moves]**

"Notice the 'AI is thinking...' message - it's exploring the game tree.

- [AI makes first move] The AI chose this because after searching 3 moves deep, this position scores highest
- [You make a move]
- [AI moves] Watch how it doesn't just move forward - it's considering my potential responses
- [Continue playing] The Hard AI is much more defensive and strategic
- [If AI places wall] See how it blocked my best path? That came from minimax evaluation
- [If you try to win] Watch - if I get close to winning... [AI blocks] The AI detected the threat and blocked immediately

The minimax algorithm makes the Hard AI play near-optimally by assuming both players will make their best possible moves."

**[Show challenging gameplay or strategic wall placement]**

---

## PART 5: ADDITIONAL FEATURES (30 seconds)

**[During gameplay]**

"The game also includes practical features:

**Save/Load System:**
- Press 'S' to save - [show custom name dialog] you get a dialog to name your save file
- Press 'L' to load - [show file browser dialog] a file browser shows all saved games sorted by date

**Visual Feedback:**
- Valid moves are highlighted in green
- Wall preview shows exactly where walls will be placed
- Turn indicator shows whose move it is
- Wall counters update in real-time

All game mechanics are fully implemented:
- Pawn jumping over adjacent opponents
- Diagonal moves when jumps are blocked
- BFS validation ensures walls never completely block paths
- Win detection is immediate"

---

## CONCLUSION (20 seconds)

**[Screen: Show game state or return to menu]**

"This project demonstrates:
- Complete game implementation with all Quoridor rules
- Three distinct AI algorithms: Greedy, BFS-based strategic search, and Minimax
- Clean MVC architecture separating game logic, AI, and UI
- Professional features like save/load with custom dialogs

The full source code and documentation are available on GitHub. Thank you for watching!"

**[End screen: GitHub URL shown]**

---

## TECHNICAL NOTES FOR RECORDING

### Before Recording:
1. Close unnecessary applications
2. Clean desktop/background
3. Set screen resolution to 1920×1080
4. Test microphone levels
5. Have the game already open on main menu
6. Clear any existing save files or prepare specific saves

### Camera/Recording:
- Record game window + voice
- Use screen capture software (OBS Studio recommended)
- 1080p at 30fps minimum
- Include mouse cursor in recording

### Timing Breakdown:
- Introduction: 0:00 - 0:30
- PvP Demo: 0:30 - 1:15
- Easy AI: 1:15 - 2:15
- Medium AI: 2:15 - 3:30
- Hard AI: 3:30 - 5:00
- Features: 5:00 - 5:30
- Conclusion: 5:30 - 5:50

### Tips:
- Speak clearly and at moderate pace
- Pause briefly between sections
- If you make a mistake, pause 3 seconds and restart that sentence (easy to edit)
- Keep mouse movements smooth and deliberate
- Don't rush the AI demonstrations - let viewers see the thinking process

### Backup Plan:
If you go over 5 minutes, you can speed up:
- PvP section (just show basic movement and one wall)
- Medium AI section (shorter explanation, same demonstration)
- Features section (show dialogs quickly, mention features faster)

Target: 4:30 - 5:00 minutes is ideal
Maximum: 5:30 minutes

---

## KEYBOARD SHORTCUTS TO REMEMBER

During recording, you'll use:
- **Mouse Click**: Move pawn
- **W**: Enter wall placement mode
- **R**: Rotate wall
- **S**: Save game (with dialog)
- **L**: Load game (with dialog)
- **ESC**: Return to menu / Cancel wall

Make sure to mention these naturally during the demo!

---

## POST-PRODUCTION CHECKLIST

After recording:
- [ ] Trim any dead air at start/end
- [ ] Add title card with project name
- [ ] Add text overlay for GitHub URL at end
- [ ] Add section markers (optional): "Easy AI", "Medium AI", "Hard AI"
- [ ] Normalize audio levels
- [ ] Add background music (optional, very quiet)
- [ ] Export at 1080p
- [ ] Upload to YouTube with proper title/description
- [ ] Add timestamp markers in YouTube description

Good luck with your demo! 🎮
