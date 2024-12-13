import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import csv
import os

def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    if file_path:
        image_path.set(file_path)

def extract_brightness():
    try:
        x_coord = int(x_entry.get())
        image_path_val = image_path.get()

        if not os.path.exists(image_path_val):
            messagebox.showerror("Error", "Selected image file does not exist.")
            return

        # Open image and extract brightness
        img = Image.open(image_path_val).convert("L")  # Convert to grayscale
        width, height = img.size

        if x_coord < 0 or x_coord >= width:
            messagebox.showerror("Error", f"x-coordinate out of bounds (0-{width - 1}).")
            return

        # Extract brightness values with y-coordinates
        data = [("y", "Brightness")]  # Add header row
        data += [(y, img.getpixel((x_coord, y))) for y in range(height)]

        # Save to CSV
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
        )
        if save_path:
            with open(save_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            messagebox.showinfo("Success", f"Brightness values saved to {save_path}")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for the x-coordinate.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("Brightness Extractor")

image_path = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Image selection
tk.Label(frame, text="Select Image:").grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(frame, textvariable=image_path, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Browse", command=select_image).grid(row=0, column=2, pady=5)

# X-coordinate entry
tk.Label(frame, text="X-Coordinate:").grid(row=1, column=0, sticky="e", pady=5)
x_entry = tk.Entry(frame, width=10)
x_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

# Extract and Save Button
tk.Button(frame, text="Extract Brightness", command=extract_brightness).grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
