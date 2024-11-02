import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label, Text, Button, Frame
import time
import os
import logging
from datetime import datetime

# MediaPipe setup for face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5
)

# Global placeholders
X_AXIS_CHEAT = 0
Y_AXIS_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.6

RECORDINGS_DIR = "recordings"
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)


class ProctoringApp:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Proctoring")
        self.root.geometry("800x600")
        self.cap = None
        self.is_proctoring = False
        self.out = None

        # UI colors
        self.bg_color = "#2E2F5B"  # Main background color
        self.label_color = "#F4D35E"  # Label text color
        self.button_bg_color = "#505581"  # Button background color
        self.button_fg_color = "#FFFFFF"  # Button text color
        self.alert_bg_color = "#F0D3A0"  # Valid alert log background color
        self.button_start_bg_color = "#28a745"  # Start button background color
        self.button_stop_bg_color = "#dc3545"  # Stop button background color
        self.button_back_bg_color = "#007bff"  # Back button background color
        self.button_fg_color = "#FFFFFF"  # Button text color
        self.alert_bg_color = "#F0D3A0"  # Valid alert log background color

        # Main frame
        self.main_frame = Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both")

        # Video label
        self.video_label = Label(self.main_frame, bg=self.bg_color)
        self.video_label.pack(pady=10, fill="both", expand=True)

        # Alert log area
        self.alert_log_area = Text(
            self.main_frame, height=10, width=80, bg=self.alert_bg_color, fg="#000000"
        )
        self.alert_log_area.pack(pady=10, fill="both", expand=True)
        self.alert_log_area.insert(tk.END, "Proctoring Log:\n")

        # Start/Stop Buttons
        self.start_button = Button(
            self.main_frame,
            text="Start Proctoring",
            command=self.start_proctoring,
            bg=self.button_bg_color,
            fg=self.button_fg_color,
        )
        self.start_button.pack(side="left", padx=10)

        self.stop_button = Button(
            self.main_frame,
            text="Stop Proctoring",
            command=self.stop_proctoring,
            bg=self.button_bg_color,
            fg=self.button_fg_color,
        )
        self.stop_button.pack(side="left", padx=10)

        # Back to Menu Button
        self.back_button = Button(
            self.main_frame,
            text="Back to Menu",
            command=self.back_to_menu,
            bg=self.button_bg_color,
            fg=self.button_fg_color,
        )
        self.back_button.pack(side="left", padx=10)

        return_button = Button(
            self.root,
            text="Return to Menu",
            command=self.return_to_menu,
            bg="blue",
            fg="white",
            font=("Helvetica", 14),
        )
        return_button.pack(pady=10)

        # Configure grid layout
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def start_proctoring(self):
        self.is_proctoring = True
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
        filepath = os.path.join(RECORDINGS_DIR, filename)
        self.out = cv2.VideoWriter(filepath, fourcc, 20.0, (640, 480))
        self.process_frames()

    def stop_proctoring(self):
        self.is_proctoring = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.out:
            self.out.release()
            self.out = None
        self.video_label.config(image="")

    def back_to_menu(self):
        self.clear_frame()
        from menu import MenuPage

        MenuPage(self.root, self.logged_in_user)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def process_frames(self):
        if not self.is_proctoring:
            return

        success, frame = self.cap.read()
        if success:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)
            self.detect_head_pose_and_mask(results, frame)

            # Convert frame to Tkinter-compatible format
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
            self.video_label.imgtk = img
            self.video_label.config(image=img)

            if self.out:
                self.out.write(frame)

        self.root.after(10, self.process_frames)

    def detect_head_pose_and_mask(self, results, frame):
        global X_AXIS_CHEAT, Y_AXIS_CHEAT, PERCENTAGE_CHEAT

        img_h, img_w, _ = frame.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx in [33, 263, 1, 61, 291, 199]:  # Key points for head pose
                        x, y = int(lm.x * img_w), int(lm.y * img_h)
                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z * 8000])

                # Compute head pose
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)
                focal_length = img_w
                cam_matrix = np.array(
                    [
                        [focal_length, 0, img_h / 2],
                        [0, focal_length, img_w / 2],
                        [0, 0, 1],
                    ]
                )
                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                success, rot_vec, trans_vec = cv2.solvePnP(
                    face_3d, face_2d, cam_matrix, dist_matrix
                )
                rmat, _ = cv2.Rodrigues(rot_vec)
                angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

                # Analyze head pose
                x, y = angles[0] * 360, angles[1] * 360
                self.analyze_cheat(x, y)

                # Overlay head pose direction on video frame
                if y < -10:
                    direction = "Looking Left"
                elif y > 10:
                    direction = "Looking Right"
                elif x < -10:
                    direction = "Looking Down"
                else:
                    direction = "Looking Forward"
                cv2.putText(
                    frame,
                    f"{direction} (x:{int(x)}, y:{int(y)})",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

                # Check mask detection based on landmarks
                mask_on = self.detect_mask(face_landmarks, img_w, img_h)
                mask_status = "Mask On" if mask_on else "Mask Off"
                cv2.putText(
                    frame,
                    mask_status,
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0) if mask_on else (0, 0, 255),
                    2,
                )

    def analyze_cheat(self, x, y):
        global PERCENTAGE_CHEAT, CHEAT_THRESH

        # Determine cheat levels based on x, y thresholds
        if abs(y) > 10:
            X_AXIS_CHEAT = 1
        else:
            X_AXIS_CHEAT = 0

        if x < -5:
            Y_AXIS_CHEAT = 1
        else:
            Y_AXIS_CHEAT = 0

        if X_AXIS_CHEAT or Y_AXIS_CHEAT:
            PERCENTAGE_CHEAT = min(PERCENTAGE_CHEAT + 0.05, 1.0)  # Increase cheat level
        else:
            PERCENTAGE_CHEAT = max(PERCENTAGE_CHEAT - 0.05, 0.0)  # Decrease cheat level

        # Trigger cheat alert
        if PERCENTAGE_CHEAT > CHEAT_THRESH:
            self.alert_log_area.insert(
                tk.END,
                f"{datetime.now()}: Suspicious behavior detected! Cheat Probability: {PERCENTAGE_CHEAT:.2f}\n",
            )
            self.alert_log_area.see(tk.END)
            logging.warning(
                f"Suspicious behavior detected at {datetime.now()}. Cheat Probability: {PERCENTAGE_CHEAT:.2f}"
            )

    def detect_mask(self, face_landmarks, img_w, img_h):
        """Detect if a mask is worn based on landmark positions."""
        # Define mouth and nose regions using specific landmarks
        mouth_region = [face_landmarks.landmark[13], face_landmarks.landmark[14]]
        nose_region = [face_landmarks.landmark[1]]

        # Calculate if landmarks in these areas fall below a certain threshold on the Y-axis (indicating a mask)
        mask_on = all(lm.y * img_h > img_h * 0.6 for lm in mouth_region + nose_region)
        return mask_on


# Sample app launch
if __name__ == "__main__":
    root = tk.Tk()
    app = ProctoringApp(root, logged_in_user="test_user")
    root.mainloop()
