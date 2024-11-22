import numpy as np
import sys
import argparse
from PIL import Image, ImageOps

ASCII_CHARS = "@%#*+=-:. "

help_message = """
Usage: python ascii_art.py -i <image_path> -o <output_file> [-w new_width] [-b bg_adjust] [-t tolerance]

Arguments:
  -i, --image_path   : Path to the input image file.
  -o, --output_file  : Path to the output text file where ASCII art will be saved.
  -w, --width        : Optional. Width of the output ASCII art. Default is 100.
  -b, --bg_adjust    : Optional. Background adjustment type: 'bright', 'dark', or 'none'. Default is 'none'.
  -t, --tolerance    : Optional. Tolerance for background color removal. Default is 30.

Methods:
  resize_image(image, new_width=100) : Resizes the image while maintaining aspect ratio.
  grayscale_image(image)             : Converts the image to grayscale.
  remove_background(image, bg_color, tolerance) : Removes the specified background color from the image.
  map_pixels_to_ascii(image, bg_adjust) : Maps the grayscale pixels to ASCII characters with background adjustment.
  image_to_ascii(image_path, new_width, bg_adjust, tolerance) : Converts an image to ASCII art.
"""

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Adjust for ASCII character aspect ratio
    resized_image = image.resize((new_width, new_height))
    print(f"Resized image to {new_width}x{new_height}")
    return resized_image

def grayscale_image(image):
    grayscale = image.convert("L")
    return grayscale

def map_pixels_to_ascii(image, bg_adjust, bg_tolerance, fill_char):
    pixels = np.array(image, dtype=int)  # Convert to signed integer type
    ascii_str = ""
    for pixel_value in pixels.flatten():
        if bg_adjust == 'bright':
            pixel_value = max(0, pixel_value - 50)  # Decrease value to brighten
        elif bg_adjust == 'dark':
            pixel_value = min(255, pixel_value + 50)  # Increase value to darken
        elif bg_adjust == 'none':
            if pixel_value > bg_tolerance:  # Use bg_tolerance to determine background
                ascii_str += fill_char  # Replace with fill_char
            else:
                ascii_str += ASCII_CHARS[pixel_value // 32]
            continue
        ascii_str += ASCII_CHARS[pixel_value // 32]
    return ascii_str

def image_to_ascii(image_path, new_width=100, bg_adjust='none', bg_tolerance=240, fill_char=' ', tolerance=30):
    try:
        image = Image.open(image_path)
        print(f"Opened image file {image_path}")
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return

    image = resize_image(image, new_width)
    image = grayscale_image(image)
    ascii_str = map_pixels_to_ascii(image, bg_adjust, bg_tolerance, fill_char)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:(index + img_width)] for index in range(0, ascii_str_len, img_width)])
    return ascii_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument('-i', '--image_path', type=str, required=True, help='Path to the input image file.')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Path to the output text file where ASCII art will be saved.')
    parser.add_argument('-w', '--width', type=int, default=100, help='Width of the output ASCII art. Default is 100.')
    parser.add_argument('-b', '--bg_adjust', type=str, choices=['bright', 'dark', 'none'], default='none', help="Background adjustment type: 'bright', 'dark', or 'none'. Default is 'none'.")
    parser.add_argument('-t', '--tolerance', type=int, default=30, help='Tolerance for background color removal. Default is 30.')
    parser.add_argument('--bg_tolerance', type=int, default=150, help='Tolerance for determining background pixels. Default is 240.')
    parser.add_argument('--fill_char', type=str, default=' ', help='Character to fill background with if bg_adjust is "none". Default is space.')

    args = parser.parse_args()

    ascii_art = image_to_ascii(args.image_path, args.width, args.bg_adjust, args.bg_tolerance, args.fill_char, args.tolerance)

    if ascii_art:
        with open(args.output_file, "w") as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {args.output_file}")
    else:
        print("Failed to generate ASCII art.")