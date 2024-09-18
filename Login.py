import os
import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

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

# Insert new user into the database
def insert_user_to_db(username, password_hash):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO Users (username, password) VALUES (%s, %s)"
            values = (username, password_hash)
            cursor.execute(sql, values)
            connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Register Failed", f"Failed to register user: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

# Check user login
def validate_login(username, password):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                return user
            else:
                return None
        except mysql.connector.Error as e:
            messagebox.showerror("Login Failed", f"Failed to validate user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Main frame
root = tk.Tk()
root.title("Cyber Checkers")
window_width = 500
window_height = 600

# Set the window position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = int((screen_width / 2) - (window_width / 2))
y_position = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.config(bg="#F0F0F0")
root.resizable(False, False)

# Switch Frame
def show_frame(frame):
    frame.tkraise()

# Input box prompt information
def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    def on_entry_click(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg='black')
    def on_focusout(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')
    entry.bind("<FocusIn>", on_entry_click)
    entry.bind("<FocusOut>", on_focusout)

# --------- Login Frame --------------
login_frame = tk.Frame(root, bg="#F0F0F0")
login_frame.place(x=0, y=0, width=window_width, height=window_height)
title_label = tk.Label(login_frame, text="Welcome to Cyber Checkers", font=("Helvetica", 26, "bold"), bg="#F0F0F0")
title_label.pack(pady=25)
login_input_frame = tk.Frame(login_frame, bg="#F0F0F0")
login_input_frame.pack(pady=10)

# Enter Username
username_label = tk.Label(login_input_frame, text="Username:", font=("Helvetica", 18), bg="#F0F0F0")
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
username_entry = tk.Entry(login_input_frame, font=("Helvetica", 18), width=22, borderwidth=2, relief="groove")
username_entry.grid(row=0, column=1, padx=10, pady=10)
add_placeholder(username_entry, "Enter your username")

# Enter password
password_label = tk.Label(login_input_frame, text="Password:", font=("Helvetica", 18), bg="#F0F0F0")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(login_input_frame, font=("Helvetica", 18), show="*", width=22, borderwidth=2, relief="groove")
password_entry.grid(row=1, column=1, padx=10, pady=10)
add_placeholder(password_entry, "******")

# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning("Login Failed", "Please enter both username and password.")
    else:
        user = validate_login(username, password)
        if user:
            root.destroy()  # Close the login window
            python_executable = sys.executable
            os.system(f'"{python_executable}" Game_frame.py {username}')
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

# Login button
login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 20, "bold"), width=18, bg="#4CAF50", fg="white",
                         command=login)
login_button.pack(pady=40)

# Register button
register_button = tk.Button(login_frame, text="Register", font=("Helvetica", 20, "bold"), width=18, bg="#2196F3", fg="white",
                            command=lambda: show_frame(register_frame))
register_button.pack(pady=10)

# --------- Register Frame --------------
register_frame = tk.Frame(root, bg="#F0F0F0")
register_frame.place(x=0, y=0, width=window_width, height=window_height)

title_label_reg = tk.Label(register_frame, text="Register for Cyber Checkers", font=("Helvetica", 26, "bold"), bg="#F0F0F0")
title_label_reg.pack(pady=25)

# Register frame
register_input_frame = tk.Frame(register_frame, bg="#F0F0F0")
register_input_frame.pack(pady=10)

# Username
username_label_reg = tk.Label(register_input_frame, text="Username:", font=("Helvetica", 14), bg="#F0F0F0")
username_label_reg.grid(row=0, column=0, padx=10, pady=10, sticky="e")
username_entry_reg = tk.Entry(register_input_frame, font=("Helvetica", 14), width=22, borderwidth=2, relief="groove")
username_entry_reg.grid(row=0, column=1, padx=10, pady=10)
add_placeholder(username_entry_reg, "Enter your username")

# Password
password_label_reg = tk.Label(register_input_frame, text="Password:", font=("Helvetica", 14), bg="#F0F0F0")
password_label_reg.grid(row=1, column=0, padx=10, pady=10, sticky="e")
password_entry_reg = tk.Entry(register_input_frame, font=("Helvetica", 14), show="*", width=22, borderwidth=2, relief="groove")
password_entry_reg.grid(row=1, column=1, padx=10, pady=10)
add_placeholder(password_entry_reg, "******")

# Confirm Password
confirm_password_label_reg = tk.Label(register_input_frame, text="Confirm Password:", font=("Helvetica", 14), bg="#F0F0F0")
confirm_password_label_reg.grid(row=2, column=0, padx=10, pady=10, sticky="e")
confirm_password_entry_reg = tk.Entry(register_input_frame, font=("Helvetica", 14), show="*", width=22, borderwidth=2, relief="groove")
confirm_password_entry_reg.grid(row=2, column=1, padx=10, pady=10)
add_placeholder(confirm_password_entry_reg, "******")

# Registration function
def register():
    username = username_entry_reg.get()
    password = password_entry_reg.get()
    confirm_password = confirm_password_entry_reg.get()

    if username == "" or password == "" or confirm_password == "":
        messagebox.showwarning("Register Failed", "All fields are required.")
    elif password != confirm_password:
        messagebox.showerror("Register Failed", "Passwords do not match.")
    else:
        password_hash = generate_password_hash(password)
        if insert_user_to_db(username, password_hash):
            messagebox.showinfo("Register Successful", f"Account for {username} has been created!")
            show_frame(login_frame)  # Go back to login frame after successful registration

# Register button
register_button_reg = tk.Button(register_frame, text="Register", font=("Helvetica", 20, "bold"), width=18, bg="#4CAF50", fg="white",
                                command=register)
register_button_reg.pack(pady=20)

# Cancel button
cancel_button = tk.Button(register_frame, text="Cancel", font=("Helvetica", 20, "bold"), width=18, bg="#FF5733", fg="white",
                          command=lambda: show_frame(login_frame))
cancel_button.pack(pady=10)

# Footer labels
footer_label = tk.Label(login_frame, text="Cyber Checkers © 2024", font=("Helvetica", 10), bg="#F0F0F0", fg="gray")
footer_label.pack(side="bottom", pady=10)
footer_label = tk.Label(register_frame, text="Cyber Checkers © 2024", font=("Helvetica", 10), bg="#F0F0F0", fg="gray")
footer_label.pack(side="bottom", pady=10)
footer_label_reg = tk.Label(login_frame, text="Project team: Byte me", font=("Helvetica", 15), bg="#F0F0F0", fg="gray")
footer_label_reg.pack(side="bottom", pady=20)
footer_label_reg = tk.Label(register_frame, text="Project team: Byte me", font=("Helvetica", 15), bg="#F0F0F0", fg="gray")
footer_label_reg.pack(side="bottom", pady=20)

# Show login frame
show_frame(login_frame)

root.mainloop()
