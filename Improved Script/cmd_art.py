import numpy as np
import sys
import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from typing import Tuple, Optional

# Extended ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "
# Alternative character set with more gradients
DETAILED_ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

class ASCIIArtGenerator:
    def __init__(self, char_set: str = "standard"):
        """Initialize the ASCII Art Generator with specified character set."""
        self.chars = DETAILED_ASCII_CHARS if char_set == "detailed" else ASCII_CHARS
        self.char_length = len(self.chars)

    def enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality while preserving central objects."""
        # Enhance contrast more conservatively
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # Reduced from 1.5 to preserve more detail
        
        # Enhance edges more subtly
        image = image.filter(ImageFilter.EDGE_ENHANCE)  # Changed from EDGE_ENHANCE_MORE
        
        # Apply adaptive sharpening
        sharpness = ImageEnhance.Sharpness(image)
        image = sharpness.enhance(1.4)
        
        return image

    def resize_image(self, image: Image.Image, new_width: int = 100) -> Image.Image:
        """Resize image with better quality preservation."""
        width, height = image.size
        aspect_ratio = height / width
        # Adjusted aspect ratio multiplier for better proportions
        new_height = int(new_width * aspect_ratio * 0.45)  # Reduced from 0.55
        
        # Use LANCZOS resampling with antialiasing
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image

    def adjust_brightness(self, pixel_value: int, bg_adjust: str, intensity: float = 0.7) -> int:
        """Adjust pixel brightness with configurable intensity."""
        if bg_adjust == 'bright':
            return max(0, pixel_value - int(40 * intensity))
        elif bg_adjust == 'dark':
            return min(255, pixel_value + int(40 * intensity))
        return pixel_value

    def detect_edges(self, image: Image.Image) -> np.ndarray:
        """Enhanced edge detection with better object preservation."""
        img_array = np.array(image)
        
        # Modified Sobel filters with reduced intensity
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]) * 0.8
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]) * 0.8
        
        # Apply gaussian blur to reduce noise
        img_array = np.array(Image.fromarray(img_array).filter(ImageFilter.GaussianBlur(radius=0.5)))
        
        edge_x = np.abs(np.correlate(img_array.flatten(), sobel_x.flatten(), mode='same').reshape(img_array.shape))
        edge_y = np.abs(np.correlate(img_array.flatten(), sobel_y.flatten(), mode='same').reshape(img_array.shape))
        
        edge_magnitude = np.sqrt(edge_x**2 + edge_y**2)
        
        # Normalize edge magnitude
        edge_magnitude = (edge_magnitude - edge_magnitude.min()) / (edge_magnitude.max() - edge_magnitude.min())
        return edge_magnitude

    def adaptive_threshold(self, pixel_value: float, local_avg: float, bg_tolerance: int) -> bool:
        """Adaptive thresholding based on local brightness."""
        threshold = bg_tolerance / 255.0
        local_threshold = threshold * (1 + (local_avg / 255.0 - 0.5) * 0.3)
        return pixel_value > local_threshold

    def map_pixels_to_ascii(self, image: Image.Image, bg_adjust: str, 
                          bg_tolerance: int, fill_char: str) -> str:
        """Map pixels to ASCII with improved detail preservation."""
        # Convert to numpy array and detect edges
        pixels = np.array(image, dtype=np.float32)
        edges = self.detect_edges(image)
        
        # Reduced edge weight for better object preservation
        edge_weight = 0.2  # Reduced from 0.3
        pixels = pixels + (edges * edge_weight * 255)
        pixels = np.clip(pixels, 0, 255)
        
        # Calculate local averages for adaptive thresholding
        local_avg = np.array(Image.fromarray(pixels.astype(np.uint8)).filter(
            ImageFilter.BoxBlur(radius=3)))
        
        ascii_str = []
        pixels_flat = pixels.flatten()
        local_avg_flat = local_avg.flatten()
        
        for i, pixel_value in enumerate(pixels_flat):
            adjusted_value = self.adjust_brightness(int(pixel_value), bg_adjust)
            
            if bg_adjust == 'none':
                # Use adaptive thresholding
                if self.adaptive_threshold(pixel_value/255, local_avg_flat[i]/255, bg_tolerance):
                    ascii_str.append(fill_char)
                    continue
            
            # Improved character mapping with gamma correction
            gamma = 1.2  # Adjust for better midtone preservation
            normalized_value = (adjusted_value / 255) ** gamma
            char_index = int(normalized_value * (self.char_length - 1))
            char_index = max(0, min(char_index, self.char_length - 1))
            ascii_str.append(self.chars[char_index])
                
        return ''.join(ascii_str)

    def image_to_ascii(self, image_path: str, new_width: int = 100, 
                      bg_adjust: str = 'none', bg_tolerance: int = 200,  # Adjusted default bg_tolerance
                      fill_char: str = ' ', tolerance: int = 30) -> Optional[str]:
        """Convert image to ASCII art with improved object preservation."""
        try:
            with Image.open(image_path) as image:
                print(f"Processing image: {image_path}")
                print(f"Original size: {image.size}")
                
                # Convert to RGB mode if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Enhancement pipeline
                image = self.enhance_image(image)
                image = self.resize_image(image, new_width)
                
                # Apply additional preprocessing
                image = image.convert("L")  # Convert to grayscale
                
                # Adjust contrast to preserve midtones
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.2)
                
                print(f"Processed size: {image.size}")
                
                # Generate ASCII art
                ascii_str = self.map_pixels_to_ascii(image, bg_adjust, bg_tolerance, fill_char)
                img_width = image.width
                
                # Format the output
                return '\n'.join([ascii_str[index:(index + img_width)] 
                                for index in range(0, len(ascii_str), img_width)])
                
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Enhanced ASCII Art Generator with Object Preservation")
    parser.add_argument('-i', '--image_path', type=str, required=True, 
                       help='Path to the input image file.')
    parser.add_argument('-o', '--output_file', type=str, required=True, 
                       help='Path to the output text file.')
    parser.add_argument('-w', '--width', type=int, default=100, 
                       help='Width of the output ASCII art. Default is 100.')
    parser.add_argument('-b', '--bg_adjust', type=str, 
                       choices=['bright', 'dark', 'none'], default='none',
                       help="Background adjustment type.")
    parser.add_argument('-t', '--tolerance', type=int, default=30,
                       help='Tolerance for background removal.')
    parser.add_argument('--bg_tolerance', type=int, default=200,  # Adjusted default
                       help='Background pixel threshold.')
    parser.add_argument('--fill_char', type=str, default=' ',
                       help='Background fill character.')
    parser.add_argument('--char_set', type=str, choices=['standard', 'detailed'],
                       default='detailed', help='ASCII character set to use.')

    args = parser.parse_args()
    
    generator = ASCIIArtGenerator(char_set=args.char_set)
    ascii_art = generator.image_to_ascii(
        args.image_path, args.width, args.bg_adjust,
        args.bg_tolerance, args.fill_char, args.tolerance
    )

    if ascii_art:
        with open(args.output_file, "w") as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {args.output_file}")
    else:
        print("Failed to generate ASCII art.")

if __name__ == "__main__":
    main()