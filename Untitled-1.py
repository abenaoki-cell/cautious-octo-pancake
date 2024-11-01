# -*- coding: utf-8 -*-
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar
from PIL import Image

# 画像パスと、左上座標、右下座標を指定して、トリミングされたimageオブジェクトを返す。
def trim(path, left, top, right, bottom):
    im = Image.open(path)
    im_trimmed = im.crop((left, top, right, bottom))
    return im_trimmed

# トリミング処理を実行する関数
def process_images():
    try:
        # 入力値を取得
        left = int(left_entry.get())
        top = int(top_entry.get())
        right = int(right_entry.get())
        bottom = int(bottom_entry.get())

        # ディレクトリのチェック
        if not os.path.isdir(input_dir.get()):
            messagebox.showerror("エラー", "入力ディレクトリが見つかりません。")
            return

        if not os.path.isdir(output_dir.get()):
            os.makedirs(output_dir.get())

        # 画像ファイルのフィルタリング
        files = os.listdir(input_dir.get())
        files = [name for name in files if name.split(".")[-1].lower() in ["png", "jpg", "bmp"]]

        # トリミング処理
        for val in files:
            path = os.path.join(input_dir.get(), val)
            im_trimmed = trim(path, left, top, right, bottom)
            im_trimmed.save(os.path.join(output_dir.get(), "cut_" + val), quality=95)
        
        messagebox.showinfo("完了", "すべての画像がトリミングされました。")

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました: {e}")

# 入力ディレクトリを選択
def select_input_dir():
    directory = filedialog.askdirectory()
    if directory:
        input_dir.set(directory)

# 出力ディレクトリを選択
def select_output_dir():
    directory = filedialog.askdirectory()
    if directory:
        output_dir.set(directory)

# GUIのセットアップ
root = Tk()
root.title("画像トリミングツール")

# StringVarオブジェクトを使用してディレクトリパスを保持
input_dir = StringVar()
output_dir = StringVar()

# ラベルとボタン
Label(root, text="入力ディレクトリ:").grid(row=0, column=0, padx=5, pady=5)
Entry(root, textvariable=input_dir, width=40).grid(row=0, column=1, padx=5, pady=5)
Button(root, text="参照", command=select_input_dir).grid(row=0, column=2, padx=5, pady=5)

Label(root, text="出力ディレクトリ:").grid(row=1, column=0, padx=5, pady=5)
Entry(root, textvariable=output_dir, width=40).grid(row=1, column=1, padx=5, pady=5)
Button(root, text="参照", command=select_output_dir).grid(row=1, column=2, padx=5, pady=5)

Label(root, text="左 (X):").grid(row=2, column=0, padx=5, pady=5)
left_entry = Entry(root)
left_entry.grid(row=2, column=1, padx=5, pady=5)

Label(root, text="上 (Y):").grid(row=3, column=0, padx=5, pady=5)
top_entry = Entry(root)
top_entry.grid(row=3, column=1, padx=5, pady=5)

Label(root, text="右 (X):").grid(row=4, column=0, padx=5, pady=5)
right_entry = Entry(root)
right_entry.grid(row=4, column=1, padx=5, pady=5)

Label(root, text="下 (Y):").grid(row=5, column=0, padx=5, pady=5)
bottom_entry = Entry(root)
bottom_entry.grid(row=5, column=1, padx=5, pady=5)

Button(root, text="実行", command=process_images).grid(row=6, column=1, padx=5, pady=5)

# GUI開始
root.mainloop()
