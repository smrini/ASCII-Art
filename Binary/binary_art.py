import numpy as np
import sys
import argparse
from PIL import Image, ImageOps

help_message = """
Usage: python binary_art.py -i <image_path> -o <output_file> [-w new_width] [-b bg_adjust] [-t tolerance]

Arguments:
  -i, --image_path   : Path to the input image file.
  -o, --output_file  : Path to the output text file where binary art will be saved.
  -w, --width        : Optional. Width of the output binary art. Default is 100.
  -b, --bg_adjust    : Optional. Background adjustment type: 'bright', 'dark', or 'none'. Default is 'none'.
  -t, --tolerance    : Optional. Tolerance for background color removal. Default is 30.

Methods:
  resize_image(image, new_width=100) : Resizes the image while maintaining aspect ratio.
  grayscale_image(image)             : Converts the image to grayscale.
  map_pixels_to_binary(image, bg_adjust, bg_tolerance, fill_char) : Maps the grayscale pixels to binary characters with background adjustment.
  image_to_binary(image_path, new_width, bg_adjust, bg_tolerance, fill_char, tolerance) : Converts an image to binary art.
"""

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Adjust for ASCII character aspect ratio
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    return image.convert("L")  # Convert to grayscale

def map_pixels_to_binary(image, bg_adjust, bg_tolerance, fill_char):
    pixels = np.array(image, dtype=int)  # Convert to signed integer type
    binary_str = ""
    for pixel_value in pixels.flatten():
        if bg_adjust == 'bright':
            pixel_value = max(0, pixel_value - 50)  # Decrease value to brighten
        elif bg_adjust == 'dark':
            pixel_value = min(255, pixel_value + 50)  # Increase value to darken
        elif bg_adjust == 'none':
            if pixel_value > bg_tolerance:  # Use bg_tolerance to determine background
                binary_str += fill_char  # Replace with fill_char
            else:
                binary_str += '1' if pixel_value < 128 else '0'
            continue
        binary_str += '1' if pixel_value < 128 else '0'
    return binary_str

def image_to_binary(image_path, new_width=100, bg_adjust='none', bg_tolerance=240, fill_char=' ', tolerance=30):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return

    print(f"Original image size: {image.size}")
    image = resize_image(image, new_width)
    print(f"Resized image size: {image.size}")
    image = grayscale_image(image)
    print(f"Image mode after conversion to grayscale: {image.mode}")
    binary_str = map_pixels_to_binary(image, bg_adjust, bg_tolerance, fill_char)
    img_width = image.width
    binary_str_len = len(binary_str)
    binary_img = "\n".join([binary_str[index:(index + img_width)] for index in range(0, binary_str_len, img_width)])
    print(f"Generated binary art length: {binary_str_len}")

    return binary_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument('-i', '--image_path', type=str, required=True, help='Path to the input image file.')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Path to the output text file where binary art will be saved.')
    parser.add_argument('-w', '--width', type=int, default=100, help='Width of the output binary art. Default is 100.')
    parser.add_argument('-b', '--bg_adjust', type=str, choices=['bright', 'dark', 'none'], default='none', help="Background adjustment type: 'bright', 'dark', or 'none'. Default is 'none'.")
    parser.add_argument('-t', '--tolerance', type=int, default=30, help='Tolerance for background color removal. Default is 30.')
    parser.add_argument('--bg_tolerance', type=int, default=150, help='Tolerance for determining background pixels. Default is 240.')
    parser.add_argument('--fill_char', type=str, default=' ', help='Character to fill background with if bg_adjust is "none". Default is space.')

    args = parser.parse_args()

    binary_art = image_to_binary(args.image_path, args.width, args.bg_adjust, args.bg_tolerance, args.fill_char, args.tolerance)

    if binary_art:
        with open(args.output_file, "w") as f:
            f.write(binary_art)
        print(f"Binary art saved to {args.output_file}")
    else:
        print("Failed to generate binary art.")