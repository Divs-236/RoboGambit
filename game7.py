"""
RoboGambit 2025-26 — Task 1: Autonomous Game Engine
Organised by Aries and Robotics Club, IIT Delhi

Board: 6x6 NumPy array
  - 0  : Empty cell
  - 1  : White Pawn
  - 2  : White Knight
  - 3  : White Bishop
  - 4  : White Queen
  - 5  : White King
  - 6  : Black Pawn
  - 7  : Black Knight
  - 8  : Black Bishop
  - 9  : Black Queen
  - 10 : Black King

Board coordinates:
  - Bottom-left  = A1  (index [0][0])
  - Columns   = A–F (left to right)
  - Rows      = 6-1 (top to bottom)(from white's perspective)

Move output format:  "<piece_id>:<source_cell>-><target_cell>"
  e.g.  "1:B3->B4"   (White Pawn moves from B3 to B4)
"""

import numpy as np
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

import time

# --- Time Management Globals ---
remaining_time = 60 #Change to 900 for submission
start_time_of_search = 0
time_limit_for_move = 0


EMPTY = 0

# Piece IDs
WHITE_PAWN   = 1
WHITE_KNIGHT = 2
WHITE_BISHOP = 3
WHITE_QUEEN  = 4
WHITE_KING   = 5
BLACK_PAWN   = 6
BLACK_KNIGHT = 7
BLACK_BISHOP = 8
BLACK_QUEEN  = 9
BLACK_KING   = 10

WHITE_PIECES = {WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING}
BLACK_PIECES = {BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING}

BOARD_SIZE = 6


PIECE_VALUES = {
    WHITE_PAWN:   100,
    WHITE_KNIGHT: 300,
    WHITE_BISHOP: 320,
    WHITE_QUEEN:  900,
    WHITE_KING:  20000,
    BLACK_PAWN:  -100,
    BLACK_KNIGHT:-300,
    BLACK_BISHOP:-320,
    BLACK_QUEEN: -900,
    BLACK_KING: -20000,
}
# Column index → letter
COL_TO_FILE = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}
FILE_TO_COL = {v: k for k, v in COL_TO_FILE.items()}


PIECE_LIMITS = {
    WHITE_PAWN: 6,
    WHITE_KNIGHT: 2,
    WHITE_BISHOP: 2,
    WHITE_QUEEN: 1,
    WHITE_KING: 1,
    BLACK_PAWN: 6,
    BLACK_KNIGHT: 2,
    BLACK_BISHOP: 2,
    BLACK_QUEEN: 1,
    BLACK_KING: 1
}

# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------
    
def idx_to_cell(row: int, col: int) -> str:
    """Convert (row, col) zero-indexed to board notation e.g. (0,0) -> 'A1'."""
    return f"{COL_TO_FILE[col]}{row + 1}"
       
def cell_to_idx(cell: str):
    """Convert board notation e.g. 'A1' -> (row=0, col=0)."""
    col = FILE_TO_COL[cell[0].upper()]
    row = int(cell[1]) - 1
    return row, col
    
def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    
def is_white(piece: int) -> bool:
    return piece in WHITE_PIECES
    
def is_black(piece: int) -> bool:
    return piece in BLACK_PIECES
    
def same_side(p1: int, p2: int) -> bool:
    return (is_white(p1) and is_white(p2)) or (is_black(p1) and is_black(p2))

# ---------------------------------------------------------------------------
# Move generation
# ---------------------------------------------------------------------------

def get_pawn_moves(board: np.ndarray, row: int, col: int, piece: int): 
    
    moves = []
    """
    White Pawns move downward (increasing row index).
    Black Pawns move upward  (decreasing row index).
    Captures are diagonal-forward.

    """
def get_pawn_moves(board: np.ndarray, row: int, col: int, piece: int, offboard: dict): 
    moves = []
    # REMOVED: offboard = get_offboard_pieces(board)  <-- This was the bottleneck

    if is_white(piece):
        promo_pieces = [WHITE_QUEEN, WHITE_BISHOP, WHITE_KNIGHT]

        if in_bounds(row+1, col) and board[row+1][col] == EMPTY:
            if row+1 == 5:
                for new_piece in promo_pieces:
                    if offboard[new_piece] > 0:
                        moves.append((piece, row, col, row+1, col,new_piece))
            else:
                moves.append((piece, row, col, row+1, col, None))

        for dc in [-1, 1]:
            if in_bounds(row+1, col+dc) and is_black(board[row+1][col+dc]):
                if row+1 == 5:
                    for new_piece in promo_pieces:
                        if offboard[new_piece] > 0:
                            moves.append((piece, row, col, row+1, col+dc,new_piece))
                else:
                    moves.append((piece, row, col, row+1, col+dc, None))

    else:
        promo_pieces = [BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT]

        if in_bounds(row-1, col) and board[row-1][col] == EMPTY:
            if row-1 == 0:
                for new_piece in promo_pieces:
                    if offboard[new_piece] > 0:
                        moves.append((piece, row, col, row-1, col, new_piece))
            else:
                moves.append((piece, row, col, row-1, col, None))
        for dc in [-1, 1]:
            if in_bounds(row-1, col+dc) and is_white(board[row-1][col+dc]):
                if row-1 == 0:
                    for new_piece in promo_pieces:
                        if offboard[new_piece] > 0:
                            moves.append((piece, row, col, row-1, col+dc, new_piece))
                else:
                    moves.append((piece, row, col, row-1, col+dc,None))

    return moves

    
def get_knight_moves(board: np.ndarray, row: int, col: int, piece: int, offboard):
    moves = []
    
    knight_jumps = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    
    for (r,c) in knight_jumps:
        new_row, new_col = row + r, col + c
        if not in_bounds(new_row, new_col):
            continue
        target = board[new_row][new_col]
        
        if target == EMPTY or (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target)):
            moves.append((piece,row,col,new_row,new_col,None))
    
    return moves
    
def get_sliding_moves(board: np.ndarray, row: int, col: int, piece: int, directions, offboard):
    """Generic sliding piece (bishop / queen / rook directions)."""
    moves = []
    for (dr,dc) in directions:
        r, c = row + dr, col + dc
        while in_bounds(r, c):
            target = board[r][c]
            if target == EMPTY:
                moves.append((piece,row,col,r,c,None))
            elif (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target)):
                moves.append((piece,row,col,r,c,None))
                break 
            else:
                break
            r += dr
            c += dc
    
    return moves

def get_bishop_moves(board: np.ndarray, row: int, col: int, piece: int, offboard):
    diagonals = [(-1,-1),(-1,1),(1,-1),(1,1)]
    return get_sliding_moves(board, row, col, piece, diagonals,offboard)


def get_queen_moves(board: np.ndarray, row: int, col: int, piece: int, offboard):
    all_dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    return get_sliding_moves(board, row, col, piece, all_dirs,offboard)
    
    
def get_king_moves(board: np.ndarray, row: int, col: int, piece: int, offboard):
    moves = []
    k = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    for (dr,dc) in k:
        r,c = row+dr,col+dc
        if in_bounds(r,c):
            target = board[r][c]
            if (target == EMPTY) or ((is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target))):
                moves.append((piece,row,col,r,c,None))
                
    return moves
    
    
MOVE_GENERATORS = {
    WHITE_PAWN:   get_pawn_moves,
    WHITE_KNIGHT: get_knight_moves,
    WHITE_BISHOP: get_bishop_moves,
    WHITE_QUEEN:  get_queen_moves,
    WHITE_KING:   get_king_moves,
    BLACK_PAWN:   get_pawn_moves,
    BLACK_KNIGHT: get_knight_moves,
    BLACK_BISHOP: get_bishop_moves,
    BLACK_QUEEN:  get_queen_moves,
    BLACK_KING:   get_king_moves,
}
def king_under_attack(bd, kr, kc, is_king_white):
    """Checks if the square (kr, kc) is being attacked by the opponent."""
    enemy_pawn = BLACK_PAWN if is_king_white else WHITE_PAWN
    enemy_knight = BLACK_KNIGHT if is_king_white else WHITE_KNIGHT
    enemy_bishop = BLACK_BISHOP if is_king_white else WHITE_BISHOP
    enemy_queen = BLACK_QUEEN if is_king_white else WHITE_QUEEN
    enemy_king = BLACK_KING if is_king_white else WHITE_KING

    pawn_dir = 1 if is_king_white else -1
    for dc in [-1, 1]:
        pr, pc = kr + pawn_dir, kc + dc
        if 0 <= pr < 6 and 0 <= pc < 6:
            if bd[pr, pc] == enemy_pawn:
                return True

    knight_jumps = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
    for dr, dc in knight_jumps:
        tr, tc = kr + dr, kc + dc
        if 0 <= tr < 6 and 0 <= tc < 6:
            if bd[tr, tc] == enemy_knight:
                return True

    directions = {
        "diag": [(-1,-1), (-1,1), (1,-1), (1,1)],
        "ortho": [(-1,0), (1,0), (0,-1), (0,1)]
    }

    for dr, dc in directions["diag"]:
        for i in range(1, 6):
            tr, tc = kr + dr * i, kc + dc * i
            if not (0 <= tr < 6 and 0 <= tc < 6): break
            p = bd[tr, tc]
            if p != EMPTY:
                if p in {enemy_bishop, enemy_queen}: return True
                break

    for dr, dc in directions["ortho"]:
        for i in range(1, 6):
            tr, tc = kr + dr * i, kc + dc * i
            if not (0 <= tr < 6 and 0 <= tc < 6): break
            p = bd[tr, tc]
            if p != EMPTY:
                if p in {enemy_queen}: return True
                break

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            tr, tc = kr + dr, kc + dc
            if 0 <= tr < 6 and 0 <= tc < 6:
                if bd[tr, tc] == enemy_king:
                    return True

    return False
def get_all_moves(board: np.ndarray, playing_white: bool, offboard):

    moves = []
    king_piece = WHITE_KING if playing_white else BLACK_KING
    king_row, king_col = None, None

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == king_piece:
                king_row, king_col = r, c
                break
        if king_row is not None:
            break

    in_check = king_under_attack(board, king_row, king_col, playing_white)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = board[i][j]
            if piece == EMPTY:
                continue
            if playing_white and is_black(piece):
                continue
            if not playing_white and is_white(piece):
                continue

            piece_moves = MOVE_GENERATORS[piece](board, i, j, piece,offboard)

            for move_candidate in piece_moves:  
                if len(move_candidate) == 5:
                    move = (*move_candidate, None)
                else:
                    move = move_candidate

                p, r1, c1, r2, c2, promo = move  
                if board[r2][c2] in {WHITE_KING, BLACK_KING}:
                    continue
                captured = board[r2][c2]
                board[r1][c1] = EMPTY
                board[r2][c2] = promo if promo is not None else p
                
                kr, kc = (r2, c2) if p == king_piece else (king_row, king_col)
                king_safe = not king_under_attack(board, kr, kc, playing_white)
                board[r1][c1] = p
                board[r2][c2] = captured
                if in_check and not king_safe:
                    continue
                if not in_check and not king_safe:
                    continue

                moves.append(move)

    return moves
    
# ---------------------------------------------------------------------------
# Board evaluation heuristic  (TODO: tune weights / add positional tables)
# ---------------------------------------------------------------------------
PST1 = np.array([
        [ 0,  0,  0,  0,  0,  0],
        [10, 10, 10, 10, 10, 10],
        [15, 25, 35, 35, 25, 15],
        [25, 35, 45, 45, 35, 25],
        [50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0]])
PST6=np.flipud(PST1)

PST2 = np.array([[-50, -40, -30, -30, -40, -50,],
        [-35,   0,  10,  10,   0, -35,],
        [-20,  15,  25,  25,  15, -20,],
        [-20,  15,  25,  25,  15, -20,],
        [-25,  15,  20,  20,  15, -25,],
        [-50, -40, -30, -30, -40, -50]])
PST7=np.flipud(PST2)
PST3 = np.array([[-20, -10, -10, -10, -10, -20,],
        [-10,  10,   5,   5,  10, -10,],
        [-10,  15,  20,  20,  15, -10,],
        [-10,  15,  20,  20,  15, -10,],
        [-10,  10,  10,  10,  10, -10,],
        [-20, -10, -10, -10, -10, -20]])
PST8=np.flipud(PST3)
PST4=np.array([
    [-20, -10, -5, -5, -10, -20],
    [-10,   0,  5,  5,   0, -10],
    [ -5,   5, 10, 10,   5,  -5],
    [ -5,   5, 10, 10,   5,  -5],
    [-10,   0,  5,  5,   0, -10],
    [-20, -10, -5, -5, -10, -20]])
PST9=np.flipud(PST4)
PST5=np.array([
    [ 20,  20,  10,  10,  20,  20], 
    [ 20,  10,   0,   0,  10,  20],
    [-10, -20, -20, -20, -20, -10], 
    [-20, -30, -30, -30, -30, -20], 
    [-30, -40, -40, -40, -40, -30], 
    [-30, -40, -40, -40, -40, -30]])
PST10=np.flipud(PST5)
PSTS = {
    WHITE_PAWN: PST1, BLACK_PAWN: PST6,
    WHITE_KNIGHT: PST2, BLACK_KNIGHT: PST7,
    WHITE_BISHOP: PST3, BLACK_BISHOP: PST8,
    WHITE_QUEEN: PST4, BLACK_QUEEN: PST9,
    WHITE_KING: PST5, BLACK_KING: PST10
}
def evaluate(board: np.ndarray) -> float:
    """
    Static board evaluation from White's perspective.
    Positive  → advantage for White
    Negative  → advantage for Black
    TODO: Add mobility, piece-square tables, king safety, etc.
    """
    score = 0.0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != EMPTY:
                score += PIECE_VALUES.get(piece, 0)+PSTS[piece][row][col]
    return score

 
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
    
def apply_move(board, piece, r1, c1, r2, c2, promo, offboard):
    captured = board[r2][c2]
    if captured != EMPTY and captured in offboard:
        offboard[captured] += 1
    if promo is not None and promo in offboard:
        offboard[promo] -= 1
    if promo is not None:
        board[r2][c2] = promo
    else:
        board[r2][c2] = piece
    board[r1][c1] = EMPTY
    return captured

def unapply_move(board, piece, r1, c1, r2, c2, promo, captured, offboard):
    if captured != EMPTY and captured in offboard:
        offboard[captured] -= 1
    if promo is not None and promo in offboard:
        offboard[promo] += 1

    board[r1][c1] = piece
    board[r2][c2] = captured

class TimeoutException(Exception):
    """Custom exception to break out of deep recursion."""
    pass

def check_time():
    """Checks if we have exceeded the time allocated for this move."""
    if time.perf_counter() - start_time_of_search > time_limit_for_move:
        raise TimeoutException()

# ---------------------------------------------------------------------------
# Format move string
# ---------------------------------------------------------------------------
       
def format_move(piece, r1, c1, r2, c2, promo):
    src = idx_to_cell(r1,c1)
    dst = idx_to_cell(r2,c2)
    if promo is not None:
        return f"{piece}:{src}->{dst}={promo}"
    else:
        return f"{piece}:{src}->{dst}"
# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def get_incremental_score(board, move, current_score):
    piece, r1, c1, r2, c2, promo = move
    piece_placed = promo if promo is not None else piece
    piece_at_src = board[r1][c1]
    captured = board[r2][c2]

    new_score = current_score

    new_score -= PIECE_VALUES[piece_at_src]
    new_score -= PSTS[piece_at_src][r1][c1]

    if captured != EMPTY:
        new_score -= PIECE_VALUES[captured]
        new_score -= PSTS[captured][r2][c2]

    new_score += PIECE_VALUES[piece_placed]
    new_score += PSTS[piece_placed][r2][c2]

    return new_score

def quiescence_search(board, alpha, beta, color, current_score, offboard):
    stand_pat = current_score * color
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    moves = get_all_moves(board, color == 1,offboard)
    capture_moves = [m for m in moves if board[m[3], m[4]] != EMPTY]
    capture_moves = score_moves(board, capture_moves)

    for move in capture_moves:
        new_score = get_incremental_score(board, move, current_score)
        captured=apply_move(board, *move,offboard)
        
        score = -quiescence_search(board, -beta, -alpha, -color, new_score, offboard)

        unapply_move(board, *move,captured,offboard)
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def score_moves(board: np.ndarray, moves: list) -> list:
    scored_moves = []
    for move in moves:
        piece, src_r, src_c, dst_r, dst_c, promo = move
        score = 0        
        target_piece = board[dst_r, dst_c]
        if target_piece != EMPTY:
            victim_val = abs(PIECE_VALUES.get(target_piece, 0))
            aggressor_val = abs(PIECE_VALUES.get(piece, 0))
            score = (10 * victim_val) - aggressor_val 
        if promo is not None:
            score = 9000
        scored_moves.append((score, move))
    scored_moves.sort(key=lambda x: x[0], reverse=True) 
    return [m[1] for m in scored_moves]

def Search(board, depth, alpha, beta, color,current_score, offboard):
    if depth>3:
        check_time()
    if depth==0:
        return quiescence_search(board, alpha, beta, color, current_score, offboard)
    moves=score_moves(board,get_all_moves(board,color==1,offboard))
    if not moves:
        king_piece = WHITE_KING if color == 1 else BLACK_KING
        kr, kc = None, None

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == king_piece:
                    kr, kc = r, c
                    break
            if kr is not None:
                break

        if king_under_attack(board, kr, kc, color == 1):
            return -100000 + depth
        return 0

    for move in moves:
        new_score = get_incremental_score(board, move, current_score)
        captured=apply_move(board,*move,offboard)
        evaluation=-Search(board,depth-1,-beta,-alpha,-color,new_score,offboard)
        unapply_move(board,*move,captured,offboard)
        if evaluation>=beta:
            return beta
        alpha=max(alpha,evaluation)
    return alpha

def get_offboard_pieces(board):
    counts = PIECE_LIMITS.copy()

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r][c]
            if piece in counts:
                counts[piece] -= 1

    return counts

def count_pieces(board):
    count = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                count += 1
    return count

def get_best_move(board: np.ndarray, playing_white: bool = True
                  ) -> Optional[str]:
    """
    Given the current board state, return the best move string.

    Parameters
    ----------
    board        : 6×6 NumPy array representing the current game state.
    playing_white: True if the engine is playing as White, False for Black.
    
    
    Returns
    -------
    Move string in the format '<piece_id>:<src_cell>-><dst_cell>', or
    None if no legal moves are available.
    """
    global remaining_time, start_time_of_search, time_limit_for_move
    
    start_time_of_search = time.perf_counter()
    time_limit_for_move = remaining_time / 20
    offboard_tracker = get_offboard_pieces(board)
    root_score = evaluate(board)
    best_move = None
    current_color = 1 if playing_white else -1
    all_moves = score_moves(board, get_all_moves(board, playing_white,offboard_tracker))
    
    if not all_moves:
        return None

    try:

        for depth in range(1, 10):
            current_best_at_depth = None
            max_eval = -float('inf')
            alpha = -float('inf')
            beta = float('inf')

            for move in all_moves:
                new_score = get_incremental_score(board, move, root_score)
                captured=apply_move(board, *move,offboard_tracker)
                
                score = -Search(board, depth - 1, -beta, -alpha, -current_color, new_score,offboard_tracker)
                unapply_move(board, *move,captured,offboard_tracker)
                if score > max_eval:
                    max_eval = score
                    current_best_at_depth = move
                
                alpha = max(alpha, score)
            
            if current_best_at_depth:
                best_move = current_best_at_depth
    except TimeoutException:
        pass
    elapsed = time.perf_counter() - start_time_of_search
    remaining_time -= elapsed
    return format_move(*best_move) if best_move else None
    
    
# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------
def play_vs_ai():
    # 1. Setup the initial board
    current_board = np.array([
        [ 2,  3,  4,  5,  3,  2], # A1-F1 (White)
        [ 1,  1,  1,  1,  1,  1], 
        [ 0,  0,  0,  0,  0,  0], 
        [ 0,  0,  0,  0,  0,  0], 
        [ 6,  6,  6,  6,  6,  6], 
        [ 7,  8,  9, 10,  8,  7], # A6-F6 (Black)
    ], dtype=int)

    is_ai_white = not True  # Set this to False if you want to play as White
    turn_white = True

    while True:
        print("\n" + "="*20)
        print(f"Current Board (Turn: {'White' if turn_white else 'Black'}):")
        print(current_board[::-1]) # Print flipped so A1 is at the bottom visually
        
        # Check for Game Over
        gameoffboard=get_offboard_pieces(current_board)
        legal_moves = get_all_moves(current_board, turn_white,gameoffboard)
        if not legal_moves:
            print("GAME OVER!")
            break

        if turn_white == is_ai_white:
            # --- AI TURN ---
            print("AI is thinking...")
            move_str = get_best_move(current_board, turn_white)
            print(f"AI plays: {move_str}")
            
            # Parse the string back into data (e.g., "1:A2->A3")
            # For simplicity, let's grab the best_move tuple directly if possible
            # or just use the format your AI generates.
            # Assuming you parse the string:
            parts = move_str.split(':')
            piece_id = int(parts[0])
            move_part = parts[1]
            if '=' in move_part:
                move_cells, promo = move_part.split('=')
                promo = int(promo)
            else:
                move_cells = move_part
                promo = None
            src_cell, dst_cell = move_cells.split('->')
            
            r1, c1 = cell_to_idx(src_cell)
            r2, c2 = cell_to_idx(dst_cell)
            
            apply_move(current_board, piece_id, r1, c1, r2, c2, promo,gameoffboard)
        
        else:
            # --- HUMAN TURN ---
            print("Your turn! Enter move (e.g., 'A5->A4'):")
            try:
                user_input = input("> ").upper().strip()
                src_cell, dst_cell = user_input.split('->')
                r1, c1 = cell_to_idx(src_cell)
                r2, c2 = cell_to_idx(dst_cell)
                piece_id = current_board[r1, c1]
                
                # Check if this move is in the legal list
                valid = False
                for m in legal_moves:
                    if (m[1], m[2], m[3], m[4]) == (r1, c1, r2, c2):
                        valid = True
                        break
                
                if valid:
                    apply_move(current_board, piece_id, r1, c1, r2, c2, None, gameoffboard)
                else:
                    print("Illegal move! Try again.")
                    continue
            except Exception as e:
                print(f"Invalid format! Error: {e}")
                continue

        # Switch turns
        turn_white = not turn_white
if __name__ == "__main__":
    # Example: standard-ish starting position on a 6x6 board
    # White pieces on rows 4-5, Black pieces on rows 0-1
    initial_board = np.array([
        [ 2,  3,  4,  5,  3,  2],   # Row 1 (A1–F1) — White back rank
        [ 1,  1,  1,  1,  1,  1],   # Row 2         — White pawns
        [ 0,  0,  0,  0,  0,  0],   # Row 3
        [ 0,  0,  0,  0,  0,  0],   # Row 4
        [ 6,  6,  6,  6,  6,  6],   # Row 5         — Black pawns
        [ 7,  8,  9, 10,  8,  7],   # Row 6 (A6–F6) — Black back rank
    ], dtype=int)
    
    print("Board:\n", initial_board)
    move = get_best_move(initial_board, playing_white=True)
    print("Best move for White:", move)
    play_vs_ai()

