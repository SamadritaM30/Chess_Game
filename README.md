# Chess Engine with Alpha-Beta Pruning AI

This project is a graphical chess engine built using **Pygame** and the **python-chess** library. The game allows a human player to play against an AI that uses the **alpha-beta pruning** algorithm along with a **heuristic evaluation function** for decision-making.

---

## 💡 Features

- Choose your color (White or Black) at the start of the game
- Graphical chess board using Pygame
- AI opponent using:
  - **Minimax with Alpha-Beta Pruning**
  - **Heuristic evaluation** based on material balance and optional positional factors
- Turn-based gameplay with legal move validation (shows illegal move when user(human) tries to play wrong moves)
- Game ends on checkmate, stalemate, or draw

---

## 🗂️ File Structure

```
.
├── chess_engine.py         # Main game logic and GUI
├── images/                 # Folder containing chess piece images
│   ├── bB.png              # Black Bishop
│   ├── bK.png              # Black King
│   └── ...                 # Other piece images
├── README.md               # You're reading it!
```

---

## 🔧 Installation & Setup

### Prerequisites

- Python 3.x
- `pygame` library
- `python-chess` library

### Installation

```bash
pip install pygame
pip install chess
```

---

## 🚀 Running the Game

```bash
python chess_engine.py
```

- At startup, choose to play as **White** or **Black**.
- Click on pieces and destination squares to make moves.
- The AI will respond using Alpha-Beta Pruning-based decision-making.

---

## ♟️ AI Algorithm Overview

### Alpha-Beta Pruning

The AI evaluates moves using the **Minimax algorithm with Alpha-Beta Pruning**. This reduces the number of nodes evaluated in the game tree, increasing performance without sacrificing optimality.

### Heuristic Evaluation Function

- **Material Balance**:
  - Pawn = 1
  - Knight = 3
  - Bishop = 3
  - Rook = 5
  - Queen = 9
  - King = ∞ (considered indirectly through checkmate detection)
- Optional: Piece positioning, king safety, pawn structure, etc.

---

## 🧩 Key Functions

### `get_best_move(board, depth, alpha, beta)`

- Returns the best move for the current board state using Minimax with Alpha-Beta pruning.
- Parameters:
  - `board`: A `chess.Board()` object
  - `depth`: Max depth to search
  - `alpha`, `beta`: Bounds for pruning
- Alternates between maximizing (AI) and minimizing (opponent) turns

---

## 📚 Useful Links

- [python-chess Documentation](https://python-chess.readthedocs.io/en/latest/)
- [UCI Protocol Guide](http://wbec-ridderkerk.nl/html/UCIProtocol.html)

---

## 📸Game UI
![image](https://github.com/user-attachments/assets/50bffce5-43b9-4fd3-969b-7ce01929bd7e)


## 🏁 Conclusion

This project combines game development with artificial intelligence, offering a solid foundation for further enhancements like deeper evaluations, better heuristics, or even neural network-based chess AI.

Feel free to experiment, optimize, and play!
