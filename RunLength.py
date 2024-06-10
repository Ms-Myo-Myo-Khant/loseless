import numpy as np

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
