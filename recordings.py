import tkinter as tk
from tkinter import Label, Button, Listbox, Scrollbar, Text
import cv2
import os
from tkinter import messagebox

RECORDINGS_DIR = "recordings"

# Create a directory to store recordings if it doesn't exist
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

class RecordingsPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user  # Store the logged-in user
        self.root.title("Examinee Proctoring Assistant - Recordings")
        self.root.geometry("800x600")
        
        self.show_recordings()

    def show_recordings(self):
        self.clear_frame()
        Label(self.root, text="Recordings", font=("Helvetica", 20)).pack(pady=10)

        # Listbox to display available recordings
        self.recordings_listbox = Listbox(self.root, height=15, width=50)
        self.recordings_listbox.pack(pady=10)

        recordings = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".avi")]
        for recording in recordings:
            self.recordings_listbox.insert(tk.END, recording)

        # Play button to play the selected recording
        play_button = Button(self.root, text="Play Selected", command=self.play_selected_recording, bg="blue", fg="white", font=("Helvetica", 14))
        play_button.pack(pady=10)

        return_button = Button(self.root, text="Return to Menu", command=self.return_to_menu, bg="blue", fg="white", font=("Helvetica", 14))
        return_button.pack(pady=10)

    def play_selected_recording(self):
        try:
            selected_recording = self.recordings_listbox.get(self.recordings_listbox.curselection())
            recording_path = os.path.join(RECORDINGS_DIR, selected_recording)
            self.play_video(recording_path)
        except:
            messagebox.showerror("Error", "Please select a recording to play.")

    def play_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Playing Recording', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def return_to_menu(self):
        self.clear_frame()
        from menu import MenuPage  # Delay import to avoid circular import
        MenuPage(self.root, self.logged_in_user)  # Pass logged_in_user when returning to MenuPage

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
