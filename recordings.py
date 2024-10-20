import tkinter as tk
from tkinter import Label, Button, Listbox, Scrollbar, Text

class RecordingsPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Examinee Proctoring Assistant - Recordings")
        self.root.geometry("800x600")

        self.show_recordings()

    def show_recordings(self):
        self.clear_frame()
        Label(self.root, text="Recordings", font=("Helvetica", 20)).pack(pady=10)

        self.recordings_listbox = Listbox(self.root, height=20, width=80)
        self.recordings_listbox.pack(pady=10)

        scrollbar = Scrollbar(self.root, command=self.recordings_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.recordings_listbox.config(yscrollcommand=scrollbar.set)

        self.load_recordings()

        return_button = Button(self.root, text="Return to Menu", command=self.return_to_menu, bg="blue", fg="white", font=("Helvetica", 14))
        return_button.pack(pady=10)

    def load_recordings(self):
        recordings = ["Recording 1", "Recording 2", "Recording 3"]  # Placeholder
        for recording in recordings:
            self.recordings_listbox.insert(tk.END, recording)

    def return_to_menu(self):
        from menu import MenuPage
        MenuPage(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
