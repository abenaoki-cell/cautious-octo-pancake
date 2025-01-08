import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import openpyxl
from openpyxl.utils import get_column_letter

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        image_folder_path.set(folder_path)

def extract_brightness():
    try:
        x_coords = x_entry.get().split(',')
        x_coords = [int(x.strip()) for x in x_coords]
        folder_path_val = image_folder_path.get()

        if not os.path.exists(folder_path_val):
            messagebox.showerror("Error", "Selected folder does not exist.")
            return

        image_files = [f for f in os.listdir(folder_path_val) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))]
        if not image_files:
            messagebox.showerror("Error", "No image files found in the selected folder.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
        )
        if not save_path:
            return

        workbook = openpyxl.Workbook()
        workbook.remove(workbook.active)  # Remove the default sheet

        for image_file in image_files:
            image_path = os.path.join(folder_path_val, image_file)
            img = Image.open(image_path).convert("L")  # Convert to grayscale
            width, height = img.size

            valid_x_coords = [x for x in x_coords if 0 <= x < width]
            if not valid_x_coords:
                messagebox.showwarning("Warning", f"Skipping {image_file}: No valid x-coordinates within image bounds.")
                continue

            sheet = workbook.create_sheet(title=os.path.splitext(image_file)[0])
            sheet.append(["y"] + [f"x={x}" for x in valid_x_coords])

            for y in range(height):
                row = [y] + [img.getpixel((x, y)) for x in valid_x_coords]
                sheet.append(row)

            # Auto-adjust column width
            for col_num, _ in enumerate(sheet.iter_cols(), 1):
                column_width = max(len(str(cell.value)) for cell in sheet[get_column_letter(col_num)])
                sheet.column_dimensions[get_column_letter(col_num)].width = column_width + 2

        workbook.save(save_path)
        messagebox.showinfo("Success", f"Brightness values saved to {save_path}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for the x-coordinates.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("Batch Brightness Extractor for Folder")

image_folder_path = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Folder selection
tk.Label(frame, text="Select Folder:").grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(frame, textvariable=image_folder_path, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Browse", command=select_folder).grid(row=0, column=2, pady=5)

# X-coordinates entry
tk.Label(frame, text="X-Coordinates (comma-separated):").grid(row=1, column=0, sticky="e", pady=5)
x_entry = tk.Entry(frame, width=30)
x_entry.grid(row=1, column=1, padx=5, pady=5)

# Extract and Save Button
tk.Button(frame, text="Extract Brightness", command=extract_brightness).grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
