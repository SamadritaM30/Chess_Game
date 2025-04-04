import pygame
import chess
import random
import sys
import time

# Constants for the board dimensions and colors
WIDTH = HEIGHT = 640  # Board size in pixels (8x8 squares)
SQ_SIZE = WIDTH // 8
FPS = 15

# Colors for the squares
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)

# Global dictionary to store images
IMAGES = {}

def load_images():
    """
    Load chess piece images from the images folder.
    """
    pieces = {
        "P": "white-pawn.png",
        "N": "white-knight.png",
        "B": "white-bishop.png",
        "R": "white-rook.png",
        "Q": "white-queen.png",
        "K": "white-king.png",
        "p": "black-pawn.png",
        "n": "black-knight.png",
        "b": "black-bishop.png",
        "r": "black-rook.png",
        "q": "black-queen.png",
        "k": "black-king.png"
    }
    for symbol, filename in pieces.items():
        path = "images/" + filename
        try:
            image = pygame.image.load(path)
        except pygame.error as e:
            print(f"Unable to load image at path: {path}")
            raise e
        IMAGES[symbol] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

def draw_board(screen, flip_board, selected_sq):
    """
    Draw the chess board with optional highlight for the selected square.
    """
    for rank in range(8):
        for file in range(8):
            draw_file = file if not flip_board else 7 - file
            draw_rank = rank if not flip_board else 7 - rank
            x = draw_file * SQ_SIZE
            y = (7 - draw_rank) * SQ_SIZE
            color = LIGHT_COLOR if (file + rank) % 2 == 0 else DARK_COLOR
            rect = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)
            if selected_sq is not None:
                sel_file = chess.square_file(selected_sq)
                sel_rank = chess.square_rank(selected_sq)
                if flip_board:
                    sel_file = 7 - sel_file
                    sel_rank = 7 - sel_rank
                if sel_file == file and sel_rank == rank:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 4)

def draw_pieces(screen, board, flip_board):
    """
    Draw all pieces on the board based on the current board state.
    """
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            if flip_board:
                file = 7 - file
                rank = 7 - rank
            x = file * SQ_SIZE
            y = (7 - rank) * SQ_SIZE
            symbol = piece.symbol()
            screen.blit(IMAGES[symbol], pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))

def get_square_from_mouse(pos, flip_board):
    """
    Convert the mouse position (x, y) to a chess square index.
    """
    x, y = pos
    file = x // SQ_SIZE
    rank = 7 - (y // SQ_SIZE)
    if flip_board:
        file = 7 - file
        rank = 7 - rank
    return chess.square(file, rank)

# Heuristic evaluation function.
def evaluate_board(board, ai_color):
    """
    Evaluate the board state from the perspective of the AI.
    Uses simple material balance.
    """
    # Piece values: Pawn, Knight, Bishop, Rook, Queen, King.
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
        'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0
    }
    value = 0
    for square, piece in board.piece_map().items():
        symbol = piece.symbol()
        # If the piece belongs to AI, add its value; otherwise, subtract.
        if piece.color == ai_color:
            value += piece_values[symbol]
        else:
            value -= piece_values[symbol]
    return value

# Alpha-beta pruning algorithm.
def alpha_beta(board, depth, alpha, beta, ai_color):
    """
    Recursively search the game tree using alpha-beta pruning.
    Returns the evaluation of the board from the AI's perspective.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, ai_color)
    
    if board.turn == ai_color:  # Maximizing for AI
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, ai_color)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:  # Minimizing for opponent
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, ai_color)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth, ai_color):
    """
    Determines the best move for the AI using the alpha-beta pruning algorithm.
    """
    best_move = None
    # Determine if we are maximizing or minimizing at the root.
    is_maximizing = (board.turn == ai_color)
    best_value = -float('inf') if is_maximizing else float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = alpha_beta(board, depth - 1, -float('inf'), float('inf'), ai_color)
        board.pop()
        if is_maximizing and board_value > best_value:
            best_value = board_value
            best_move = move
        elif not is_maximizing and board_value < best_value:
            best_value = board_value
            best_move = move

    # In case no move was selected (should not happen), fallback to random.
    if best_move is None:
        best_move = random.choice(list(board.legal_moves))
    return best_move

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game: Human vs. AI")
    clock = pygame.time.Clock()
    load_images()

    board = chess.Board()

    # Ask the player to choose a color.
    player_color = input("Choose your color (white/black): ").strip().lower()
    if player_color not in ['white', 'black']:
        print("Invalid choice. Defaulting to white.")
        player_color = 'white'
    human_is_white = (player_color == 'white')
    # Determine the AI's color.
    ai_color = chess.BLACK if human_is_white else chess.WHITE
    # Flip the board so that the human's pieces appear at the bottom.
    flip_board = not human_is_white

    selected_sq = None  # Currently selected square for a move

    running = True
    # Set the search depth for the AI.
    SEARCH_DEPTH = 3

    while running:
        # Determine whose turn it is.
        human_turn = (board.turn == chess.WHITE and human_is_white) or (board.turn == chess.BLACK and not human_is_white)

        if human_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    sq = get_square_from_mouse(pos, flip_board)
                    if selected_sq is None:
                        piece = board.piece_at(sq)
                        if piece and ((piece.color == chess.WHITE and human_is_white) or (piece.color == chess.BLACK and not human_is_white)):
                            selected_sq = sq
                    else:
                        move = chess.Move(selected_sq, sq)
                        if move in board.legal_moves:
                            board.push(move)
                        else:
                            print("Illegal move, try again.")
                        selected_sq = None
        else:
            # Process events during AI turn (to allow quitting).
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            time.sleep(0.5)  # Delay for realism.
            ai_move = get_best_move(board, SEARCH_DEPTH, ai_color)
            board.push(ai_move)
            print("AI played:", ai_move.uci())

        # Redraw board and pieces.
        draw_board(screen, flip_board, selected_sq)
        draw_pieces(screen, board, flip_board)
        pygame.display.flip()

        # Check if the game is over.
        if board.is_game_over():
            print("Game over. Result:", board.result())
            time.sleep(3)
            running = False

        clock.tick(FPS)

if __name__ == "__main__":
    main()
