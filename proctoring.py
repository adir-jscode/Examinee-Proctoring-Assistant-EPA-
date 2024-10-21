import tkinter as tk
from tkinter import Label, Button, Text, Scrollbar, messagebox
import os
import cv2
from PIL import Image, ImageTk
from datetime import datetime

RECORDINGS_DIR = "recordings"

if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

class ProctoringApp:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Proctoring")
        self.root.geometry("800x600")
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.is_proctoring = False
        self.recording = False
        self.out = None
        self.last_face_detected_time = None
        self.capture = None  # Initialize capture as None

        self.show_proctoring()

    def show_proctoring(self):
        self.clear_frame()
        Label(self.root, text="Proctoring", font=("Helvetica", 20)).pack(pady=10)

        self.video_label = Label(self.root)
        self.video_label.pack(pady=10)

        self.start_button = Button(self.root, text="Start Proctoring", command=self.start_proctoring, bg="green", fg="white", font=("Helvetica", 14))
        self.start_button.pack(side="left", padx=10)
        self.stop_button = Button(self.root, text="Stop Proctoring", command=self.stop_proctoring, bg="red", fg="white", font=("Helvetica", 14))
        self.stop_button.pack(side="left", padx=10)

        # Return to Menu Button
        return_button = Button(self.root, text="Return to Menu", command=self.confirm_return_to_menu, bg="blue", fg="white", font=("Helvetica", 14))
        return_button.pack(pady=10)

        self.alert_log_area = Text(self.root, height=10, width=80)
        self.alert_log_area.pack(pady=10)

        scrollbar = Scrollbar(self.root, command=self.alert_log_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.alert_log_area.config(yscrollcommand=scrollbar.set)

    def start_proctoring(self):
        self.is_proctoring = True
        self.capture = cv2.VideoCapture(0)  # Create the capture object
        self.record_video()

    def stop_proctoring(self):
        self.is_proctoring = False
        if self.capture is not None:  # Check if capture exists
            self.capture.release()
            self.capture = None  # Reset capture after releasing
        if self.out:
            self.out.release()
        self.video_label.config(image="")
        self.log_alert("Proctoring stopped.")

    def record_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.out = cv2.VideoWriter(f"{RECORDINGS_DIR}/proctoring_{current_time}.avi", fourcc, 20.0, (640, 480))

        self.detect_faces()

    def detect_faces(self):
        if self.is_proctoring and self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    self.log_alert(f"Face detected at {datetime.now().strftime('%H:%M:%S')}")

                self.out.write(frame)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)

            self.root.after(10, self.detect_faces)

    def log_alert(self, message):
        self.alert_log_area.insert(tk.END, f"{message}\n")
        self.alert_log_area.see(tk.END)

    def confirm_return_to_menu(self):
       
        if messagebox.askyesno("Confirmation", "Are you sure you want to stop and return to the menu?"):
            self.stop_proctoring()
        from menu import MenuPage
        MenuPage(self.root, self.logged_in_user)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
