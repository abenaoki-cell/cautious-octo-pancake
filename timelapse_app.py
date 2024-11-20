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

        self.capture_interval = tk.DoubleVar(value=1.0)
        self.waiting_time = tk.IntVar(value=5)
        self.width = tk.IntVar(value=2592)
        self.height = tk.IntVar(value=1944)
        self.save_directory = tk.StringVar(value=os.getcwd())
        self.capturing = False
        self.capture_thread = None

        self.create_widgets()

    def create_widgets(self):
        inputs = [("Capture Interval (sec):", self.capture_interval),
                  ("Waiting Time (sec):", self.waiting_time),
                  ("Image Width:", self.width),
                  ("Image Height:", self.height),
                  ("Save Directory:", self.save_directory)]
        for i, (label, var) in enumerate(inputs):
            self.create_input(label, var, i)

        tk.Button(self.root, text="Select Folder", command=self.select_directory).grid(row=4, column=2)
        tk.Button(self.root, text="Start Capture", command=self.start_capture).grid(row=5, column=0)
        tk.Button(self.root, text="Stop Capture", command=self.stop_capture).grid(row=5, column=1)
        tk.Button(self.root, text="Exit", command=self.cleanup).grid(row=6, column=0, columnspan=2)

        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.grid(row=7, column=0, columnspan=3)

    def create_input(self, label_text, variable, row):
        tk.Label(self.root, text=label_text).grid(row=row, column=0)
        tk.Entry(self.root, textvariable=variable).grid(row=row, column=1)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory.set(directory)

    def start_capture(self):
        inputs = self.validate_inputs()
        if not inputs:
            return
        capture_interval, waiting_time, width, height = inputs
        cap = self.init_camera()
        if not cap:
            return

        self.capturing = True
        self.capture_thread = threading.Thread(
            target=self.capture_images, args=(cap, capture_interval, waiting_time, width, height), daemon=True
        )
        self.capture_thread.start()

    def stop_capture(self):
        self.capturing = False
        self.update_status("Stopping capture...")

    def init_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return None
        return cap

    def capture_images(self, cap, interval, waiting_time, width, height):
        save_dir = os.path.join(self.save_directory.get(), datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(save_dir, exist_ok=True)

        time.sleep(waiting_time)

        try:
            while self.capturing:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (width, height))
                filename = os.path.join(save_dir, f"{datetime.now().strftime('%Y%m%d%H%M%S')}.bmp")
                self.save_image(frame, filename)
                cv2.imshow("Preview", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    self.stop_capture()
                    break
                time.sleep(interval)
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.update_status("Capture completed.")

    def save_image(self, frame, path):
        success, buffer = cv2.imencode('.bmp', frame)
        if success:
            with open(path, 'wb') as f:
                f.write(buffer)

    def validate_inputs(self):
        try:
            return (
                float(self.capture_interval.get()),
                int(self.waiting_time.get()),
                int(self.width.get()),
                int(self.height.get()),
            )
        except ValueError:
            messagebox.showerror("Error", "Invalid inputs.")
            return None

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def cleanup(self):
        self.stop_capture()
        cv2.destroyAllWindows()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimelapseApp(root)
    root.mainloop()
