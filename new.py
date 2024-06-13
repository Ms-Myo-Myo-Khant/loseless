import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import heapq
from collections import Counter, defaultdict

original_img=None

#Huffman Alogrithm
class HuffmanNode:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(symbol=s, frequency=f) for s, f in frequencies.items()]  
    heapq.heapify(heap)  

    while len(heap) > 1:
        left = heapq.heappop(heap)  
        right = heapq.heappop(heap)  

        internal_node = HuffmanNode(frequency=left.frequency + right.frequency)  
        internal_node.left = left  
        internal_node.right = right  

        heapq.heappush(heap, internal_node)  

    return heap[0]  

def generate_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node.symbol is not None:
        codes[node.symbol] = current_code
    else:
        generate_huffman_codes(node.left, current_code + "0", codes)  
        generate_huffman_codes(node.right, current_code + "1", codes)  

    return codes

def huffman_encode(data):
    frequencies = Counter(data)  
    root = build_huffman_tree(frequencies)  
    codes = generate_huffman_codes(root)  

    encoded_data = "".join(codes[symbol] for symbol in data)  
    return encoded_data, root  

def huffman_decode(encoded_data, root):
    decoded_data = []
    current_node = root

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left  
        else:
            current_node = current_node.right  

        if current_node.symbol is not None:
            decoded_data.append(current_node.symbol)  
            current_node = root  

    return decoded_data

def compress_with_huffman(original_img): 
    global original_img_array, original_size_bytes
    if original_img_array is None:
        messagebox.showerror("Error", "No image has been opened.")
        return
    
    original_img_array = list(original_img.getdata())
    encoded_pixels, root = huffman_encode(original_img_array)
    encoded_data = ''.join(encoded_pixels)
    decoded_data = huffman_decode(encoded_data, root)
    compressed_img = Image.new(original_img.mode, original_img.size)
    compressed_img.putdata(decoded_data)
    
    # Calculate compressed size
    compressed_size_bytes = len(encoded_data) 
    
    # Calculate compression ratio
    compression_ratio = original_size_bytes / compressed_size_bytes
    
    # Display compressed image on the right panel
    display_compressed_image(compressed_img)
    show_compressed_size(compressed_size_bytes, compression_ratio)


#RLE Algorithm
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



def compress_with_rle(): 
    global original_img_array, original_size_bytes
    if original_img_array is None:
        messagebox.showerror("Error", "No image has been opened.")
        return
    
    # Perform RLE compression
    encoded_pixels = rle_encode(original_img_array)
    decoded_img_array = rle_decode(encoded_pixels, original_img_array.shape)
    compressed_img = Image.fromarray(decoded_img_array)
    
    # Accurately calculate the compressed size
    tuple_size = 3 + 4  # 3 bytes for the pixel value (RGB), 4 bytes for the count
    compressed_size = len(encoded_pixels) * tuple_size
    
    # Calculate compression ratio
    compression_ratio = original_size_bytes / compressed_size
    
    # Display compressed image on the right panel
    display_compressed_image(compressed_img)
    show_compressed_size(compressed_size, compression_ratio)



def open_image():
    global original_img
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    original_img = Image.open(file_path)
    original_img.thumbnail((300, 300))
    original_size = os.path.getsize(file_path)
    
    img_array = np.array(original_img)
    display_original_image(original_img)
    show_original_size(original_size)
    
    # Store image data for compression
    global original_img_array, original_size_bytes
    original_img_array = img_array
    original_size_bytes = original_size

def display_original_image(img):
    img_tk = ImageTk.PhotoImage(img)
    original_panel.config(image=img_tk)
    original_panel.image = img_tk

def display_compressed_image(img):
    img_tk = ImageTk.PhotoImage(img)
    compressed_panel.config(image=img_tk)
    compressed_panel.image = img_tk

def show_original_size(size):
    info_label.config(text=f"Original Size: {size} bytes")

def show_compressed_size(size, ratio):
    info_label.config(text=f"Original Size: {original_size_bytes} bytes\nCompressed Size: {size} bytes\nCompression Ratio: {ratio:.2f}")

app = tk.Tk()
app.title("Image Compression with RLE and Huffman Coding")

# Left part
left_frame = tk.Frame(app)
left_frame.pack(side="left")

open_button = tk.Button(left_frame, text="Open Image", command=open_image)
open_button.pack()

rle_compress_button = tk.Button(left_frame, text="Compress with RLE", command=compress_with_rle)
rle_compress_button.pack()

huffman_compress_button = tk.Button(left_frame, text="Compress with Huffman", command=lambda: compress_with_huffman(original_img))
huffman_compress_button.pack()

# Right part
right_frame = tk.Frame(app)
right_frame.pack(side="right")

original_panel = tk.Label(right_frame)
original_panel.pack()

compressed_panel = tk.Label(right_frame)
compressed_panel.pack()

info_label = tk.Label(right_frame, text="")
info_label.pack()

# Initialize global variables
original_img_array = None
original_size_bytes = 0

app.mainloop()
