import cv2
import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class TimelapseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timelapse Capture")

        self.capture_interval = tk.DoubleVar()
        self.waiting_time = tk.IntVar()
        self.width = tk.IntVar()
        self.height = tk.IntVar()

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

        tk.Button(self.root, text="Start Capture", command=self.start_capture).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Exit", command=self.root.quit).grid(row=5, column=0, columnspan=2)

    def start_capture(self):
        capture_interval = self.capture_interval.get()
        waiting_time = self.waiting_time.get()
        width = self.width.get()
        height = self.height.get()

        if not capture_interval or not waiting_time or not width or not height:
            messagebox.showerror("Error", "All fields must be filled with valid numbers")
            return

        date = self.create_directory()
        self.capture_thread = threading.Thread(target=self.capture_images, args=(date, capture_interval, width, height))
        self.capture_thread.start()

    def create_directory(self):
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(date):
            os.mkdir(date)
        return date

    def capture_images(self, date, capture_interval, width, height):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return

        start_time = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image.")
                break

            frame = cv2.resize(frame, (width, height))
            cv2.imshow("Camera", frame)

            date_time = datetime.now().strftime("%Y%m%d%H%M%S")
            path = f"./{date}/{date_time}.bmp"
            cv2.imwrite(path, frame)

            elapsed_time = time.time() - start_time
            if elapsed_time < capture_interval:
                time.sleep(capture_interval - elapsed_time)
            start_time = time.time()

            if cv2.waitKey(1) & 0xFF == 13:  # Enter key to stop
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimelapseApp(root)
    root.mainloop()
