import os
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import sys

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'cyber_checker'
}

# Fetch user info from the database
def get_user_info(username):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"Error fetching user info: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create and display the user info window
def create_user_info_window(username):
    user_info = get_user_info(username)

    if not user_info:
        messagebox.showerror("Error", "User information not found!")
        return
    info_window = tk.Tk()
    info_window.title(f"{username}'s Information")

    # Set window size
    window_width = 600
    window_height = 605
    screen_width = info_window.winfo_screenwidth()
    screen_height = info_window.winfo_screenheight()
    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))

    # Set window size and position
    info_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    info_window.config(bg="#F0F0F0")

    # Display user information
    tk.Label(info_window, text="User Information", font=("Helvetica", 18, "bold"), bg="#F0F0F0").pack(pady=10)
    tk.Label(info_window, text=f"Username: {user_info['username']}", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=5)
    tk.Label(info_window, text=f"Total Games: {user_info['total_games']}", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=5)
    tk.Label(info_window, text=f"Wins: {user_info['wins']}", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=5)
    tk.Label(info_window, text=f"Losses: {user_info['losses']}", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=5)
    tk.Label(info_window, text=f"Win Rate: {user_info['win_rate']}%", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=5)

    # View game history, it will open the Game_history.py file with username and user ID
    def open_game_history():
        info_window.destroy()  # Close current window
        # Always open Game_history.py even if there are no game records
        os.system(f'python Game_history.py {username} {user_info["user_id"]}')

    tk.Button(info_window, text="View Game History", font=("Helvetica", 12), bg="#2196F3", fg="white",
              command=open_game_history).pack(pady=10)

    # Add a close button that will return to Game_frame
    def close_and_return():
        info_window.destroy()
        os.system(f'python Game_frame.py {username}')

    close_button = tk.Button(info_window, text="Close", font=("Helvetica", 12), bg="#FF5733", fg="white",
                             command=close_and_return)
    close_button.pack(pady=20)

    info_window.mainloop()

# Main program
if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]  # Get the username
    else:
        username = "Guest"
    create_user_info_window(username)
