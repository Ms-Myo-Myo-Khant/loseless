import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

def rle_encode(img_array):
    pixels = img_array.flatten()
    encoded_pixels = []
    count = 1
    for i in range(1, len(pixels)):
        if np.array_equal(pixels[i], pixels[i - 1]):  # Check if two pixels are equal (for color images)
            count += 1
        else:
            encoded_pixels.append((pixels[i - 1], count))
            count = 1
    encoded_pixels.append((pixels[-1], count))
    return encoded_pixels

def rle_decode(encoded_pixels, shape):
    decoded_pixels = []
    for value, count in encoded_pixels:
        decoded_pixels.extend([value] * count)
    return np.array(decoded_pixels).reshape(shape)

def open_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    img = Image.open(file_path)  # Color image
    img.thumbnail((300, 300))
    img_array = np.array(img)
    original_size = os.path.getsize(file_path)
    
    encoded_pixels = rle_encode(img_array)
    decoded_img_array = rle_decode(encoded_pixels, img_array.shape)
    decoded_img = Image.fromarray(decoded_img_array)
    
    # Accurately calculate the compressed size
    tuple_size = 3 + 4  # 3 bytes for the pixel value (RGB), 4 bytes for the count
    compressed_size = len(encoded_pixels) * tuple_size
    
    display_image(img, decoded_img)
    show_comparison(original_size, compressed_size)

def display_image(original_img, compressed_img):
    original_img_tk = ImageTk.PhotoImage(original_img)
    compressed_img_tk = ImageTk.PhotoImage(compressed_img)
    
    original_panel.img_tk = original_img_tk
    compressed_panel.img_tk = compressed_img_tk
    
    original_panel.config(image=original_img_tk)
    compressed_panel.config(image=compressed_img_tk)

def show_comparison(original_size, compressed_size):
    compression_ratio = original_size / compressed_size
    info_label.config(text=f"Original Size: {original_size} bytes\nCompressed Size: {compressed_size} bytes\nCompression Ratio: {compression_ratio:.2f}")

app = tk.Tk()
app.title("Image Compression with RLE")

open_button = tk.Button(app, text="Open Image", command=open_image)
open_button.pack()

original_panel = tk.Label(app)
original_panel.pack()

compressed_panel = tk.Label(app)
compressed_panel.pack()

info_label = tk.Label(app, text="")
info_label.pack()


