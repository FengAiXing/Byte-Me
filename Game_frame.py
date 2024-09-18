import itertools
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'cyber_checker'
}

# Establish database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to the database: {e}")
        return None

# Get user information
def get_user_info(username):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            return user
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to retrieve user info: {e}")
        finally:
            cursor.close()
            connection.close()

# Get the username from command line arguments
username = sys.argv[1] if len(sys.argv) > 1 else "Guest"

# Create the main frame
game_window = tk.Tk()
game_window.title(f"Cyber Checkers - {username}")
window_width = 600
window_height = 605

# Get the width and height of the screen
screen_width = game_window.winfo_screenwidth()
screen_height = game_window.winfo_screenheight()
x_position = int((screen_width / 2) - (window_width / 2))
y_position = int((screen_height / 2) - (window_height / 2))

# Set the size and initial position of the frame
game_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
game_window.config(bg="#F0F0F0")
game_window.resizable(False, False)

# Set background image
bg_image = Image.open("IMG/icon/chess_board.jpg")
bg_image = bg_image.resize((600, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(game_window, width=600, height=600, bd=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Set dynamic title
titles = itertools.cycle(["Welcome to Cyber Checkers", "Let's Play Chess", "Challenge the AI", "Compete with Players"])
title_text = canvas.create_text(300, 50, text="Welcome to Chess", font=("Comic Sans MS", 30, "bold"), fill="yellow")

# Update frequency for title change
def update_title():
    new_title = next(titles)
    canvas.itemconfig(title_text, text=new_title)
    game_window.after(2000, update_title)

update_title()

# Button Icon
ai_icon = ImageTk.PhotoImage(Image.open("IMG/icon/robot.png").resize((30, 30)))
player_icon = ImageTk.PhotoImage(Image.open("IMG/icon/human.png").resize((30, 30)))

# Button Information
def open_user_info():
    # Fetch user info from the database
    user_info = get_user_info(username)
    if user_info:
        game_window.destroy()
        os.system(f'python User_information.py {username}')
    else:
        messagebox.showerror("Error", "User information not found!")

info_button = tk.Button(game_window, text=f"Hello: {username}", font=("Helvetica", 18, "bold"), compound="left", bg="pink", fg="black", padx=10, pady=5, bd=0, command=open_user_info)
canvas.create_window(300, 130, window=info_button)

# Play chess with AI
def play_ai():
    game_window.destroy()
    os.system(f'python Game_with_AI.py {username}')

ai_button = tk.Button(game_window, text="Play against AI", font=("Helvetica", 15), image=ai_icon, compound="left", command=play_ai, bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5)
canvas.create_window(300, 200, window=ai_button)

# Play chess with players
def play_player():
    messagebox.showinfo("Player Game", "Not yet available!")

player_button = tk.Button(game_window, text="Play against Player", font=("Helvetica", 15), image=player_icon, compound="left", command=play_player, bg="#2196F3", fg="white", relief="flat", padx=10, pady=5)
canvas.create_window(300, 270, window=player_button)

# Log out of current login button
def logout():
    game_window.destroy()
    os.system('python login.py')

logout_button = tk.Button(game_window, text="Log out", font=("Helvetica", 15), compound="left", command=logout, bg="#FF5733", fg="white", relief="flat", padx=10, pady=5)
canvas.create_window(300, 360, window=logout_button)

# Exit button
exit_button = tk.Button(game_window, text="Exit", font=("Helvetica", 15), compound="left", command=game_window.destroy, bg="#FF5733", fg="white", relief="flat", padx=10, pady=5)
canvas.create_window(300, 430, window=exit_button)

game_window.mainloop()
