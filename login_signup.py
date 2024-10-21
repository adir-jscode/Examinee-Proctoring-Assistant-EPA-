import tkinter as tk
from tkinter import Label, Button, Entry, messagebox
from PIL import Image, ImageTk
import os
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()

class LoginSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EPA-Login")
        self.root.geometry("500x500")
        self.root.config(bg="#2E2F5B")
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root, bg="#2E2F5B")
        login_frame.grid(row=0, column=0, padx=20, pady=20)

        image_path = os.path.join("images", "login_images.png")
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(login_frame, image=self.image_tk, bg="#2E2F5B")
        self.image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=10)

        Label(login_frame, text="Login", font=("Helvetica", 22, "bold"), bg="#2E2F5B", fg="#F4D35E").grid(row=0, column=1, pady=10)
        Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=1, column=1, sticky="w", pady=5)
        self.username_entry = Entry(login_frame, font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=3, column=1, sticky="w", pady=5)
        self.password_entry = Entry(login_frame, show="*", font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        self.login_button = Button(login_frame, text="Login", command=self.login, font=("Helvetica", 14), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.login_button.grid(row=5, column=1, pady=20, ipadx=10, ipady=5)

        self.signup_button = Button(login_frame, text="Don't have an account? Signup", command=self.show_signup_screen, font=("Helvetica", 10), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.signup_button.grid(row=6, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Query database to check if credentials are valid
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            logged_in_user = username  # Set the logged-in user
            from menu import MenuPage
            self.clear_frame()
            MenuPage(self.root, logged_in_user)  # Pass the logged-in user to MenuPage
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        signup_frame = tk.Frame(self.root, bg="#2E2F5B")
        signup_frame.grid(row=0, column=0, padx=20, pady=20)

        Label(signup_frame, text="Signup", font=("Helvetica", 22, "bold"), bg="#2E2F5B", fg="#F4D35E").grid(row=0, column=1, pady=10)
        Label(signup_frame, text="Username:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=1, column=1, sticky="w", pady=5)
        self.signup_username_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.signup_username_entry.grid(row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        Label(signup_frame, text="Password:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=3, column=1, sticky="w", pady=5)
        self.signup_password_entry = Entry(signup_frame, show="*", font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.signup_password_entry.grid(row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        self.signup_button = Button(signup_frame, text="Signup", command=self.signup, font=("Helvetica", 14), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.signup_button.grid(row=5, column=1, pady=20, ipadx=10, ipady=5)

        Button(signup_frame, text="Back to Login", command=self.show_login_screen, font=("Helvetica", 10), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat").grid(row=6, column=1, pady=10)

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()

        # Insert the new user into the database
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
