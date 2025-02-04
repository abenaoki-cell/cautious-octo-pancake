import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        image_folder_path.set(folder_path)

def select_save_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        save_folder_path.set(folder_path)

def extract_and_save_cropped_images():
    try:
        # 座標と矩形サイズの入力処理
        x_coord = int(x_entry.get().strip())
        y_coord = int(y_entry.get().strip())
        rect_width = int(width_entry.get().strip())
        rect_height = int(height_entry.get().strip())
        folder_path_val = image_folder_path.get()
        save_folder_val = save_folder_path.get()

        if not os.path.exists(folder_path_val):
            messagebox.showerror("Error", "選択されたフォルダが存在しません。")
            return

        if not save_folder_val:
            messagebox.showerror("Error", "保存先のフォルダを選択してください。")
            return

        if not os.path.exists(save_folder_val):
            os.makedirs(save_folder_val)  # 保存フォルダを作成

        image_files = [f for f in os.listdir(folder_path_val) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))]
        if not image_files:
            messagebox.showerror("Error", "選択されたフォルダに画像ファイルが見つかりません。")
            return

        for image_file in image_files:
            image_path = os.path.join(folder_path_val, image_file)
            img = Image.open(image_path)
            width, height = img.size

            # 入力範囲が画像サイズを超えていないかチェック
            if not (0 <= x_coord < width and 0 <= y_coord < height):
                messagebox.showwarning("Warning", f"{image_file}をスキップ: 指定された座標が画像範囲外です。")
                continue
            if x_coord + rect_width > width or y_coord + rect_height > height:
                messagebox.showwarning("Warning", f"{image_file}をスキップ: 矩形範囲が画像の範囲外です。")
                continue

            # 画像を切り抜いて保存
            cropped_img = img.crop((x_coord, y_coord, x_coord + rect_width, y_coord + rect_height))
            save_path = os.path.join(save_folder_val, f"cropped_{image_file}")
            cropped_img.save(save_path)

        messagebox.showinfo("Success", f"画像が{save_folder_val}に保存されました。")

    except ValueError:
        messagebox.showerror("Error", "座標および矩形のサイズには有効な数値を入力してください。")
    except Exception as e:
        messagebox.showerror("Error", f"予期しないエラーが発生しました: {e}")

# GUI Setup
root = tk.Tk()
root.title("Rectangle Image Cropper")

image_folder_path = tk.StringVar()
save_folder_path = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# フォルダ選択
tk.Label(frame, text="Select Image Folder:").grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(frame, textvariable=image_folder_path, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Browse", command=select_folder).grid(row=0, column=2, pady=5)

# 保存先フォルダ選択
tk.Label(frame, text="Select Save Folder:").grid(row=1, column=0, sticky="e", pady=5)
tk.Entry(frame, textvariable=save_folder_path, width=40).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Browse", command=select_save_folder).grid(row=1, column=2, pady=5)

# X座標入力
tk.Label(frame, text="X-Coordinate:").grid(row=2, column=0, sticky="e", pady=5)
x_entry = tk.Entry(frame, width=30)
x_entry.grid(row=2, column=1, padx=5, pady=5)

# Y座標入力
tk.Label(frame, text="Y-Coordinate:").grid(row=3, column=0, sticky="e", pady=5)
y_entry = tk.Entry(frame, width=30)
y_entry.grid(row=3, column=1, padx=5, pady=5)

# 幅入力
tk.Label(frame, text="Rectangle Width:").grid(row=4, column=0, sticky="e", pady=5)
width_entry = tk.Entry(frame, width=30)
width_entry.grid(row=4, column=1, padx=5, pady=5)

# 高さ入力
tk.Label(frame, text="Rectangle Height:").grid(row=5, column=0, sticky="e", pady=5)
height_entry = tk.Entry(frame, width=30)
height_entry.grid(row=5, column=1, padx=5, pady=5)

# 抽出と保存ボタン
tk.Button(frame, text="Extract and Save Cropped Images", command=extract_and_save_cropped_images).grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
