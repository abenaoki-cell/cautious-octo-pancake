import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def calculate_area_integral(input_file: str, output_file: str):
    try:
        # Excelファイルを読み込み
        excel_data = pd.ExcelFile(input_file)

        # 結果を格納するリスト
        integration_results = []

        # 各シートについて処理
        for sheet_name in excel_data.sheet_names:
            # シートデータをデータフレームとして取得
            df = excel_data.parse(sheet_name, header=None)

            # 1行目はX座標、1列目はY座標
            x_coords = df.iloc[0, 1:].astype(float).values  # X座標を取得
            y_coords = df.iloc[1:, 0].astype(float).values  # Y座標を取得
            brightness_values = df.iloc[1:, 1:].astype(float).values  # 輝度値部分

            # 正の輝度値のみ対象にする
            brightness_values[brightness_values <= 0] = 0

            # 2次元積分を実施（台形法）
            area_integral = np.trapz(np.trapz(brightness_values, x=x_coords, axis=1), x=y_coords)

            # 単位面積当たりの平均輝度値を計算
            positive_area = np.trapz(np.trapz(brightness_values > 0, x=x_coords, axis=1), x=y_coords)
            average_brightness = area_integral / positive_area if positive_area > 0 else 0

            # シート名、積分値、平均輝度値を結果に追加
            integration_results.append((sheet_name, area_integral, average_brightness))

        # 結果をデータフレームとして整形
        result_df = pd.DataFrame(integration_results, columns=["Sheet Name", "Area Integral", "Average Brightness"])

        # 結果を新しいExcelファイルとして保存
        result_df.to_excel(output_file, index=False)
        messagebox.showinfo("成功", "積分結果を保存しました。")

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")

def select_input_file():
    input_file = filedialog.askopenfilename(
        title="入力ファイルを選択",
        filetypes=[("Excelファイル", "*.xlsx;*.xls")]
    )
    if input_file:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, input_file)

def select_output_file():
    output_file = filedialog.asksaveasfilename(
        title="出力ファイルを保存",
        defaultextension=".xlsx",
        filetypes=[("Excelファイル", "*.xlsx")]
    )
    if output_file:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, output_file)

def start_processing():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    if not input_file or not output_file:
        messagebox.showwarning("警告", "入力ファイルと出力ファイルを指定してください。")
        return

    calculate_area_integral(input_file, output_file)

# GUIの設定
root = tk.Tk()
root.title("Excel 面積積分ツール")

# ファイル選択部分
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# 入力ファイル選択
tk.Label(frame, text="入力ファイル:").grid(row=0, column=0, sticky="w")
input_file_entry = tk.Entry(frame, width=50)
input_file_entry.grid(row=0, column=1, padx=5)
input_file_button = tk.Button(frame, text="選択", command=select_input_file)
input_file_button.grid(row=0, column=2)

# 出力ファイル選択
tk.Label(frame, text="出力ファイル:").grid(row=1, column=0, sticky="w")
output_file_entry = tk.Entry(frame, width=50)
output_file_entry.grid(row=1, column=1, padx=5)
output_file_button = tk.Button(frame, text="保存", command=select_output_file)
output_file_button.grid(row=1, column=2)

# 実行ボタン
process_button = tk.Button(root, text="積分計算開始", command=start_processing, bg="lightblue")
process_button.pack(pady=10)

# メインループの開始
root.mainloop()
