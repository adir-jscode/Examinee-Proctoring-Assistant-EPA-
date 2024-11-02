import tkinter as tk
from tkinter import Label, Text, Button


class AlertsPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Alerts")
        self.root.geometry("800x600")
        self.bg_color = "#2E2F5B"  # Background color
        self.label_color = "#F4D35E"  # Label text color
        self.button_bg_color = "#505581"  # Button background color
        self.button_fg_color = "#FFFFFF"  # Button text color

        self.show_alerts()

    def show_alerts(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        # Title Label
        title_label = Label(
            self.root,
            text="Alerts",
            font=("Helvetica", 20),
            bg=self.bg_color,
            fg=self.label_color,
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Alert Log Area
        self.alert_log_area = Text(
            self.root, height=20, width=80, bg="#FFFFFF", fg="#000000"
        )
        self.alert_log_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Return to Menu Button
        return_button = Button(
            self.root,
            text="Back",
            command=self.return_to_menu,
            bg="#D9534F",
            fg=self.button_fg_color,
            font=("Helvetica", 14),
        )
        return_button.grid(row=2, column=0, pady=10)

        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Load alerts into the text area
        self.load_alerts()

    def load_alerts(self):
        alerts = ["Alert 1", "Alert 2", "Alert 3"]
        for alert in alerts:
            self.alert_log_area.insert(tk.END, f"{alert}\n")

    def return_to_menu(self):
        from menu import MenuPage

        MenuPage(self.root, self.logged_in_user)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
