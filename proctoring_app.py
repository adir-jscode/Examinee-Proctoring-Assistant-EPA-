import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk

class ProctoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Examinee Proctoring Assistant")
        self.root.geometry("800x600")

        # Label to display video feed
        self.video_label = Label(self.root)
        self.video_label.pack()

        # Start and Stop buttons with custom colors
        self.start_button = Button(self.root, text="Start Proctoring", command=self.start_proctoring, bg="green", fg="white", font=("Helvetica", 14))
        self.start_button.pack(side="left", padx=10)

        self.stop_button = Button(self.root, text="Stop Proctoring", command=self.stop_proctoring, bg="red", fg="white", font=("Helvetica", 14))
        self.stop_button.pack(side="left", padx=10)

        self.cap = None
        self.is_proctoring = False

    def start_proctoring(self):
        if not self.is_proctoring:
            self.is_proctoring = True
            self.cap = cv2.VideoCapture(0)  # Capture video from the webcam
            self.show_frame()

    def stop_proctoring(self):
        self.is_proctoring = False
        if self.cap:
            self.cap.release()
            self.cap = None
        # Clear the video frame
        self.video_label.config(image='')

    def show_frame(self):
        if self.is_proctoring:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to a format Tkinter can display
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.root.after(10, self.show_frame)  # Keep updating the frame

if __name__ == "__main__":
    root = tk.Tk()
    app = ProctoringApp(root)
    root.mainloop()
