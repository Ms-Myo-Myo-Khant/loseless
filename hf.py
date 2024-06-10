import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import heapq
from collections import Counter, defaultdict
import os

class HuffmanNode:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

# Function to build the Huffman tree from symbol frequencies
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

# Function to generate Huffman codes from the Huffman tree
def generate_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node.symbol is not None:
        codes[node.symbol] = current_code
    else:
        generate_huffman_codes(node.left, current_code + "0", codes)  
        generate_huffman_codes(node.right, current_code + "1", codes)  

    return codes

# Function to encode data using Huffman codes
def huffman_encode(data):
    frequencies = Counter(data)  
    root = build_huffman_tree(frequencies)  
    codes = generate_huffman_codes(root)  

    encoded_data = "".join(codes[symbol] for symbol in data)  
    return encoded_data, root  

# Function to decode Huffman-encoded data
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

def open_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    original_img = Image.open(file_path)
    original_img.thumbnail((300, 300))
    original_size = os.path.getsize(file_path)
    
    img_array = list(original_img.getdata())
    encoded_pixels, root = huffman_encode(img_array)
    encoded_data = ''.join(encoded_pixels)
    decoded_data = huffman_decode(encoded_data, root)
    decoded_img = Image.new(original_img.mode, original_img.size)
    decoded_img.putdata(decoded_data)
    decoded_size = len(encoded_data) // 8
    show_comparison(original_size, decoded_size)
    display_image(original_img, decoded_img)

def display_image(original_img, decoded_img):
    original_img_tk = ImageTk.PhotoImage(original_img)
    decoded_img_tk = ImageTk.PhotoImage(decoded_img)
    
    original_panel = tk.Label(app)
    original_panel.config(image=original_img_tk)
    original_panel.image = original_img_tk
    original_panel.pack(side="left")

    decoded_panel = tk.Label(app)
    decoded_panel.config(image=decoded_img_tk)
    decoded_panel.image = decoded_img_tk
    decoded_panel.pack(side="right")

def show_comparison(original_size, compressed_size):
    compression_ratio = original_size / compressed_size
    info_label.config(text=f"Original Size: {original_size} bytes\nCompressed Size: {compressed_size} bytes\nCompression Ratio: {compression_ratio:.2f}")

app = tk.Tk()
app.title("Image Compression with Huffman Coding")

open_button = tk.Button(app, text="Open Image", command=open_image)
open_button.pack()

info_label = tk.Label(app, text="")
info_label.pack()

app.mainloop()
