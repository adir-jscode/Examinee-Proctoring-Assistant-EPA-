import tkinter as tk
from tkinter import Label, Button
from proctoring import ProctoringApp
from recordings import RecordingsPage
from alerts import AlertsPage
from login_signup import LoginSignupApp


class MenuPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Menu")
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1F3B")  # Background color for the menu page

        self.show_menu()

    def show_menu(self):
        self.clear_frame()

        # Configuring grid layout for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Label showing logged-in user
        Label(
            self.root,
            text=f"Logged in as: {self.logged_in_user}",
            bg="#1E1F3B",
            fg="#B3B6D3",
            font=("Helvetica", 12),
        ).grid(row=0, column=0, pady=10, sticky="n")

        # Welcome label
        Label(
            self.root,
            text="Welcome to the Examinee Proctoring Assistant",
            bg="#1E1F3B",
            fg="#F4D35E",
            font=("Helvetica", 20, "bold"),
        ).grid(row=1, column=0, pady=20, sticky="n")

        # Proctoring Button
        proctoring_button = Button(
            self.root,
            text="Proctoring",
            command=self.open_proctoring,
            font=("Helvetica", 16, "bold"),
            bg="#3AA17E",
            fg="white",
            activebackground="#2F8764",
            activeforeground="white",
            relief="flat",
        )
        proctoring_button.grid(row=2, column=0, pady=10, ipadx=10, ipady=5, sticky="ew")

        # Recordings Button
        recordings_button = Button(
            self.root,
            text="Recordings",
            command=self.open_recordings,
            font=("Helvetica", 16, "bold"),
            bg="#3A6EA1",
            fg="white",
            activebackground="#2F5487",
            activeforeground="white",
            relief="flat",
        )
        recordings_button.grid(row=3, column=0, pady=10, ipadx=10, ipady=5, sticky="ew")

        # Alerts Button
        alerts_button = Button(
            self.root,
            text="Alerts",
            command=self.open_alerts,
            font=("Helvetica", 16, "bold"),
            bg="#F4A259",
            fg="white",
            activebackground="#D97A33",
            activeforeground="white",
            relief="flat",
        )
        alerts_button.grid(row=4, column=0, pady=10, ipadx=10, ipady=5, sticky="ew")

        # Logout Button
        logout_button = Button(
            self.root,
            text="Logout",
            command=self.logout,
            font=("Helvetica", 16, "bold"),
            bg="#D9534F",
            fg="white",
            activebackground="#C64540",
            activeforeground="white",
            relief="flat",
        )
        logout_button.grid(row=5, column=0, pady=20, ipadx=10, ipady=5, sticky="ew")

    def open_proctoring(self):
        self.clear_frame()
        ProctoringApp(self.root, self.logged_in_user)

    def open_recordings(self):
        self.clear_frame()
        RecordingsPage(self.root, self.logged_in_user)

    def open_alerts(self):
        self.clear_frame()
        AlertsPage(self.root, self.logged_in_user)

    def logout(self):
        self.clear_frame()
        LoginSignupApp(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    MenuPage(root, "User")
    root.mainloop()
