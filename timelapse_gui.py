import cv2
import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

class TimelapseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timelapse Capture")

        # GUI input variables
        self.capture_interval = tk.DoubleVar()
        self.waiting_time = tk.IntVar()
        self.width = tk.IntVar()
        self.height = tk.IntVar()
        self.save_directory = tk.StringVar(value=os.getcwd())  # Default save directory

        self.capturing = threading.Event()  # Thread-safe flag
        self.capture_thread = None

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

        tk.Label(self.root, text="Save Directory:").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.save_directory, state="readonly").grid(row=4, column=1)
        tk.Button(self.root, text="Select Folder", command=self.select_directory).grid(row=4, column=2)

        tk.Button(self.root, text="Start Capture", command=self.start_capture).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Stop Capture", command=self.stop_capture).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Exit", command=self.exit_app).grid(row=7, column=0, columnspan=2)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory.set(directory)

    def start_capture(self):
        try:
            capture_interval = float(self.capture_interval.get())
            waiting_time = int(self.waiting_time.get())
            width = int(self.width.get())
            height = int(self.height.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        if any(value <= 0 for value in [capture_interval, waiting_time, width, height]):
            messagebox.showerror("Error", "Values must be positive.")
            return

        if not self.check_camera():
            messagebox.showerror("Error", "Could not access camera.")
            return

        date_directory = self.create_directory()
        self.capturing.set()  # Start capturing
        self.capture_thread = threading.Thread(
            target=self.capture_images, args=(date_directory, capture_interval, waiting_time, width, height), daemon=True
        )
        self.capture_thread.start()

    def stop_capture(self):
        self.capturing.clear()  # Stop the capture loop
        if self.capture_thread:
            self.capture_thread.join()  # Wait for the thread to finish

    def create_directory(self):
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = os.path.join(self.save_directory.get(), date)
        os.makedirs(directory, exist_ok=True)
        return directory

    def capture_images(self, date_directory, capture_interval, waiting_time, width, height):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return

        # Wait for the specified waiting time before starting the capture loop
        messagebox.showinfo("Info", f"Waiting for {waiting_time} seconds before starting capture.")
        time.sleep(waiting_time)

        try:
            while self.capturing.is_set():
                start_time = time.time()

                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to capture image.")
                    self.stop_capture()
                    break

                frame = cv2.resize(frame, (width, height))
                cv2.imshow("Camera", frame)

                date_time = datetime.now().strftime("%Y%m%d%H%M%S")
                path = os.path.join(date_directory, f"{date_time}.bmp")

                # Save the image with Unicode handling
                cv2.imencode('.bmp', frame)[1].tofile(path)

                elapsed_time = time.time() - start_time
                time_to_sleep = max(0, capture_interval - elapsed_time)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC to stop
                    self.stop_capture()
                    break

                time.sleep(time_to_sleep)

        finally:
            cap.release()
            cv2.destroyAllWindows()

    def check_camera(self):
        cap = cv2.VideoCapture(0)
        is_opened = cap.isOpened()
        cap.release()
        return is_opened

    def exit_app(self):
        self.stop_capture()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimelapseApp(root)
    root.mainloop()
