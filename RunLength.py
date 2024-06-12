import numpy as np
from PIL import Image

def rle_encode(img_array):
    pixels = img_array.flatten()
    encoded_pixels = []
    count = 1
    for i in range(1, len(pixels)):
        if np.array_equal(pixels[i], pixels[i - 1]):
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

def compress_RLE(uploaded_image):
    # Convert the uploaded image to a NumPy array
    img_array = np.array(uploaded_image)

    # Get the original size in bytes
    original_size = img_array.nbytes
    
    # Encode and decode
    encoded_pixels = rle_encode(img_array)
    decoded_img_array = rle_decode(encoded_pixels, img_array.shape)
    decoded_img = Image.fromarray(decoded_img_array)
    
    # Calculate the compressed size
    tuple_size = 3 + 4  # Assuming 3 bytes for RGB values and 4 bytes for count
    compressed_size = len(encoded_pixels) * tuple_size

    return decoded_img, original_size, compressed_size
