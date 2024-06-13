import tkinter
import customtkinter
from PIL.ImageTk import PhotoImage
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from tkinter import filedialog 
import threading

# Declaring icons as public from the start
uploadIcon = CTkImage(Image.open("Image/upload.png"), size=(30, 30))
downloadIcon = CTkImage(Image.open("Image/download.png"), size=(22, 22))
logo = CTkImage(Image.open("Image/i-logo.png"), size=(140, 50))
linkicon = CTkImage(Image.open("Image/link.png"), size=(20, 20))
plusicon = CTkImage(Image.open("Image/plus_icon.png"), size=(20, 20))
rightArrowIcon = CTkImage(Image.open("Image/arrow_right.png"), size=(40, 40))
smileIcon = CTkImage(Image.open("Image/smile.png"), size=(20, 20))

# Tab Button colors variables
active_btn_color = "#00BB6D"
inactive_tab_color = "transparent"

# Creating for User Uploaded Image Variable as public to use in another places.
uploaded_image = None

# Creating after image (after changing) to be implement download function
after_image = None

# Function for changing frame

def on_tab_click(sectionframes, sectionbuttons, currentFrame, currentbutton):
    global after_image

    #to get return from extracted text and passed it into save text function
    
    # Forgetting all Frames
    for frame in sectionframes:
        frame.pack_forget()
        
    
    
    # Setting Inactive Tab Button Color
    for button in sectionbuttons:
        button.configure(fg_color=inactive_tab_color)

    # Setting current Frame and Button Color
    currentFrame.pack(expand=1, fill="both")
    currentbutton.configure(fg_color=active_btn_color)

    # Setting Left Icon in every frame
    # Brand Logo
    brand_logo = CTkLabel(currentFrame, image=logo, text="")
    brand_logo.place(x=26, y=26)

    '''Middle Section : Where main function work'''

    # Result Image Frame
    resultFrame = CTkFrame(currentFrame, width=500, height=370,
                            bg_color="#121212", border_width=1, border_color="#00BB6D")
    resultFrame.place(x=800, y=120)

    # Result Image Label Frame
    result_label = CTkLabel(resultFrame, text="", width=250, height=300)
    result_label.place(x=38, y=32)

    after_image = None
    # creating before image upload frame
    create_before_image_frame(currentFrame, result_label)

    # Middle Right Arrow Icon Creation
    arrow_label = CTkLabel(
        currentFrame, image=rightArrowIcon, text="", bg_color="transparent")
    arrow_label.place(x=745, y=300)

    # result text
    resultText = CTkLabel(result_label, text="Result  ", image=smileIcon, compound="right", font=("Poppins", 16),
                            text_color="#EDEADE")
    resultText.place(x=175, y=150)

    textFrame = CTkFrame(currentFrame, width=900, height=70,
                        border_width=1, border_color="#00BB6D")
    textFrame.place(x=280, y=540)

    originalSizeText = CTkLabel(currentFrame, text="Original Size:  ", compound="right", font=("Poppins", 16),
                            text_color="#00BB6D")
    originalSizeText.place(x=300, y=560)

    compressedSizeText = CTkLabel(currentFrame, text="Compressed Size:  ", compound="right", font=("Poppins", 16),
                            text_color="#00BB6D")
    compressedSizeText.place(x=600, y=560)

    compressedSizeRatio = CTkLabel(currentFrame, text="Compressed Ratio:  ", compound="right", font=("Poppins", 16),
                            text_color="#00BB6D")
    
    compressedSizeRatio.place(x=900, y=560)

    if currentFrame == sectionframes[0]:
        
        # Generate Button for Huffman
        generate_Huffman_Button = CTkButton(currentFrame, text=" Compress", font=("Poppins", 20), border_width=0, corner_radius=32,
                                            fg_color="#00BB6D", width=600, height=50, hover_color="null", 
                                            command=lambda: generate_huffman(currentFrame, result_label, uploaded_image, resultText,originalSizeText,compressedSizeText,compressedSizeRatio))
        generate_Huffman_Button.place(x=460, y=630)

    else:
        # Generate Button for RLE
        generate_RLE_Button = CTkButton(currentFrame, text=" Compress", font=("Poppins", 20), border_width=0, corner_radius=32,
                                            fg_color="#00BB6D", width=600, height=50, hover_color="null", 
                                            command=lambda: generate_RLE(currentFrame, result_label, uploaded_image, resultText,originalSizeText,compressedSizeText,compressedSizeRatio))
        
        generate_RLE_Button.place(x=460, y=630)
        
    # Download Button
    download_Button = CTkButton(currentFrame, text="Download", font=("Poppins", 20), image=downloadIcon, compound="right",
                                border_width=1, border_color="#00BB6D", corner_radius=32,
                                fg_color="transparent", width=600, height=50, hover_color="null", command=lambda: download_image(currentFrame, uploaded_image))
    download_Button.place(x=460, y=696)
    

    
def generate_huffman(currentFrame, result_label, uploaded_image, resultText,originalSizeText,compressedSizeText,compressedSizeRatio):
    # if user click generate button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x + 120}+{y}")

        t.resizable(width=False, height=False)

        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Compress!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null", border_color="#00BB6D",
                                border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)
        t.mainloop()

    else:
        cartoon_image = convert_to_cartoon(uploaded_image)
        # Update the result_label widget with the cartoon image
        result_label.configure(image=cartoon_image)
        result_label.image = cartoon_image

        # Destroy the resultText widget (optional)
        resultText.destroy()

def generate_RLE(currentFrame, result_label, uploaded_image, resultText, originalSizeText, compressedSizeText, compressedSizeRatio):
    global after_image  # Ensure this is updated globally

    if uploaded_image is None:
        alert(currentFrame, "Sorry! Can't Compress!", "Please choose your image first.")
        return

    # Display loading indicator
    loading_label = CTkLabel(currentFrame, text="Compressing, please wait...", font=("Poppins", 16), bg="#121212", fg="#00BB6D")
    loading_label.place(x=100, y=200)

    # Create a thread for the compression to avoid freezing the UI
    def compress_image():
        global after_image
        try:
            # Convert the uploaded image to a NumPy array
            img_array = np.array(uploaded_image)

            # Perform RLE compression
            after_image, original_size, compressed_size = RunLength.compress_RLE(img_array)
            compression_ratio = compressed_size / original_size

            # Resize image if necessary
            max_size = 300
            if max(after_image.size) > max_size:
                after_image.thumbnail((max_size, max_size))

            # Convert the compressed image to a PhotoImage object
            compressed_image_tk = ImageTk.PhotoImage(after_image)

            # Update the result_label widget with the compressed image
            result_label.configure(image=compressed_image_tk)
            result_label.image = compressed_image_tk

            # Update the resultText with compression details
            originalSizeText.configure(text=f"Original Size: {original_size} bytes")
            compressedSizeText.configure(text=f"Compressed Size: {compressed_size} bytes")
            compressedSizeRatio.configure(text=f"Compression Ratio: {compression_ratio:.2f}")

        finally:
            # Remove loading indicator
            loading_label.destroy()

    threading.Thread(target=compress_image).start()


def alert(currentFrame, title, message):
    t = CTkToplevel(currentFrame)
    t.title("Alert")
    t.iconbitmap("Image/favicon.ico")
    t.configure(bg="#121212")
    t.transient([currentFrame])

    width = 380
    height = 220
    x = t.winfo_screenwidth() // 2 - width // 2
    y = t.winfo_screenheight() // 2 - height // 2
    t.geometry(f"{width}x{height}+{x + 120}+{y}")

    t.resizable(width=False, height=False)
    icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
    alertIcon = CTkLabel(t, image=icon, text="")
    alertIcon.place(x=180, y=18)

    alertLabel1 = CTkLabel(t, text=title, font=("Poppins", 22), text_color="#00BB6D", bg_color="transparent")
    alertLabel1.place(x=74, y=60)
    alertLabel2 = CTkLabel(t, text=message, font=("Poppins", 16), text_color="#777", bg_color="transparent")
    alertLabel2.place(x=80, y=100)

    closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null",
                            border_color="#00BB6D", border_width=1, command=t.destroy)
    closeButton.place(x=125, y=150)
    t.mainloop()


# Function for downloading the after image
def download_image(currentFrame, uploaded_image):

    # # if user click download button without uploading image, it will alert to choose image first.
    if uploaded_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")
        t.iconbitmap("favicon.ico")
        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x+120}+{y}")

        t.resizable(width=False, height=False)
        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Download!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please choose your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16),hover_color="null",
                                border_color="#00BB6D", border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)

        t.mainloop()

    # when user uploaded the image and didn't click the generate button and click download button first, it will alert to generate first.
    elif after_image is None:
        t = CTkToplevel(currentFrame)
        t.title("Alert")

        t.iconbitmap("Image/favicon.ico")

        t.configure(bg="#121212")
        t.transient([currentFrame])

        width = 380
        height = 220
        x = t.winfo_screenwidth() // 2 - width // 2
        y = t.winfo_screenheight() // 2 - height // 2
        t.geometry(f"{width}x{height}+{x+120}+{y}")

        t.resizable(width=False, height=False)
        icon = CTkImage(Image.open("Image/sad.png"), size=(30, 30))
        alertIcon = CTkLabel(t, image=icon, text="")
        alertIcon.place(x=180, y=18)

        alertLabel1 = CTkLabel(t, text="Sorry! Can't Download!", font=("Poppins", 22), text_color="#00BB6D",
                               bg_color="transparent")
        alertLabel1.place(x=74, y=60)
        alertLabel2 = CTkLabel(t, text="Please generate your image first.", font=("Poppins", 16),
                               text_color="#777", bg_color="transparent")
        alertLabel2.place(x=80, y=100)

        closeButton = CTkButton(t, text="Ok", fg_color="transparent", font=("Poppins", 16), hover_color="null",
                                border_color="#00BB6D", border_width=1, command=t.destroy)
        closeButton.place(x=125, y=150)

        t.mainloop()

    elif after_image is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            cv2.imwrite(save_path, after_image)

# Uploading Image for first time function
def addImage(image_label, addPhoto):

    # calling global uploaded_image variable to use in another places
    global uploaded_image

    file_path = filedialog.askopenfilename(
        filetypes=[("All files", "*.*"),("JPEG files", "*.jpg"), ("PNG files", "*.png")])
    if file_path:

        uploaded_image = cv2.imread(file_path)

        # Convert image to RGB for PIL
        rgbimage = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)

        # Convert to a PIL Image object
        image_pil = Image.fromarray(rgbimage)

        # Resize image if necessary
        max_size = 300
        if max(image_pil.size) > max_size:
            image_pil.thumbnail((max_size, max_size))

        # Convert to a PhotoImage object
        image_photo = ImageTk.PhotoImage(image_pil)
        uploaded_image=image_photo
        # Update label and add the image
        image_label.configure(image=image_photo)
        image_label.image = image_photo

        addPhoto.destroy()


# Function for uploading new photo
def browse_new_image(result_label, image_label, addPhoto):
    # calling global uploaded_image variable to use in another places
    global uploaded_image
    # checking if the image is uploaded, if there is already an uploaded image, it will upload new image. Unless it will pass.
    if image_label.cget("image") and result_label.cget("image"):
        file_path = filedialog.askopenfilename(
            filetypes=[("All files", "*.*"),("JPEG files", "*.jpg"), ("PNG files", "*.png")])

        if file_path:

            uploaded_image = cv2.imread(file_path)

            # Convert image to RGB for PIL
            rgbimage = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)

            # Convert to a PIL Image object
            image_pil = Image.fromarray(rgbimage)

            # Resize image if necessary
            max_size = 300
            if max(image_pil.size) > max_size:
                image_pil.thumbnail((max_size, max_size))

            # Convert to a PhotoImage object
            image_photo = ImageTk.PhotoImage(image_pil)

            # Update label and add the image
            image_label.configure(image=image_photo)
            image_label.image = image_photo

            addPhoto.destroy()
            result_label.configure(image="")  # clear before result image
    else:
        pass

# Function for Creating Frame for Upload Image Section and Showing Uploaded Image

def create_before_image_frame(currentFrame, result_label):
    # Before Image Frame
    imageFrame = CTkFrame(currentFrame, width=500, height=370,
                          bg_color="#121212", border_width=0.6, border_color="#00BB6D")
    imageFrame.place(x=231, y=120)

    # Before Image Label
    image_label = CTkLabel(imageFrame, text="", width=250,
                           height=300)
    image_label.place(x=150, y=32)

    # To show Browse Your Image button and after User uploaded the button will destory and the image will show in the imagelabel.
    addPhoto = CTkButton(image_label, text="Browse Your Image ", font=("Poppins", 16), image=uploadIcon,
                         fg_color="transparent", hover_color="null", compound="top", anchor="end", text_color="#EDEADE",
                         corner_radius=32, command=lambda: addImage(image_label, addPhoto))
    addPhoto.place(x=10, y=100)

    # For adding new images
    browse_new = CTkButton(currentFrame, text="Select new image", image=plusicon, compound="right", text_color="#00BB6D", font=(
        "Poppins", 15), hover_color="null", bg_color="transparent", fg_color="transparent", command=lambda: browse_new_image(result_label, image_label, addPhoto))
    browse_new.place(x=220, y=490)


def main():

    # Creating Frames as public for 6 sections to change Frame According to current Button
    root = CTk()
    # Setting window Title,Icon, appearance mode and color theme
    root.title("I-mage")
    root.iconbitmap("Image/favicon.ico")
    root.geometry("{}x{}+0+0".format(root.winfo_screenwidth(),
                                     root.winfo_screenheight()))
    set_appearance_mode("dark")
    set_default_color_theme("green")
    root.resizable(width=TRUE, height=TRUE)

   
    huffmanFrame = CTkFrame(root, fg_color="transparent")
    huffmanFrame.pack(expand=1, fill="both")
   
    RLEFrame = CTkFrame(root, fg_color="transparent")
    RLEFrame.pack(expand=1, fill="both")

    '''Header section Start : Including Each Section Button'''

    # setting all to frame into the list for on tab click function
    sectionframes = [huffmanFrame, RLEFrame]

    # Image to Cartoon Button
    huffmanBtn = CTkButton(root, text="Huffman Coding", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                          fg_color=active_btn_color, corner_radius=32,height=40,
                          hover_color="null",
                          command=lambda: on_tab_click(sectionframes, sectionbuttons, huffmanFrame, huffmanBtn))
    huffmanBtn.place(x=600, y=45)

    # Image to Text Button
    RLEBtn = CTkButton(root, text="Run Length Encoding", font=("Poppins", 14), border_color="#00BB6D", border_width=1,
                           fg_color="transparent",height=40,
                           hover_color="null", corner_radius=32,
                           command=lambda: on_tab_click(sectionframes, sectionbuttons, RLEFrame, RLEBtn))
    RLEBtn.place(x=780, y=45)

    # setting all to tab buttons into the list for on tab click function
    sectionbuttons = [huffmanBtn, RLEBtn]

    # Setting image to cartoon frame as current frame
    on_tab_click(sectionframes, sectionbuttons, huffmanFrame, huffmanBtn)

    '''Header section End'''

    root.mainloop()

main()