import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Menu
from PIL import Image, ImageTk
import os
import cv2

# Dummy database for storing user credentials (in a real system, you'd use a database)
users_db = {}

class ProctoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Examinee Proctoring Assistant")
        self.root.geometry("800x600")

        # Create the menu
        self.create_menu()

        # Label to display video feed
        self.video_label = Label(self.root)
        self.video_label.pack(pady=10)

        # Start and Stop buttons
        self.start_button = Button(self.root, text="Start Proctoring", command=self.start_proctoring, bg="green", fg="white", font=("Helvetica", 14))
        self.start_button.pack(side="left", padx=10)

        self.stop_button = Button(self.root, text="Stop Proctoring", command=self.stop_proctoring, bg="red", fg="white", font=("Helvetica", 14))
        self.stop_button.pack(side="left", padx=10)

        # Alerts Section
        self.alerts_label = Label(self.root, text="Alerts:", font=("Helvetica", 14))
        self.alerts_label.pack(pady=5)

        self.alerts_text = tk.Text(self.root, height=5, width=60, state='disabled', font=("Helvetica", 12))
        self.alerts_text.pack(pady=5)

        # Scrollbar for alerts
        self.scrollbar = tk.Scrollbar(self.root, command=self.alerts_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.alerts_text.config(yscrollcommand=self.scrollbar.set)

        # Log Section
        self.logs_label = Label(self.root, text="Logs:", font=("Helvetica", 14))
        self.logs_label.pack(pady=5)

        self.logs_text = tk.Text(self.root, height=10, width=60, state='disabled', font=("Helvetica", 12))
        self.logs_text.pack(pady=5)

        # Scrollbar for logs
        self.logs_scrollbar = tk.Scrollbar(self.root, command=self.logs_text.yview)
        self.logs_scrollbar.pack(side="right", fill="y")
        self.logs_text.config(yscrollcommand=self.logs_scrollbar.set)

        self.cap = None
        self.is_proctoring = False

    def create_menu(self):
        menubar = Menu(self.root)

        # Create pages submenu
        pages_menu = Menu(menubar, tearoff=0)
        pages_menu.add_command(label="Dashboard", command=self.show_dashboard)
        pages_menu.add_command(label="Proctoring", command=self.show_proctoring)
        pages_menu.add_command(label="Alerts", command=self.show_alerts)
        pages_menu.add_command(label="Logs", command=self.show_logs)
        pages_menu.add_command(label="Settings", command=self.show_settings)
        pages_menu.add_separator()
        pages_menu.add_command(label="Profile", command=self.show_profile)
        pages_menu.add_command(label="Logout", command=self.logout)

        menubar.add_cascade(label="Navigate", menu=pages_menu)

        # Configure the menu
        self.root.config(menu=menubar)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_frame()
        Label(self.root, text="Dashboard", font=("Helvetica", 20)).pack(pady=10)

    def show_proctoring(self):
        self.clear_frame()
        self.__init__(self.root)  # Reload the proctoring page

    def show_alerts(self):
        self.clear_frame()
        Label(self.root, text="Alerts", font=("Helvetica", 20)).pack(pady=10)
        Label(self.root, text="No alerts to show", font=("Helvetica", 14)).pack(pady=10)

    def show_logs(self):
        self.clear_frame()
        Label(self.root, text="Logs", font=("Helvetica", 20)).pack(pady=10)

    def show_settings(self):
        self.clear_frame()
        Label(self.root, text="Settings", font=("Helvetica", 20)).pack(pady=10)

    def show_profile(self):
        self.clear_frame()
        Label(self.root, text="Profile", font=("Helvetica", 20)).pack(pady=10)

    def logout(self):
        result = messagebox.askquestion("Logout", "Are you sure you want to logout?")
        if result == 'yes':
            self.clear_frame()
            LoginSignupApp(self.root)

    def start_proctoring(self):
        if not self.is_proctoring:
            self.is_proctoring = True
            self.cap = cv2.VideoCapture(0)  # Capture video from the webcam
            self.show_frame()
            self.log_activity("Proctoring started.")

    def stop_proctoring(self):
        self.is_proctoring = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.config(image='')  # Clear the video frame
        self.log_activity("Proctoring stopped.")

    def show_frame(self):
        if self.is_proctoring:
            ret, frame = self.cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.root.after(10, self.show_frame)

    def log_activity(self, message):
        self.logs_text.config(state='normal')
        self.logs_text.insert(tk.END, message + '\n')
        self.logs_text.config(state='disabled')
        self.logs_text.yview(tk.END)

class LoginSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EPA-Login")
        self.root.geometry("500x500")
        self.root.config(bg="#2E2F5B")  # Background color set to #2E2F5B

        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root, bg="#2E2F5B")
        login_frame.grid(row=0, column=0, padx=20, pady=20)

        image_path = os.path.join("images", "login_image.png")  # Adjust the image name as per your file
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

    def show_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        signup_frame = tk.Frame(self.root, bg="#2E2F5B")
        signup_frame.grid(row=0, column=0, padx=20, pady=20)

        image_path = os.path.join("images", "login_image.png")
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(signup_frame, image=self.image_tk, bg="#2E2F5B")
        self.image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=10)

        Label(signup_frame, text="Signup", font=("Helvetica", 22, "bold"), bg="#2E2F5B", fg="#F4D35E").grid(row=0, column=1, pady=10)
        Label(signup_frame, text="Create Username:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=1, column=1, sticky="w", pady=5)
        self.username_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        Label(signup_frame, text="Create Password:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=3, column=1, sticky="w", pady=5)
        self.password_entry = Entry(signup_frame, show="*", font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        self.signup_button = Button(signup_frame, text="Signup", command=self.signup, font=("Helvetica", 14), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.signup_button.grid(row=5, column=1, pady=20, ipadx=10, ipady=5)

        self.back_to_login_button = Button(signup_frame, text="Already have an account? Login", command=self.show_login_screen, font=("Helvetica", 10), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.back_to_login_button.grid(row=6, column=1, pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users_db:
            messagebox.showerror("Signup Failed", "Username already exists!")
        else:
            users_db[username] = password
            messagebox.showinfo("Signup Success", "Account created successfully! Please login.")
            self.show_login_screen()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin":
            messagebox.showinfo("Login Success", "You have logged in successfully!")
            self.open_main_proctoring_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_main_proctoring_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        app = ProctoringApp(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupApp(root)
    root.mainloop()
