import os
import subprocess
import sys

def build_executable(script_path, output_name=None, add_data=None, windowed=True):
    """
    指定されたPythonスクリプトを実行可能ファイルにパッケージ化します。

    Args:
        script_path (str): パッケージ化するPythonスクリプトのパス。
        output_name (str): 出力実行可能ファイルの名前（省略可能）。
        add_data (list): 含める追加データ（例: ["source_path;destination_path"]）。
        windowed (bool): GUIモードでパッケージ化する場合はTrue。
    """
    # 必要なオプションを組み立て
    options = ["pyinstaller", "--onefile"]

    if windowed:
        options.append("--windowed")

    if output_name:
        options.extend(["--name", output_name])

    if add_data:
        for data in add_data:
            options.extend(["--add-data", data])

    options.append(script_path)

    # PyInstallerを実行
    try:
        print("ビルド開始...")
        subprocess.run(options, check=True)
        print("ビルド完了: dist フォルダを確認してください。")
    except subprocess.CalledProcessError as e:
        print(f"ビルド中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # パッケージ化対象スクリプト
    script_to_package = "gui_brightness_histogram.py"

    # 出力実行可能ファイル名
    executable_name = "BrightnessHistogramApp"

    # 追加データ（フォントなど）
    additional_data = [
        "C:/Windows/Fonts/meiryo.ttc;."
    ]

    # 実行可能ファイルをビルド
    build_executable(
        script_path=script_to_package,
        output_name=executable_name,
        add_data=additional_data,
        windowed=True
    )
