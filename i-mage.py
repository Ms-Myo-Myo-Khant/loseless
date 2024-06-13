import tkinter as tk
from customtkinter import *
from MainPage import main  # Assuming main() function is defined in MainPage

# Create the main welcome window
welcome_root = CTk()
welcome_root.title("i-Mage")
welcome_root.iconbitmap("Image/favicon.ico")
set_appearance_mode("dark")
set_default_color_theme("green")

# Set window dimensions and position
width = 900
height = 600
x = (welcome_root.winfo_screenwidth() // 2) - (width // 2)
y = (welcome_root.winfo_screenheight() // 2) - (height // 2)
welcome_root.geometry(f"{width}x{height}+{x+80}+{y}")
welcome_root.resizable(width=False, height=False)

# Create main frame
main_frame = CTkFrame(master=welcome_root, width=500, height=350, bg_color="#2B2B2B", border_width=1,
                      border_color="#00BB6D", corner_radius=12)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create welcome header
header = CTkLabel(master=main_frame, text="Welcome", font=("Poppins", 38, "bold"), bg_color="transparent",
                  text_color="#00BB6D")
header.place(x=170, y=40)

# Create welcome message
message = CTkLabel(master=main_frame,
                   text="Welcome to i-Mage, your tool for efficient image compression.\n  Utilizing advanced techniques like Huffman coding and \nRun-Length Encoding (RLE), i-Mage ensures optimal storage \nand transmission of images without compromising quality. \nSimplify your digital workflow with our user-friendly\n interface designed for a variety of image types.",
                   font=("Poppins", 16), text_color="#ffffff")
message.place(x=30, y=120)

# Function to start the main application
def goToMain():
    welcome_root.destroy()
    main()

# Create start button
start_button = CTkButton(master=main_frame, text="Get Started", fg_color="#00BB6D", width=160, height=50,
                         font=("Poppins", 16), hover_color="#00BB6D", command=goToMain)
start_button.place(x=170, y=260)

# Run the Tkinter main loop
welcome_root.mainloop()
