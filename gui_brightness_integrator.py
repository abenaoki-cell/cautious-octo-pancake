# file path: gui_brightness_integrator.py
import openpyxl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def process_excel():
    # ファイル選択ダイアログでExcelファイルを選択
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx")]
    )
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    def calculate_and_save():
        try:
            # 寸法入力を取得
            x_dim = float(x_dim_entry.get())
            y_dim = float(y_dim_entry.get())
            if x_dim <= 0 or y_dim <= 0:
                raise ValueError("Dimensions must be positive values.")

            # Excelファイルを読み込み
            workbook = openpyxl.load_workbook(file_path)
            results = []

            # 各シートの積分計算
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                if sheet.max_row < 2 or sheet.max_column < 2:
                    continue  # データがないシートはスキップ

                total_area = 0  # 面積積分の合計
                for row in sheet.iter_rows(min_row=2, min_col=2, values_only=True):
                    for brightness in row:
                        if brightness is not None:
                            total_area += brightness * (x_dim * y_dim)

                results.append((sheet_name, total_area))

            # 結果を新しいワークブックに保存
            output_workbook = openpyxl.Workbook()
            output_sheet = output_workbook.active
            output_sheet.title = "Integrated Results"
            output_sheet.append(["Sheet Name", "Integrated Brightness (mm^2)"])

            for name, area in results:
                output_sheet.append([name, area])

            # 保存ダイアログを表示
            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
            )
            if not save_path:
                return
            output_workbook.save(save_path)
            messagebox.showinfo("Success", f"Results saved to {save_path}")
            root.destroy()

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # 寸法入力用のGUIウィンドウを作成
    root = tk.Tk()
    root.title("Dimension Input")

    tk.Label(root, text="Enter Dimensions (mm/pixel)").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="X Dimension:").grid(row=1, column=0, sticky="e", padx=5)
    x_dim_entry = ttk.Entry(root, width=20)
    x_dim_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Y Dimension:").grid(row=2, column=0, sticky="e", padx=5)
    y_dim_entry = ttk.Entry(root, width=20)
    y_dim_entry.grid(row=2, column=1, padx=5, pady=5)

    calculate_button = ttk.Button(root, text="Calculate and Save", command=calculate_and_save)
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    process_excel()
