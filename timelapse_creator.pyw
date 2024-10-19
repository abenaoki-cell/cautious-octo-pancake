import os
import cv2
import glob
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def create_timelapse(image_folder, output_video_path, fps=30):
    # BMP画像のパスを取得
    image_paths = glob.glob(os.path.join(image_folder, '*.bmp'))
    image_paths.sort()  # 画像をソート

    # 画像が存在しない場合の処理
    if not image_paths:
        messagebox.showerror("Error", "No BMP images found in the directory.")
        return

    # 最初の画像を読み込み、動画のサイズを取得
    first_image_path = image_paths[0]
    first_image = cv2.imdecode(np.fromfile(first_image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    if first_image is None:
        messagebox.showerror("Error", f"Failed to read the image file: {first_image_path}")
        return
    
    height, width, layers = first_image.shape
    size = (width, height)

    # 動画ファイルを作成
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for image_path in image_paths:
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            messagebox.showerror("Error", f"Failed to read the image file: {image_path}")
            return
        out.write(img)  # 動画にフレームとして追加

    out.release()
    messagebox.showinfo("Success", f"Timelapse video saved as {output_video_path}")

def select_image_folder():
    folder_selected = filedialog.askdirectory()
    image_folder_entry.delete(0, tk.END)
    image_folder_entry.insert(0, folder_selected)

def select_output_file():
    file_selected = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi"), ("All files", "*.*")])
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

    create_timelapse(image_folder, output_video_path, fps)

# GUIのセットアップ
root = tk.Tk()
root.title("Timelapse Creator")

tk.Label(root, text="BMP Image Folder:").grid(row=0, column=0, padx=10, pady=10)
image_folder_entry = tk.Entry(root, width=50)
image_folder_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_image_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Output Video Path:").grid(row=1, column=0, padx=10, pady=10)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="FPS:").grid(row=2, column=0, padx=10, pady=10)
fps_entry = tk.Entry(root, width=10)
fps_entry.grid(row=2, column=1, padx=10, pady=10)
fps_entry.insert(0, "30")

tk.Button(root, text="Create Timelapse", command=create_timelapse_from_gui).grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()
