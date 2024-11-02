import tkinter as tk
from tkinter import Label, Button, Listbox, Scrollbar, messagebox
import cv2
import os

RECORDINGS_DIR = "recordings"

if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)


class RecordingsPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Recordings")
        self.root.geometry("800x600")
        self.bg_color = "#2E2F5B"  # Background color
        self.label_color = "#F4D35E"  # Label text color
        self.button_bg_color = "#505581"  # Button background color
        self.button_fg_color = "#FFFFFF"  # Button text color

        self.show_recordings()

    def show_recordings(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        # Title Label
        title_label = Label(
            self.root,
            text="Recordings",
            font=("Helvetica", 20),
            bg=self.bg_color,
            fg=self.label_color,
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Recordings Listbox
        self.recordings_listbox = Listbox(
            self.root, height=15, width=50, bg="#FFFFFF", fg="#000000"
        )
        self.recordings_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Listbox
        scrollbar = Scrollbar(self.root)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.recordings_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.recordings_listbox.yview)

        self.populate_recordings()

        # Play Button
        play_button = Button(
            self.root,
            text="Play",
            command=self.play_selected_recording,
            bg="#3AA17E",
            fg=self.button_fg_color,
            font=("Helvetica", 14),
        )
        play_button.grid(row=2, column=0, padx=10, pady=10)

        # Delete Button
        delete_button = Button(
            self.root,
            text="Delete",
            command=self.delete_selected_recording,
            bg="#D9534F",
            fg=self.button_fg_color,
            font=("Helvetica", 14),
        )
        delete_button.grid(row=2, column=1, padx=10, pady=10)

        # Return to Menu Button
        return_button = Button(
            self.root,
            text="Return to Menu",
            command=self.return_to_menu,
            bg="#F4A259",
            fg=self.button_fg_color,
            font=("Helvetica", 14),
        )
        return_button.grid(row=2, column=2, padx=10, pady=10)

        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def populate_recordings(self):
        """Populates the listbox with recording files."""
        self.recordings_listbox.delete(0, tk.END)
        recordings = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".avi")]
        for recording in recordings:
            self.recordings_listbox.insert(tk.END, recording)

    def play_selected_recording(self):
        try:
            selected_recording = self.recordings_listbox.get(
                self.recordings_listbox.curselection()
            )
            recording_path = os.path.join(RECORDINGS_DIR, selected_recording)
            self.play_video(recording_path)
        except tk.TclError:
            messagebox.showerror("Error", "Please select a recording to play.")

    def play_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Playing Recording", frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

    def delete_selected_recording(self):
        try:
            selected_recording = self.recordings_listbox.get(
                self.recordings_listbox.curselection()
            )
            recording_path = os.path.join(RECORDINGS_DIR, selected_recording)

            # Confirm deletion
            confirm = messagebox.askyesno(
                "Delete Confirmation",
                f"Are you sure you want to delete '{selected_recording}'?",
            )
            if confirm:
                os.remove(recording_path)
                messagebox.showinfo(
                    "Deleted", f"'{selected_recording}' has been deleted."
                )
                self.populate_recordings()
        except tk.TclError:
            messagebox.showerror("Error", "Please select a recording to delete.")

    def return_to_menu(self):
        self.clear_frame()
        from menu import MenuPage

        MenuPage(self.root, self.logged_in_user)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
