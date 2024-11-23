import numpy as np
import sys
import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

# Character sets remain the same
CHAR_SETS = {
    'standard': "@%#*+=-:. ",
    'detailed': "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    'simple': '#@%-. ',
    'binary': '10',
    'numbers': '8846923570',
    'blocks': '█▆▄▃▂▁ ',
    'blocks2': '██▛▌▖  ',
    'letters': 'MWBHNXKAVREDCJLITP@SZFQUG#=+<>~^",:. ',
    'custom': None
}

def get_fill_char_for_set(char_set):
    """
    Get appropriate fill character based on character set
    """
    if char_set == 'blocks' or char_set == 'blocks2':
        return ' '  # Empty space for blocks
    elif char_set == 'numbers':
        return '0'  # Zero for numbers
    elif char_set == 'letters':
        return '.'  # Dot for letters
    elif char_set == 'binary':
        return '0'  # Zero for binary
    else:
        return ' '  # Default space

def clean_edges_advanced(ascii_art, char_set, border_width=2):
    """
    Enhanced edge cleaning with character set specific handling
    """
    lines = ascii_art.split('\n')
    if not lines:
        return ascii_art

    height = len(lines)
    width = len(lines[0]) if lines else 0
    fill_char = get_fill_char_for_set(char_set)
    
    # Convert to list of lists for easier manipulation
    grid = [list(line) for line in lines]
    
    # Clean top and bottom edges
    for i in range(border_width):
        if i < height:
            # Top edge
            grid[i] = [fill_char] * width
            # Bottom edge
            if i < height:
                grid[-(i+1)] = [fill_char] * width

    # Clean left and right edges
    for i in range(height):
        # Left edge
        for j in range(border_width):
            if j < width:
                grid[i][j] = fill_char
        # Right edge
        for j in range(border_width):
            if j < width:
                grid[i][-(j+1)] = fill_char

    # Convert back to string
    return '\n'.join([''.join(line) for line in grid])

def enhance_edges(image, edge_factor=2.0, sharpen_factor=2.0):
    if image.mode != 'L':
        image = image.convert('L')
    
    # Apply edge enhancement
    edge_enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    # Apply sharpening
    sharpener = ImageEnhance.Sharpness(edge_enhanced)
    sharpened = sharpener.enhance(sharpen_factor)
    
    # Increase contrast
    contraster = ImageEnhance.Contrast(sharpened)
    contrasted = contraster.enhance(1.5)
    
    return contrasted

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

def detect_background(image, tolerance, char_set='standard'):
    """
    Enhanced background detection with character set specific adjustments
    """
    pixels = np.array(image)
    hist = np.histogram(pixels, bins=256, range=(0, 256))[0]
    
    # Adjust background detection based on character set
    if char_set in ['letters', 'numbers']:
        # For letters and numbers, use a more aggressive threshold
        # Find the two highest peaks in the histogram
        peak_indices = np.argsort(hist)[-2:]
        bg_value = min(peak_indices)  # Use the lower value peak as background
        # Adjust tolerance based on character set
        adjusted_tolerance = tolerance * 1.5 if char_set == 'letters' else tolerance * 1.2
    else:
        bg_value = np.argmax(hist)
        adjusted_tolerance = tolerance
    
    bg_mask = np.abs(pixels - bg_value) <= adjusted_tolerance
    return bg_mask

def adjust_for_char_set(pixel_value, char_set_name):
    """
    Improved pixel value adjustment based on character set
    """
    if char_set_name == 'blocks' or char_set_name == 'blocks2':
        return int(np.clip((pixel_value - 32) * 1.5, 0, 255))
    elif char_set_name == 'numbers':
        # Enhance contrast for numbers
        adjusted = int(np.clip((pixel_value - 32) * 1.6, 0, 255))
        return 255 if adjusted > 200 else (0 if adjusted < 50 else adjusted)
    elif char_set_name == 'letters':
        # Enhance contrast for letters
        adjusted = int(np.clip((pixel_value - 32) * 1.7, 0, 255))
        return 255 if adjusted > 180 else (0 if adjusted < 70 else adjusted)
    elif char_set_name == 'binary':
        return 255 if pixel_value > 127 else 0
    return pixel_value

def map_pixels_to_ascii(image, char_set, bg_adjust, bg_tolerance, fill_char):
    pixels = np.array(image, dtype=int)
    
    if isinstance(char_set, str):
        if char_set in CHAR_SETS:
            chars = CHAR_SETS[char_set]
        else:
            chars = char_set
    else:
        chars = CHAR_SETS['standard']
    
    if not chars:
        chars = CHAR_SETS['standard']
    
    # Pass character set to background detection
    bg_mask = detect_background(image, bg_tolerance, char_set if isinstance(char_set, str) else 'standard')
    ascii_str = ""
    pixels_flat = pixels.flatten()
    bg_mask_flat = bg_mask.flatten()
    step = 256 // len(chars)
    
    for idx, pixel_value in enumerate(pixels_flat):
        if bg_adjust == 'bright':
            pixel_value = max(0, pixel_value - 50)
        elif bg_adjust == 'dark':
            pixel_value = min(255, pixel_value + 50)
        
        if bg_mask_flat[idx]:
            ascii_str += fill_char
        else:
            adjusted_value = adjust_for_char_set(pixel_value, char_set if isinstance(char_set, str) else 'standard')
            char_index = min(len(chars) - 1, adjusted_value // step)
            ascii_str += chars[char_index]
    
    return ascii_str

def image_to_ascii(image_path, new_width=100, char_set='standard', bg_adjust='none', 
                  bg_tolerance=30, fill_char=' ', tolerance=30, 
                  edge_enhancement=True, border_cleanup=True):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return

    image = image.convert('L')
    
    if edge_enhancement:
        image = enhance_edges(image)
    
    image = resize_image(image, new_width)
    
    # Use character-set specific fill character
    actual_fill_char = get_fill_char_for_set(char_set) if fill_char == ' ' else fill_char
    
    ascii_str = map_pixels_to_ascii(image, char_set, bg_adjust, bg_tolerance, actual_fill_char)
    
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:(index + img_width)] 
                          for index in range(0, ascii_str_len, img_width)])
    
    if border_cleanup:
        ascii_img = clean_edges_advanced(ascii_img, char_set)
    
    return ascii_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced ASCII Art Generator")
    parser.add_argument('-i', '--image_path', type=str, required=True, 
                       help='Path to the input image file.')
    parser.add_argument('-o', '--output_file', type=str, required=True, 
                       help='Path to the output text file where ASCII art will be saved.')
    parser.add_argument('-w', '--width', type=int, default=100, 
                       help='Width of the output ASCII art. Default is 100.')
    parser.add_argument('-b', '--bg_adjust', type=str, 
                       choices=['bright', 'dark', 'none'], default='none',
                       help="Background adjustment type: 'bright', 'dark', or 'none'.")
    parser.add_argument('-t', '--tolerance', type=int, default=30,
                       help='Tolerance for background color removal. Default is 30.')
    parser.add_argument('-c', '--char_set', type=str, default='standard',
                       help='Character set to use: standard, detailed, simple, binary, numbers, blocks, blocks2, letters, or custom string')
    parser.add_argument('--bg_tolerance', type=int, default=30,
                       help='Tolerance for determining background pixels. Default is 30.')
    parser.add_argument('--fill_char', type=str, default=' ',
                       help='Character to fill background with if bg_adjust is "none".')
    parser.add_argument('--no_edge_enhancement', action='store_true',
                       help='Disable edge enhancement')
    parser.add_argument('--no_border_cleanup', action='store_true',
                       help='Disable border cleanup')

    args = parser.parse_args()

    ascii_art = image_to_ascii(
        args.image_path,
        args.width,
        args.char_set,
        args.bg_adjust,
        args.bg_tolerance,
        args.fill_char,
        args.tolerance,
        not args.no_edge_enhancement,
        not args.no_border_cleanup
    )

    if ascii_art:
        with open(args.output_file, "w", encoding='utf-8') as f:
            f.write(ascii_art)
        print(f"Enhanced ASCII art saved to {args.output_file}")
    else:
        print("Failed to generate ASCII art.")