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

