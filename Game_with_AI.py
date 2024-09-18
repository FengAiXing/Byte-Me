import sys
import tkinter as tk
import os

class CheckerGame:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Store the username
        self.root.title("Cyber Checkers")

        # Set window size and position
        self.window_width = 1100
        self.window_height = 920
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = int((screen_width - self.window_width) / 2)
        y_position = int((screen_height - self.window_height) / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")

        # Create main frame with grid layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # Create board frame (grid layout)
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=0, column=0, padx=10)

        self.rows = 8
        self.cols = 8
        self.square_size = 100
        self.board = []
        self.pieces = {}
        self.red_score = 0
        self.green_score = 0
        self.move_log = []  # Log for movements

        self.create_board()
        self.initialize_pieces()

        # Create score frame (below the board)
        self.score_frame = tk.Frame(self.main_frame, bg="#F0F0F0")
        self.score_frame.grid(row=1, column=0, pady=20)

        # Add score labels (pack them horizontally in the score_frame)
        self.red_score_label = tk.Label(self.score_frame, text=f"AI score: {self.red_score}", font=("Helvetica", 16),
                                        bg="#F0F0F0", fg="red", anchor="w", width=20)
        self.red_score_label.grid(row=0, column=0)

        self.green_score_label = tk.Label(self.score_frame, text=f"Your score: {self.green_score}",
                                          font=("Helvetica", 16), bg="#F0F0F0", fg="green", anchor="w", width=20)
        self.green_score_label.grid(row=0, column=1)

        # Create move log frame (right side of the board)
        self.move_log_frame = tk.Frame(self.main_frame, bg="#F0F0F0")
        self.move_log_frame.grid(row=0, column=1, padx=20)

        # Create a label for the movement logs
        self.move_log_label = tk.Label(self.move_log_frame, text="Move Log", font=("Helvetica", 16), bg="#F0F0F0")
        self.move_log_label.pack()

        # Create a text widget to display move logs
        self.move_log_text = tk.Text(self.move_log_frame, height=30, width=30, state=tk.DISABLED)
        self.move_log_text.pack()

        # Add exit button (right bottom)
        self.exit_button = tk.Button(self.main_frame, text="Exit Game", font=("Helvetica", 14),
                                     command=self.exit_to_main_menu, bg="#FF5733", fg="white")
        self.exit_button.grid(row=1, column=1, pady=20)

    def create_board(self):
        """Creating chessboard"""
        colors = ["white", "black"]  # Set the board color
        for row in range(self.rows):
            row_list = []
            for col in range(self.cols):
                color = colors[(row + col) % 2]
                square = tk.Canvas(self.board_frame, width=self.square_size, height=self.square_size, bg=color)
                square.grid(row=row, column=col)
                row_list.append(square)
            self.board.append(row_list)

    def initialize_pieces(self):
        """Initialize chess pieces"""
        # Red pieces
        for row in range(3):
            for col in range(self.cols):
                if (row + col) % 2 != 0:  # Only on black grid
                    self.add_piece(row, col, "red")

        # Green pieces
        for row in range(5, 8):
            for col in range(self.cols):
                if (row + col) % 2 != 0:
                    self.add_piece(row, col, "green")

    def add_piece(self, row, col, color):
        """Add a chess piece at the specified position"""
        piece_radius = 40
        center_x = self.square_size // 2
        center_y = self.square_size // 2
        piece = self.board[row][col].create_oval(center_x - piece_radius, center_y - piece_radius,
                                                 center_x + piece_radius, center_y + piece_radius, fill=color)
        self.pieces[(row, col)] = piece

    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move the specified chess piece"""
        if (from_row, from_col) in self.pieces:
            piece = self.pieces.pop((from_row, from_col))
            self.board[from_row][from_col].delete(piece)  # remove old pieces
            self.add_piece(to_row, to_col, "red" if from_row < 3 else "green")
            self.pieces[(to_row, to_col)] = piece

            # Log the move in the move log
            self.log_move(from_row, from_col, to_row, to_col)

    def remove_piece(self, row, col):
        """Remove the specified chess piece"""
        if (row, col) in self.pieces:
            piece = self.pieces.pop((row, col))
            self.board[row][col].delete(piece)

    def update_board(self, move_from, move_to, captured=None):
        """Get chess piece movement information and update"""
        from_row, from_col = move_from
        to_row, to_col = move_to

        # Move
        self.move_piece(from_row, from_col, to_row, to_col)

        # Remove captured pieces
        if captured:
            capture_row, capture_col = captured
            self.remove_piece(capture_row, capture_col)
            self.update_score(captured)

    def update_score(self, captured_piece):
        """Update the score when a piece is captured"""
        capture_row, capture_col = captured_piece
        if capture_row < 3:
            self.green_score += 1  # Red get score
        else:
            self.red_score += 1  # Green get score

        # Update score labels
        self.red_score_label.config(text=f"Red Player: {self.red_score}")
        self.green_score_label.config(text=f"Green Player: {self.green_score}")

    def log_move(self, from_row, from_col, to_row, to_col):
        """Log a move in the move log text widget"""
        self.move_log_text.config(state=tk.NORMAL)
        move_text = f"Moved from ({from_row+1}, {from_col+1}) to ({to_row+1}, {to_col+1})\n"
        self.move_log_text.insert(tk.END, move_text)
        self.move_log_text.config(state=tk.DISABLED)

    def exit_to_main_menu(self):
        """Exit to the user's main game page"""
        self.root.destroy()  # Close the current window
        os.system(f'python Game_frame.py {self.username}')  # Pass the username back to the main game page


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    username = sys.argv[1] if len(sys.argv) > 1 else "Guest"  # Get username from command-line args
    game = CheckerGame(root, username)  # Pass username to the game
    root.mainloop()
