import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
import pandas as pd

def int_from_img(filename):
    """Read an image, calculate and return its luminance as a grayscale image."""
    try:
        # Use open() to handle network path issues
        with open(filename, 'rb') as f:
            img_array = np.asarray(bytearray(f.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Could not read the image. Please ensure the file is a valid image format and path.")

        # Calculate luminance using weighted sum of RGB channels
        luminance = 0.299 * img[:, :, 2] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 0]
        
        return luminance

    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def select_file():
    """Open a file dialog to select an image file and process it for luminance."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    
    if file_path:
        luminance = int_from_img(file_path)
        if luminance is not None:
            print("Luminance calculation successful.")
            return luminance
        else:
            print("Error: Unable to process the selected file.")
            return None
    else:
        print("No file selected.")
        return None

def save_luminance_profile(dataframe):
    """Open a file dialog to select the output location for the luminance profile spreadsheet."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Luminance Profile"
    )
    if file_path:
        dataframe.to_excel(file_path, index=False)
        print(f"Luminance values saved to '{file_path}' as an Excel file.")
    else:
        print("No save location selected.")

def plot_luminance_y_profile(luminance):
    """Plot the luminance values along the Y-coordinate for the X-coordinate of maximum luminance."""
    # Find the (x, y) coordinates of the maximum luminance value
    max_lum_coords = np.unravel_index(np.argmax(luminance, axis=None), luminance.shape)
    max_x = max_lum_coords[1]  # X-coordinate of maximum luminance

    # Extract luminance values along this X-coordinate
    y_coords = np.arange(luminance.shape[0])  # Y-coordinates (vertical positions)
    luminance_values = luminance[:, max_x]     # Luminance values along the selected X-coordinate

    # Filter out zero luminance values for plotting
    non_zero_y_coords = y_coords[luminance_values > 0]
    non_zero_luminance_values = luminance_values[luminance_values > 0]

    # Convert Y-coordinates to relative coordinates (minimum Y becomes 0)
    relative_y_coords = non_zero_y_coords - non_zero_y_coords.min()

    # Save luminance values to a spreadsheet with relative Y-coordinates
    data = {"Relative Y-coordinate": relative_y_coords, "Luminance Value": non_zero_luminance_values}
    df = pd.DataFrame(data)
    save_luminance_profile(df)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(relative_y_coords, non_zero_luminance_values, marker='o', linestyle='-')
    plt.xlabel("Relative Y-coordinate")
    plt.ylabel("Luminance Value")
    plt.title(f"Luminance Profile Along X = {max_x}")
    plt.grid()
    plt.savefig("luminance_profile.svg", format="svg")
    print("Graph saved as 'luminance_profile.svg' in SVG format.")
    plt.show()

# Run the file selection, processing, and plotting
luminance_result = select_file()
if luminance_result is not None:
    plot_luminance_y_profile(luminance_result)
