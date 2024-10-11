import cv2
import os
import time  # Import the time module
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk


class TimelapseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timelapse Capture")

        self.capture_interval = tk.DoubleVar()
        self.waiting_time = tk.IntVar()
        self.width = tk.IntVar()
        self.height = tk.IntVar()
        self.frame_rate = tk.IntVar(value=10)  # Default frame rate

        self.stop_capture_flag = threading.Event()

        # Store the directory name for captured images
        self.images_folder = None

        # Initialize capture_thread as None to avoid AttributeError
        self.capture_thread = None

        # Initialize camera variable
        self.cap = None

        # Variable to hold remaining countdown time
        self.remaining_time = 0

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Capture Interval (seconds):").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.capture_interval).grid(row=0, column=1)

        tk.Label(self.root, text="Waiting Time (seconds):").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.waiting_time).grid(row=1, column=1)

        tk.Label(self.root, text="Image Width:").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.width).grid(row=2, column=1)

        tk.Label(self.root, text="Image Height:").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.height).grid(row=3, column=1)

        tk.Label(self.root, text="Frame Rate (fps):").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.frame_rate).grid(row=4, column=1)

        self.countdown_label = tk.Label(self.root, text="")
        self.countdown_label.grid(row=5, column=0, columnspan=2)

        tk.Button(self.root, text="Start Capture", command=self.start_camera_warmup).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Stop Capture", command=self.stop_capture).grid(row=7, column=0, columnspan=2)
        tk.Button(self.root, text="Preview Timelapse", command=self.preview_timelapse).grid(row=8, column=0, columnspan=2)
        tk.Button(self.root, text="Exit", command=self.on_exit).grid(row=9, column=0, columnspan=2)

    def start_camera_warmup(self):
        """Start the camera to allow warmup during the waiting time."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return

        # Set the remaining time to the waiting time value and start countdown
        self.remaining_time = self.waiting_time.get()
        if self.remaining_time <= 0:
            messagebox.showerror("Error", "Please provide a valid waiting time.")
            return

        # Start the countdown
        self.update_countdown()

    def update_countdown(self):
        """Show the countdown timer while camera warms up."""
        if self.remaining_time > 0:
            self.countdown_label.config(text=f"Starting in {self.remaining_time} seconds...")
            self.remaining_time -= 1
            self.root.after(1000, self.update_countdown)  # Update every second
        else:
            self.countdown_label.config(text="Starting capture now!")
            self.start_capture()

    def start_capture(self):
        """Start the image capture process after the waiting time has passed."""
        capture_interval = self.capture_interval.get()
        width = self.width.get()
        height = self.height.get()
        frame_rate = self.frame_rate.get()

        if not capture_interval or not width or not height or not frame_rate:
            messagebox.showerror("Error", "All fields must be filled with valid numbers")
            return

        self.images_folder = self.create_directory()

        self.stop_capture_flag.clear()

        self.capture_thread = threading.Thread(
            target=self.capture_images, args=(self.images_folder, capture_interval, width, height))
        self.capture_thread.start()

    def stop_capture(self):
        """Stop the capture process and clean up."""
        self.stop_capture_flag.set()

        # Ensure self.capture_thread is not None before checking if it is alive
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join()

        # Release the camera resource
        if self.cap:
            self.cap.release()

        # After capture ends, create timelapse video
        if self.images_folder:
            self.create_timelapse_video()

    def create_directory(self):
        """Create a new directory to store captured images."""
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = f"./{date}"
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder

    def capture_images(self, images_folder, capture_interval, width, height):
        """Capture images from the camera at regular intervals."""
        start_time = time.time()
        while not self.stop_capture_flag.is_set():
            ret, frame = self.cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image.")
                break

            frame = cv2.resize(frame, (width, height))
            cv2.imshow("Camera", frame)

            date_time = datetime.now().strftime("%Y%m%d%H%M%S")
            path = os.path.join(images_folder, f"{date_time}.bmp")
            cv2.imwrite(path, frame)

            elapsed_time = time.time() - start_time
            if elapsed_time < capture_interval:
                time.sleep(capture_interval - elapsed_time)
            start_time = time.time()

            if cv2.waitKey(1) & 0xFF == 13:  # Enter key to stop
                break

        # Release the camera resource when done
        self.cap.release()
        cv2.destroyAllWindows()

    def create_timelapse_video(self):
        """Create a timelapse video from captured images."""
        images = [img for img in os.listdir(self.images_folder) if img.endswith(".bmp")]

        if not images:
            messagebox.showerror("Error", "No images captured to create a video.")
            return

        images.sort()

        frame = cv2.imread(os.path.join(self.images_folder, images[0]))
        height, width, layers = frame.shape

        # Retrieve the frame rate specified by the user
        frame_rate = self.frame_rate.get()

        video_path = os.path.join(self.images_folder, "timelapse.mp4")
        video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

        for image in images:
            img_path = os.path.join(self.images_folder, image)
            img = cv2.imread(img_path)
            video.write(img)

        video.release()
        messagebox.showinfo("Success", f"Timelapse video created at {video_path}")

    def preview_timelapse(self):
        """Preview the created timelapse video."""
        if not self.images_folder:
            messagebox.showerror("Error", "No timelapse video found.")
            return

        video_path = os.path.join(self.images_folder, "timelapse.mp4")
        if not os.path.exists(video_path):
            messagebox.showerror("Error", "Timelapse video does not exist.")
            return

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video.")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Timelapse Preview", frame)
            if cv2.waitKey(25) & 0xFF == 13:  # Enter key to stop preview
                break

        cap.release()
        cv2.destroyAllWindows()

    def on_exit(self):
        """Handle exiting the application."""
        self.stop_capture()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimelapseApp(root)
    root.mainloop()
