import tkinter as tk
from tkinter import messagebox

# Constants
BOARD_SIZE = 8
TILE_SIZE = 60
PIECE_SYMBOLS = {
    'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N', 'P': 'P',
    'k': 'K', 'q': 'q', 'r': 'r', 'b': 'b', 'n': 'n', 'p': 'p'
}

# Initialize the main window
root = tk.Tk()
root.title("Chess Game")

# Canvas for drawing the board
canvas = tk.Canvas(root, width=BOARD_SIZE * TILE_SIZE, height=BOARD_SIZE * TILE_SIZE)
canvas.pack()

# Initialize the board with pieces
initial_board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

board = [row[:] for row in initial_board]  # Create a copy of the initial board
selected_piece = None
turn = 'white'

def draw_board():
    canvas.delete("all")
    colors = ['#f0d9b5', '#b58863']
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = colors[(row + col) % 2]
            x0 = col * TILE_SIZE
            y0 = row * TILE_SIZE
            x1 = x0 + TILE_SIZE
            y1 = y0 + TILE_SIZE
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="tile")

            piece = board[row][col]
            if piece != '.':
                canvas.create_text(
                    col * TILE_SIZE + TILE_SIZE // 2,
                    row * TILE_SIZE + TILE_SIZE // 2,
                    text=PIECE_SYMBOLS[piece],
                    font=("Helvetica", TILE_SIZE // 2),
                    tags="piece"
                )

def on_tile_click(event):
    global selected_piece, turn
    col = event.x // TILE_SIZE
    row = event.y // TILE_SIZE

    if selected_piece:
        old_row, old_col, piece = selected_piece
        if (turn == 'white' and piece.isupper()) or (turn == 'black' and piece.islower()):
            if is_valid_move(piece, old_row, old_col, row, col):
                board[row][col] = piece
                board[old_row][old_col] = '.'
                turn = 'black' if turn == 'white' else 'white'
        selected_piece = None
    else:
        piece = board[row][col]
        if (turn == 'white' and piece.isupper()) or (turn == 'black' and piece.islower()):
            selected_piece = (row, col, piece)

    draw_board()

def is_valid_move(piece, start_row, start_col, end_row, end_col):
    if board[end_row][end_col] == '.' or board[end_row][end_col].islower() != piece.islower():
        if piece.lower() == 'p':  # Pawn
            direction = -1 if piece.isupper() else 1
            start_row_check = 6 if piece.isupper() else 1
            if start_col == end_col:
                if end_row == start_row + direction and board[end_row][end_col] == '.':
                    return True
                if start_row == start_row_check and end_row == start_row + 2 * direction:
                    return board[start_row + direction][start_col] == '.'
            elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
                return board[end_row][end_col] != '.' and board[end_row][end_col].islower() != piece.islower()
        elif piece.lower() == 'r':  # Rook
            if start_row == end_row or start_col == end_col:
                return clear_path(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'n':  # Knight
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
                return True
        elif piece.lower() == 'b':  # Bishop
            if abs(start_row - end_row) == abs(start_col - end_col):
                return clear_path(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'q':  # Queen
            if abs(start_row - end_row) == abs(start_col - end_col) or start_row == end_row or start_col == end_col:
                return clear_path(start_row, start_col, end_row, end_col)
        elif piece.lower() == 'k':  # King
            if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
                return True
    return False

def clear_path(start_row, start_col, end_row, end_col):
    step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
    step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
    current_row, current_col = start_row + step_row, start_col + step_col

    while (current_row != end_row or current_col != end_col):
        if board[current_row][current_col] != '.':
            return False
        current_row += step_row
        current_col += step_col
    return True

# Initial draw of the board
draw_board()

# Bind click event to the canvas
canvas.bind("<Button-1>", on_tile_click)

root.mainloop()
