import os
import cv2
import glob
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def create_timelapse(image_folder, output_video_path, fps=30):
    image_paths = glob.glob(os.path.join(image_folder, '*.bmp'))
    image_paths.sort()

    if not image_paths:
        messagebox.showerror("Error", "No BMP images found in the directory.")
        return

    first_image_path = image_paths[0]
    first_image = cv2.imdecode(np.fromfile(first_image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    if first_image is None:
        messagebox.showerror("Error", f"Failed to read the image file: {first_image_path}")
        return
    
    height, width, layers = first_image.shape
    size = (width, height)

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for image_path in image_paths:
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            messagebox.showerror("Error", f"Failed to read the image file: {image_path}")
            return
        out.write(img)
    
    out.release()
    messagebox.showinfo("Success", f"Timelapse video saved as {output_video_path}")

def select_image_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        image_folder_entry.delete(0, tk.END)
        image_folder_entry.insert(0, folder_selected)
        # Automatically set output file name based on folder name
        folder_name = os.path.basename(folder_selected)
        default_output_path = os.path.join(folder_selected, f"{folder_name}.avi")
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, default_output_path)

def select_output_file():
    file_selected = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi"), ("All files", "*.*")])
    if file_selected:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_selected)

def create_timelapse_from_gui():
    image_folder = image_folder_entry.get()
    output_video_path = output_file_entry.get()
    try:
        fps = int(fps_entry.get())
    except ValueError:
        messagebox.showerror("Error", "FPS must be an integer.")
        return

    if not os.path.exists(image_folder):
        messagebox.showerror("Error", "Image folder does not exist.")
        return

    if not output_video_path:
        messagebox.showerror("Error", "Output video path cannot be empty.")
        return

    create_timelapse(image_folder, output_video_path, fps)

# GUI Setup
root = tk.Tk()
root.title("Timelapse Creator")

# Input Fields
tk.Label(root, text="Image Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
image_folder_entry = tk.Entry(root, width=50)
image_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_image_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="FPS:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
fps_entry = tk.Entry(root, width=10)
fps_entry.insert(0, "30")
fps_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Button(root, text="Create Timelapse", command=create_timelapse_from_gui).grid(row=3, column=1, pady=20)

root.mainloop()
