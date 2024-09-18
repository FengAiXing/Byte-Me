import sys
import tkinter as tk
import os

from django.db.models.fields import return_None

# Test data
moves = [
    ((5, 0), (4, 1), 1, 0),
    ((2, 1), (3, 0), 1, 1),
    ((5, 2), (4, 3), 2, 1),
    ((2, 3), (3, 2), 2, 2),
]

# Create the checkerboard with initial pieces
def create_initial_board():
    board = [["" for _ in range(8)] for _ in range(8)]
    # Place red pieces
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = "R"  # Red pieces
    # Place green pieces
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = "G"  # Green pieces
    return board

# Update the board according to the current move
def apply_move(board, move):
    start, end, _, _ = move
    piece = board[start[0]][start[1]]
    board[start[0]][start[1]] = ""
    board[end[0]][end[1]] = piece

# Draw the board
def draw_board(canvas, board):
    canvas.delete("all")
    size = 100
    for row in range(8):
        for col in range(8):
            x1 = col * size
            y1 = row * size
            x2 = x1 + size
            y2 = y1 + size
            color = "white" if (row + col) % 2 == 0 else "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            # Draw pieces
            if board[row][col] == "R":  # Red piece
                canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="red")
            elif board[row][col] == "G":  # Green piece
                canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="green")

# Handle the next move
def next_move(board, move_index, move_label, canvas, red_score_label, green_score_label):
    if move_index.get() < len(moves):
        move_index.set(move_index.get() + 1)
        if move_index.get() > 0:
            apply_move(board, moves[move_index.get() - 1])  # Apply the move for step N
            _, _, red_score, green_score = moves[move_index.get() - 1]  # Extract the scores
            # Update score labels
            red_score_label.config(text=f"Red Player: {red_score}")
            green_score_label.config(text=f"Green Player: {green_score}")
        draw_board(canvas, board)
        move_label.config(text=f"Move {move_index.get()} of {len(moves)}")

# Handle the previous move
def previous_move(board, move_index, move_label, canvas, red_score_label, green_score_label):
    if move_index.get() > 0:
        move_index.set(move_index.get() - 1)
        # Reset board to initial state
        board[:] = create_initial_board()
        for i in range(move_index.get()):
            apply_move(board, moves[i])
        # Update score labels based on the current move
        if move_index.get() > 0:
            _, _, red_score, green_score = moves[move_index.get() - 1]
            red_score_label.config(text=f"Red Player: {red_score}")
            green_score_label.config(text=f"Green Player: {green_score}")
        else:
            red_score_label.config(text="Red Player: 0")
            green_score_label.config(text="Green Player: 0")
        draw_board(canvas, board)
        move_label.config(text=f"Move {move_index.get()} of {len(moves)}")

# Exit to game history
def exit_to_history(game_id, game_window):
    game_window.destroy()
    os.system(f'python Game_history.py {game_id}')

# Create the Game Detail window
def create_game_detail_window(game_id):
    game_window = tk.Tk()
    game_window.title(f"Game {game_id} - Details")

    # Center the window on the screen
    window_width = 1100
    window_height = 920
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()
    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))
    game_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create the initial checkerboard
    board = create_initial_board()

    main_frame = tk.Frame(game_window)
    main_frame.pack(pady=10)
    canvas = tk.Canvas(main_frame, width=800, height=800)
    canvas.grid(row=0, column=0, padx=20)
    draw_board(canvas, board)

    # Create score display
    score_frame = tk.Frame(main_frame)
    score_frame.grid(row=1, column=0, pady=10)
    red_score_label = tk.Label(score_frame, text="Red Player: 0", font=("Helvetica", 14), fg="red")
    green_score_label = tk.Label(score_frame, text="Green Player: 0", font=("Helvetica", 14), fg="green")
    red_score_label.grid(row=0, column=0, padx=40)
    green_score_label.grid(row=0, column=1, padx=40)

    # Create move label
    move_index = tk.IntVar(value=0)
    move_label = tk.Label(game_window, text=f"Move 0 of {len(moves)}", font=("Helvetica", 14))
    move_label.pack(pady=10)

    # Create buttons for next, previous, and exit
    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=0, column=1, sticky="n", padx=10)

    button_width = 15  # Uniform width for buttons

    prev_button = tk.Button(button_frame, text="Previous Move", font=("Helvetica", 12), width=button_width,
                            command=lambda: previous_move(board, move_index, move_label, canvas, red_score_label, green_score_label))
    prev_button.pack(pady=40)

    next_button = tk.Button(button_frame, text="Next Move", font=("Helvetica", 12), width=button_width,
                            command=lambda: next_move(board, move_index, move_label, canvas, red_score_label, green_score_label))
    next_button.pack(pady=40)

    exit_button = tk.Button(game_window, text="Exit", font=("Helvetica", 12), bg="#FF5733", fg="white", width=button_width,
                            command=lambda: exit_to_history(game_id, game_window))
    exit_button.place(x=1000, y=870, anchor="se")

    game_window.mainloop()

# Main function to run the game detail viewer
if __name__ == "__main__":
    if len(sys.argv) < 2:
        pass
    else:
        game_id = sys.argv[1]
        create_game_detail_window(game_id)
