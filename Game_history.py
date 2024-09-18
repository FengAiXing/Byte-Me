import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import os

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'cyber_checker'
}

# Fetch game history
def get_user_game_history(user_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT g.game_id, u1.username AS player1, u2.username AS player2, 
                   w.username AS winner, g.start_time
            FROM Games g
            JOIN Users u1 ON g.player1_id = u1.user_id
            JOIN Users u2 ON g.player2_id = u2.user_id
            LEFT JOIN Users w ON g.winner_id = w.user_id
            WHERE g.player1_id = %s OR g.player2_id = %s
            ORDER BY g.start_time DESC
        """, (user_id, user_id))
        games = cursor.fetchall()
        return games
    except Error as e:
        print(f"Error fetching game history: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Handle click on the entire row or button to view details
def view_game_details(game_id):
    os.system(f'python Game_detail.py {game_id}')

# Make labels clickable
def make_label_clickable(label, game_id):
    label.bind("<Button-1>", lambda e: view_game_details(game_id))

# Display the game history
def create_game_history_window(username, user_id):
    games = get_user_game_history(user_id)

    history_window = tk.Tk()
    history_window.title(f"{username}'s Game History")

    # Set window size
    window_width = 700
    window_height = 600
    screen_width = history_window.winfo_screenwidth()
    screen_height = history_window.winfo_screenheight()

    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))

    history_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    history_window.config(bg="#F0F0F0")

    # Display game history in labels
    tk.Label(history_window, text="Game History", font=("Helvetica", 18, "bold"), bg="#F0F0F0").pack(pady=10)

    # Create a frame to hold the scrollable content, with border color
    frame = tk.Frame(history_window, highlightbackground="black", highlightthickness=2)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a scrollable area within the frame
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Check if there are games, otherwise display "No games found" message
    if games:
        # Display each game in the scrollable frame using a grid layout
        for i, game in enumerate(games):
            game_text = (f"Game {i + 1}: {game['player1']} vs {game['player2']} "
                         f"| Winner: {game['winner'] if game['winner'] else 'Draw'} "
                         f"| Start: {game['start_time']}")

            game_label = tk.Label(scrollable_frame, text=game_text, font=("Helvetica", 12), bg="#F0F0F0", wraplength=700)
            game_label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
            make_label_clickable(game_label, game['game_id'])
            detail_button = tk.Button(scrollable_frame, text="View Details", font=("Helvetica", 10),
                                      command=lambda game_id=game['game_id']: view_game_details(game['game_id']))
            detail_button.grid(row=i, column=1, padx=10, pady=10, sticky="e")
    else:
        # If no games found, display a message in the scrollable frame
        tk.Label(scrollable_frame, text="No game history.", font=("Helvetica", 14),
                 bg="#F0F0F0").grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

    # Close button
    def close_and_return():
        history_window.destroy()
        os.system(f'python user_information.py {username}')

    tk.Button(history_window, text="Close", font=("Helvetica", 12), bg="#FF5733", fg="white",
              command=close_and_return).pack(pady=10)

    history_window.mainloop()

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 3:
        pass
    else:
        username = sys.argv[1]
        user_id = sys.argv[2]
        create_game_history_window(username, user_id)
