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

        self.show_menu()

    def show_menu(self):
        self.clear_frame()

       
        Label(self.root, text=f"Logged in as: {self.logged_in_user}", font=("Helvetica", 12), fg="blue").pack(pady=10)

        Label(self.root, text="Welcome to the Examinee Proctoring Assistant", font=("Helvetica", 20)).pack(pady=20)

        # Proctoring Button
        proctoring_button = Button(self.root, text="Proctoring", command=self.open_proctoring, font=("Helvetica", 16), bg="green", fg="white")
        proctoring_button.pack(pady=10)

        # Recordings Button
        recordings_button = Button(self.root, text="Recordings", command=self.open_recordings, font=("Helvetica", 16), bg="blue", fg="white")
        recordings_button.pack(pady=10)

        # Alerts Button
        alerts_button = Button(self.root, text="Alerts", command=self.open_alerts, font=("Helvetica", 16), bg="orange", fg="white")
        alerts_button.pack(pady=10)

        # Logout Button
        logout_button = Button(self.root, text="Logout", command=self.logout, font=("Helvetica", 16), bg="red", fg="white")
        logout_button.pack(pady=20)

    def open_proctoring(self):
        self.clear_frame()
        ProctoringApp(self.root, self.logged_in_user)  # Pass logged_in_user here

    def open_recordings(self):
        self.clear_frame()
        RecordingsPage(self.root, self.logged_in_user) 

    def open_alerts(self):
        self.clear_frame()
        AlertsPage(self.root,self.logged_in_user)

    def logout(self):
        self.clear_frame()
        LoginSignupApp(self.root)  

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
