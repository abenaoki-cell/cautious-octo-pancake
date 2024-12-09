# ファイル名: gui_brightness_histogram.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# フォント設定（日本語対応）
try:
    jp_font = FontProperties(fname="C:/Windows/Fonts/meiryo.ttc")  # Windowsの場合
    rcParams['font.family'] = jp_font.get_name()
except Exception as e:
    print("フォント設定に失敗しました。デフォルトフォントを使用します。", e)

def calculate_average_brightness(image_path: str) -> float:
    try:
        img = Image.open(image_path).convert('L')  # グレースケールに変換
        img_array = np.array(img)
        avg_brightness = img_array.mean()
        return avg_brightness
    except Exception as e:
        messagebox.showerror("エラー", f"画像処理中にエラーが発生しました: {e}")
        return -1

def plot_histogram(image_path: str):
    try:
        img = Image.open(image_path).convert('L')  # グレースケールに変換
        img_array = np.array(img)
        hist, bins = np.histogram(img_array, bins=256, range=(0, 256))

        # プロット
        fig = plt.Figure(figsize=(6, 4), dpi=100)  # サイズ調整
        ax = fig.add_subplot(111)
        ax.bar(bins[:-1], hist, width=1, color='dodgerblue', edgecolor='black', alpha=0.7)
        ax.set_title("明るさヒストグラム", fontproperties=jp_font, fontsize=16)
        ax.set_xlabel("輝度値 (0-255)", fontproperties=jp_font, fontsize=12)
        ax.set_ylabel("ピクセル数", fontproperties=jp_font, fontsize=12)
        ax.grid(visible=True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.set_facecolor('#f5f5f5')
        fig.tight_layout()
        return fig
    except Exception as e:
        messagebox.showerror("エラー", f"ヒストグラム作成中にエラーが発生しました: {e}")
        return None

def select_image():
    file_path = filedialog.askopenfilename(
        title="画像を選択してください",
        filetypes=[("画像ファイル", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((300, 300))  # 表示用に画像サイズを縮小
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk

            avg_brightness = calculate_average_brightness(file_path)
            if avg_brightness != -1:
                result_label.config(text=f"平均輝度: {avg_brightness:.2f}")

            global current_figure  # グローバル変数でヒストグラムを保存
            current_figure = plot_histogram(file_path)
            if current_figure:
                for widget in histogram_frame.winfo_children():
                    widget.destroy()

                canvas = FigureCanvasTkAgg(current_figure, master=histogram_frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack()
                canvas.draw()
        except Exception as e:
            messagebox.showerror("エラー", f"画像の読み込みに失敗しました: {e}")

def export_histogram():
    """
    現在のヒストグラムを画像として保存します。
    """
    if current_figure is None:
        messagebox.showwarning("警告", "エクスポートするヒストグラムがありません。")
        return

    file_path = filedialog.asksaveasfilename(
        title="ヒストグラムを保存",
        defaultextension=".png",
        filetypes=[("PNGファイル", "*.png"), ("JPEGファイル", "*.jpg"), ("すべてのファイル", "*.*")]
    )
    if file_path:
        try:
            current_figure.savefig(file_path, format=file_path.split('.')[-1])
            messagebox.showinfo("成功", f"ヒストグラムを保存しました: {file_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"ヒストグラムの保存中にエラーが発生しました: {e}")

# GUIアプリケーションのセットアップ
root = tk.Tk()
root.title("画像の平均輝度とヒストグラム")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

select_button = tk.Button(frame, text="画像を選択", command=select_image)
select_button.grid(row=0, column=0, pady=10)

image_label = tk.Label(frame, text="画像がここに表示されます", width=40, height=15, bg="gray")
image_label.grid(row=1, column=0, pady=10)

result_label = tk.Label(frame, text="平均輝度: -", font=("Arial", 14))
result_label.grid(row=2, column=0, pady=10)

export_button = tk.Button(frame, text="ヒストグラムをエクスポート", command=export_histogram)
export_button.grid(row=3, column=0, pady=10)

histogram_frame = tk.Frame(root)
histogram_frame.pack(pady=10)

current_figure = None  # グローバル変数でヒストグラムを保持

root.mainloop()
