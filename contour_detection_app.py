import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os
import numpy as np

class ContourApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contour Detection App")

        # GUI Components
        self.label = tk.Label(root, text="Select an image to process:")
        self.label.pack(pady=10)

        self.select_btn = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_btn.pack(pady=5)

        # Sliders for parameters
        self.threshold_label = tk.Label(root, text="Threshold:")
        self.threshold_label.pack()
        self.threshold_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.threshold_slider.set(100)
        self.threshold_slider.pack()

        self.blur_label = tk.Label(root, text="Blur Size:")
        self.blur_label.pack()
        self.blur_slider = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, resolution=1)
        self.blur_slider.set(9)
        self.blur_slider.pack()

        self.process_btn = tk.Button(root, text="Process Image", command=self.process_image, state=tk.DISABLED)
        self.process_btn.pack(pady=5)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.save_btn = tk.Button(root, text="Save Processed Image", command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack(pady=5)

        self.annotation_text = ScrolledText(root, height=10, width=70, state=tk.DISABLED)
        self.annotation_text.pack(pady=10)

        self.original_image_path = None
        self.processed_image = None

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpeg;*.jpg;*.png;*.bmp")])
        if file_path:
            self.original_image_path = file_path
            self.display_image(file_path)
            self.process_btn.config(state=tk.NORMAL)

    def display_image(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((500, 500))  # Resize for display
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def process_image(self):
        if not self.original_image_path:
            messagebox.showerror("Error", "No image selected!")
            return

        try:
            # Handle Japanese or special character paths
            with open(self.original_image_path, 'rb') as f:
                file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                img_color = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img_color is None:
                raise FileNotFoundError("Failed to load the image. Check the file path or its format.")

            # Create inverted color version of the image
            inverted_img_color = cv2.bitwise_not(img_color)

            # Read parameters from sliders
            threshold = self.threshold_slider.get()
            blur_size = max(1, self.blur_slider.get())  # Ensure blur size is at least 1

            # Process image
            img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.blur(img_gray, (blur_size, blur_size))
            _, img_binary = cv2.threshold(img_blur, threshold, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Draw contours, bounding rectangles, and center points
            img_color_with_annotations = img_color.copy()
            self.annotation_text.config(state=tk.NORMAL)
            self.annotation_text.delete(1.0, tk.END)  # Clear previous annotations

            for i, contour in enumerate(contours):
                # Get inverted color for the contour
                color = tuple(map(int, inverted_img_color[contour[0][0][1], contour[0][0][0]]))

                # Draw the contour
                cv2.drawContours(img_color_with_annotations, [contour], -1, color, 2)

                # Calculate bounding rectangle and draw it
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img_color_with_annotations, (x, y), (x + w, y + h), color, 2)

                # Calculate moments and centroid
                moments = cv2.moments(contour)
                if moments["m00"] != 0:  # Avoid division by zero
                    center_x = int(moments["m10"] / moments["m00"])
                    center_y = int(moments["m01"] / moments["m00"])
                else:
                    center_x, center_y = 0, 0

                # Draw centroid using inverted colors
                cv2.circle(img_color_with_annotations, (center_x, center_y), 5, color, -1)

                # Add annotation to text widget
                annotation = f"Contour {i+1}: Centroid=({center_x},{center_y})\n"
                self.annotation_text.insert(tk.END, annotation)

            self.annotation_text.config(state=tk.DISABLED)

            # Convert processed image to PIL format
            img_color_with_annotations = cv2.cvtColor(img_color_with_annotations, cv2.COLOR_BGR2RGB)
            self.processed_image = Image.fromarray(img_color_with_annotations)

            # Display processed image
            self.display_processed_image(self.processed_image)
            self.save_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Image processing failed: {e}")

    def display_processed_image(self, image):
        image.thumbnail((500, 500))  # Resize for display
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpeg",
                                                     filetypes=[("JPEG files", "*.jpeg"),
                                                                ("PNG files", "*.png"),
                                                                ("BMP files", "*.bmp")])
            if file_path:
                self.processed_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ContourApp(root)
    root.mainloop()
