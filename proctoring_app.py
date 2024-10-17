import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Menu, Text, Scrollbar, Listbox
from PIL import Image, ImageTk
import os
import cv2
import logging
from datetime import datetime

# Dummy database for storing user credentials (in a real system, you'd use a database)
users_db = {}

# Setup logging
logging.basicConfig(filename='proctoring_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

RECORDINGS_DIR = "recordings"

# Create a directory to store recordings if it doesn't exist
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

class ProctoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Examinee Proctoring Assistant")
        self.root.geometry("800x600")
        self.root.grid_rowconfigure(0, weight=1)  # Make rows responsive
        self.root.grid_columnconfigure(0, weight=1)  # Make columns responsive

        # Load Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Create the main menu
        self.create_menu()

        # Create the initial view
        self.show_proctoring()  # Show the proctoring page initially

        self.alerts = []  # Store alerts
        self.is_proctoring = False  # Proctoring status
        self.recording = False
        self.out = None  # VideoWriter object for recording

    def create_menu(self):
        menubar = Menu(self.root)

        # Create pages submenu
        pages_menu = Menu(menubar, tearoff=0)
        pages_menu.add_command(label="Dashboard", command=self.show_dashboard)
        pages_menu.add_command(label="Proctoring", command=self.show_proctoring)
        pages_menu.add_command(label="Recordings", command=self.show_recordings)  # Added Recordings menu
        pages_menu.add_command(label="Alerts", command=self.show_alerts)
        pages_menu.add_command(label="Logs", command=self.show_logs)
        pages_menu.add_command(label="Settings", command=self.show_settings)
        pages_menu.add_command(label="Profile", command=self.show_profile)
        pages_menu.add_command(label="Logout", command=self.logout)

        menubar.add_cascade(label="Navigate", menu=pages_menu)

        # Configure the menu
        self.root.config(menu=menubar)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_frame()
        Label(self.root, text="Dashboard", font=("Helvetica", 20)).pack(pady=10)

    def show_proctoring(self):
        self.clear_frame()
        Label(self.root, text="Proctoring", font=("Helvetica", 20)).pack(pady=10)
        self.video_label = Label(self.root)
        self.video_label.pack(pady=10)
        self.start_button = Button(self.root, text="Start Proctoring", command=self.start_proctoring, bg="green", fg="white", font=("Helvetica", 14))
        self.start_button.pack(side="left", padx=10)
        self.stop_button = Button(self.root, text="Stop Proctoring", command=self.stop_proctoring, bg="red", fg="white", font=("Helvetica", 14))
        self.stop_button.pack(side="left", padx=10)

        # Button to navigate to the Recordings page
        recordings_button = Button(self.root, text="Show Recordings", command=self.show_recordings, bg="blue", fg="white", font=("Helvetica", 14))
        recordings_button.pack(side="left", padx=10)  # Button to show recordings

        # Alert and Log display area
        self.alert_log_area = Text(self.root, height=10, width=80)
        self.alert_log_area.pack(pady=10)

        # Add a scrollbar
        scrollbar = Scrollbar(self.root, command=self.alert_log_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.alert_log_area.config(yscrollcommand=scrollbar.set)

    def show_alerts(self):
        self.clear_frame()
        Label(self.root, text="Alerts", font=("Helvetica", 20)).pack(pady=10)
        Label(self.root, text="No alerts to show", font=("Helvetica", 14)).pack(pady=10)

    def show_logs(self):
        self.clear_frame()
        Label(self.root, text="Logs", font=("Helvetica", 20)).pack(pady=10)

    def show_settings(self):
        self.clear_frame()
        Label(self.root, text="Settings", font=("Helvetica", 20)).pack(pady=10)

    def show_profile(self):
        self.clear_frame()
        Label(self.root, text="Profile", font=("Helvetica", 20)).pack(pady=10)

    def show_recordings(self):
        self.clear_frame()
        Label(self.root, text="Recordings", font=("Helvetica", 20)).pack(pady=10)

        # Listbox to display available recordings
        self.recordings_listbox = Listbox(self.root, height=15, width=50)
        self.recordings_listbox.pack(pady=10)

        # Load recordings from the directory
        recordings = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".avi")]
        for recording in recordings:
            self.recordings_listbox.insert(tk.END, recording)

        # Play button to play the selected recording
        play_button = Button(self.root, text="Play Selected", command=self.play_selected_recording, bg="blue", fg="white", font=("Helvetica", 14))
        play_button.pack(pady=10)
        
        # Button to navigate back to the Proctoring page
        proctoring_button = Button(self.root, text="Back to Proctoring", command=self.show_proctoring, bg="green", fg="white", font=("Helvetica", 14))
        proctoring_button.pack(pady=10)

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

    def logout(self):
        result = messagebox.askquestion("Logout", "Are you sure you want to logout?")
        if result == 'yes':
            self.clear_frame()
            LoginSignupApp(self.root)

    def start_proctoring(self):
        self.is_proctoring = True
        self.cap = cv2.VideoCapture(0)  # Capture video from the webcam
        
        # Setup video writer for recording
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video format
        filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".avi"
        filepath = os.path.join(RECORDINGS_DIR, filename)
        self.out = cv2.VideoWriter(filepath, fourcc, 20.0, (640, 480))  # Adjust frame size to webcam output
        
        self.recording = True  # Flag to indicate recording
        self.show_frame()
        logging.info("Proctoring started.")
        self.alert_log_area.insert(tk.END, "Proctoring started.\nRecording started.\n")

    def stop_proctoring(self):
        if self.cap:
            self.cap.release()
            self.cap = None

        if self.out:
            self.out.release()  # Stop recording
        
        self.video_label.config(image='')  # Clear the video frame
        self.is_proctoring = False
        self.recording = False
        logging.info("Proctoring stopped.")
        self.alert_log_area.insert(tk.END, "Proctoring stopped.\nRecording stopped.\n")

    def show_frame(self):
        if self.cap and self.is_proctoring:
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to grayscale for face detection
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

                # Draw rectangles around detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle
                    logging.info(f"Face detected at ({x}, {y}, {w}, {h}).")
                    alert_message = f"Face detected at ({x}, {y}, {w}, {h})."
                    self.alert_log_area.insert(tk.END, alert_message + "\n")

                # If recording, write the frame to the output file
                if self.recording:
                    self.out.write(frame)

                # Convert BGR frame to RGB for displaying
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.root.after(10, self.show_frame)

class LoginSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EPA-Login")
        self.root.geometry("500x500")
        self.root.config(bg="#2E2F5B")  # Background color set to #2E2F5B

        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root, bg="#2E2F5B")
        login_frame.grid(row=0, column=0, padx=20, pady=20)

        image_path = os.path.join("images", "login_image.png")  # Adjust the image name as per your file
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(login_frame, image=self.image_tk, bg="#2E2F5B")
        self.image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=10)

        Label(login_frame, text="Login", font=("Helvetica", 22, "bold"), bg="#2E2F5B", fg="#F4D35E").grid(row=0, column=1, pady=10)
        Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=1, column=1, sticky="w", pady=5)
        self.username_entry = Entry(login_frame, font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=3, column=1, sticky="w", pady=5)
        self.password_entry = Entry(login_frame, show="*", font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        self.login_button = Button(login_frame, text="Login", command=self.login, font=("Helvetica", 14), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.login_button.grid(row=5, column=1, pady=20, ipadx=10, ipady=5)

        self.signup_button = Button(login_frame, text="Don't have an account? Signup", command=self.show_signup_screen, font=("Helvetica", 10), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.signup_button.grid(row=6, column=1, pady=10)

    def show_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        signup_frame = tk.Frame(self.root, bg="#2E2F5B")
        signup_frame.grid(row=0, column=0, padx=20, pady=20)

        image_path = os.path.join("images", "login_image.png")
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(signup_frame, image=self.image_tk, bg="#2E2F5B")
        self.image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=10)

        Label(signup_frame, text="Signup", font=("Helvetica", 22, "bold"), bg="#2E2F5B", fg="#F4D35E").grid(row=0, column=1, pady=10)
        Label(signup_frame, text="Choose Username:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=1, column=1, sticky="w", pady=5)
        self.username_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        Label(signup_frame, text="Create Password:", font=("Helvetica", 12), bg="#2E2F5B", fg="#F4D35E").grid(row=3, column=1, sticky="w", pady=5)
        self.password_entry = Entry(signup_frame, show="*", font=("Helvetica", 12), bg="#FAF0CA", fg="#000000", relief="flat", bd=2)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10)

        self.signup_button = Button(signup_frame, text="Signup", command=self.signup, font=("Helvetica", 14), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.signup_button.grid(row=5, column=1, pady=20, ipadx=10, ipady=5)

        self.back_button = Button(signup_frame, text="Back to Login", command=self.show_login_screen, font=("Helvetica", 10), bg="#505581", fg="white", activebackground="#43496C", activeforeground="white", relief="flat")
        self.back_button.grid(row=6, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # hardcoded username and password
        if username == "admin" and password == "admin":
            self.clear_frame()
            ProctoringApp(self.root)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users_db:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users_db[username] = password
            messagebox.showinfo("Success", "Signup successful! You can now log in.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupApp(root)
    root.mainloop()
