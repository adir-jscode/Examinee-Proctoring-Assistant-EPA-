import tkinter as tk
from tkinter import Label, Text, Button

class AlertsPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Alerts")
        self.root.geometry("800x600")

        self.show_alerts()

    def show_alerts(self):
        self.clear_frame()
        Label(self.root, text="Alerts", font=("Helvetica", 20)).pack(pady=10)

        self.alert_log_area = Text(self.root, height=20, width=80)
        self.alert_log_area.pack(pady=10)

        return_button = Button(self.root, text="Return to Menu", command=self.return_to_menu, bg="blue", fg="white", font=("Helvetica", 14))
        return_button.pack(pady=10)

        # Example of loading alerts
        self.load_alerts()

    def load_alerts(self):
        alerts = ["Alert 1", "Alert 2", "Alert 3"]  # Placeholder
        for alert in alerts:
            self.alert_log_area.insert(tk.END, f"{alert}\n")

    def return_to_menu(self):
        from menu import MenuPage
        MenuPage(self.root, self.logged_in_user)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
