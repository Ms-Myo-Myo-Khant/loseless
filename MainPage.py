import tkinter as tk
from customtkinter import *
from tkinter import filedialog, messagebox, Toplevel, Label
from PIL import Image, ImageTk
import numpy as np
import os
import heapq
from collections import Counter, defaultdict
import threading
from PIL import Image, ImageTk

# Declaring as public from the start
original_img=None
original_size = 0

# Tab Button colors variables
active_btn_color = "#00BB6D"
inactive_tab_color = "transparent"

root = CTk()

# Original Image Frame
originalTitleText = CTkLabel(root, text="Original Image", compound="right", font=("Poppins", 16),
                            text_color="#fff")
originalTitleText.place(x=630, y=220)

originalFrame = CTkFrame(root, width=350, height=250,
                            bg_color="#121212", border_width=1, border_color="#00BB6D")
originalFrame.place(x=505, y=250)

original_panel = CTkLabel(root,text="")
original_panel.place(x=560,y=300) 

# Compressed Image Frame
compressedTitleText = CTkLabel(root, text="Compressed Image", compound="right", font=("Poppins", 16),
                            text_color="#fff")
compressedTitleText.place(x=1020, y=220)

compressedFrame = CTkFrame(root, width=350, height=250,
                            bg_color="#121212", border_width=1, border_color="#00BB6D")
compressedFrame.place(x=905, y=250)

compressed_panel = CTkLabel(root,text="")
compressed_panel.place(x=960,y=300)

info_label = CTkLabel(root, text="",compound="right", font=("Poppins", 16),
                            text_color="#fff")
info_label.place(x=700,y=530)

def show_loading_popup():
    loading_popup = Toplevel(root)
    loading_popup.title("Processing")
    loading_popup.configure(bg="#121212")
    loading_popup.iconbitmap("Image/favicon.ico")
    width = 380
    height = 200
    x = loading_popup.winfo_screenwidth() // 2 - width // 2
    y = loading_popup.winfo_screenheight() // 2 - height // 2
    loading_popup.geometry(f"{width}x{height}+{x + 120}+{y}")

    loading_popup.resizable(width=False, height=False)
    
     
    alertLabel = CTkLabel(loading_popup, text="Processing, please wait...", font=("Poppins", 16), text_color="#00BB6D",
                            bg_color="transparent")
    alertLabel.place(x=74, y=60)

    return loading_popup

def custom_messagebox(message):
    top = Toplevel(root)
    top.title("Alert")
    top.configure(bg="#121212")
    top.iconbitmap("Image/favicon.ico")
    width = 320
    height = 180
    x = top.winfo_screenwidth() // 2 - width // 2
    y = top.winfo_screenheight() // 2 - height // 2
    top.geometry(f"{width}x{height}+{x + 120}+{y}")

    top.resizable(width=False, height=False)
    
    label = CTkLabel(top, text=message, font=("Poppins", 16), text_color="#00BB6D",
                            bg_color="transparent")
    label.place(relx=0.5, rely=0.3, anchor='center')

    ok_button = CTkButton(top, text="Ok",
                            font=("Poppins", 16), border_color="#00BB6D", border_width=1,
                            fg_color=inactive_tab_color, corner_radius=10,
                            command=top.destroy,)
    ok_button.place(relx=0.5, rely=0.6, anchor='center')
                    
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
    huffman_tree_root = build_huffman_tree(frequencies)  
    codes = generate_huffman_codes(huffman_tree_root)  

    encoded_data = "".join(codes[symbol] for symbol in data)  
    return encoded_data, huffman_tree_root  

def huffman_decode(encoded_data, huffman_tree_root):
    decoded_data = []
    current_node = huffman_tree_root

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left  
        else:
            current_node = current_node.right  

        if current_node.symbol is not None:
            decoded_data.append(current_node.symbol)  
            current_node = huffman_tree_root  

    return decoded_data

def compress_with_huffman(): 
    global original_img, original_size
    

    if original_img is None:
        custom_messagebox("No image has been chosen!")
        return
    
    loading_popup = show_loading_popup()
    def run_compression(root_window):
        original_img_array=list(original_img.getdata()) 
        encoded_pixels, root = huffman_encode(original_img_array)
        encoded_data = ''.join(encoded_pixels)
        decoded_data = huffman_decode(encoded_data, root)
        compressed_img = Image.new(original_img.mode, original_img.size)
        compressed_img.putdata(decoded_data)
        
        # Calculate compressed size
        compressed_size = len(encoded_data) 
        
        # Calculate compression ratio
        compression_ratio = original_size / compressed_size

        root_window.after(3000, lambda: display_compressed_image(compressed_img))
        root_window.after(3000, lambda: show_compressed_size(compressed_size, compression_ratio))
        root_window.after(3000, loading_popup.destroy)
    
    threading.Thread(target=run_compression, args=(root,)).start()


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

    global original_img,original_size
    
    if original_img is None:
        custom_messagebox("No image has been chosen!")
        return
    
    loading_popup = show_loading_popup()

    def run_compression():
        # Perform RLE compression
        original_img_array=np.array(original_img)
        encoded_pixels = rle_encode(original_img_array)
        decoded_img_array = rle_decode(encoded_pixels, original_img_array.shape)
        compressed_img = Image.fromarray(decoded_img_array)
        
        # Accurately calculate the compressed size
        tuple_size = 3 + 4  # 3 bytes for the pixel value (RGB), 4 bytes for the count
        compressed_size = len(encoded_pixels) * tuple_size
        
        # Calculate compression ratio
        compression_ratio = original_size / compressed_size
    
        # Display compressed image on the right panel
        root.after(3000,lambda:display_compressed_image(compressed_img))
        root.after(3000,lambda:show_compressed_size(compressed_size, compression_ratio))

        root.after(3000, loading_popup.destroy)

    threading.Thread(target=run_compression).start()



def open_image():
    global original_img,original_size
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    original_img = Image.open(file_path)
    original_img.thumbnail((300, 300))
    original_size = os.path.getsize(file_path) 

    display_original_image(original_img)
    show_original_size(original_size)

def display_original_image(img): 
    
    img_tk = ImageTk.PhotoImage(img)
    original_panel.configure(image=img_tk)
    original_panel.image = img_tk

def display_compressed_image(img):
    img_tk = ImageTk.PhotoImage(img)
    compressed_panel.configure(image=img_tk)
    compressed_panel.image = img_tk

def show_original_size(size):
    info_label.configure(text=f"Original Image Size: {size} bytes")

def show_compressed_size(size, ratio):
    info_label.configure(text=f"Original Image Size: {original_size} bytes\n\nCompressed Image Size: {size} bytes\n\nCompression Ratio: {ratio:.2f}")

def clear_all():
    global original_img, original_size
    original_img = None
    original_size = 0
    
    original_panel.configure(image='')
    original_panel.image = None
    
    compressed_panel.configure(image='')
    compressed_panel.image = None
    
    info_label.configure(text='')

def main():

    
    root.title("Image Compression with RLE and Huffman Coding")
    root.iconbitmap("Image/favicon.ico")
    # Determine the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the desired width and height for your window
    window_width = 1400
    window_height = 700

    # Calculate the x and y positions for the window to be centered
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window to be centered
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    set_appearance_mode("dark")
    set_default_color_theme("green")
    root.resizable(width=TRUE, height=TRUE)

    titleTextFrame = CTkFrame(root, width=900, height=70,
                        border_width=1, border_color="#00BB6D")
    titleTextFrame.place(x=300, y=80)

    titleText = CTkLabel(root, text="Image Compression Application with Huffman Coding and Run Length Encoding", compound="right", font=("Poppins", 18,"bold"),
                            text_color="#fff",height=65,width=895)
    titleText.place(x=302, y=82)

    open_button = CTkButton(root, text="Open Image",
                            font=("Poppins", 16), border_color="#00BB6D", border_width=1,
                            fg_color=active_btn_color, corner_radius=10,height=40, 
                            command=open_image,width=300)
    open_button.place(x=150,y=300)

    rle_compress_button = CTkButton(root, text="Compress with RLE", 
                                    font=("Poppins", 16), border_color="#00BB6D", border_width=1,
                                    fg_color=active_btn_color, corner_radius=10,height=40,
                                    command=compress_with_rle,width=300)
    rle_compress_button.place(x=150,y=350)

    huffman_compress_button = CTkButton(root, text="Compress with Huffman", 
                                        font=("Poppins", 16), border_color="#00BB6D", border_width=1,
                                        fg_color=active_btn_color, corner_radius=10,height=40,
                                        command=compress_with_huffman,width=300)
    huffman_compress_button.place(x=150,y=400)

    clear_button = CTkButton(root, text="Clear", 
                             font=("Poppins", 16), border_color="#00BB6D", border_width=1,
                            fg_color=active_btn_color, corner_radius=10,height=40,
                             command=clear_all,width=300)
    clear_button.place(x=150,y=450)

    
    root.mainloop()


