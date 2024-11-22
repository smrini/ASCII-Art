# Image to ASCII/Binary Art Generator

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/dependencies-numpy%20|%20pillow-orange.svg)](https://pypi.org/project/numpy/)

A Python-based command-line tool that converts images into ASCII or binary art. This project provides two separate scripts for generating either ASCII art using various characters (`@%#*+=-:. `) or binary art using 1's and 0's.

## Features

- Convert images to ASCII or binary art
- Maintain aspect ratio during conversion
- Adjustable output width
- Background adjustment options (bright, dark, or none)
- Customizable background tolerance
- Support for different image formats (PNG, JPG, etc.)
- Background removal capabilities
- Custom fill character option for background

## Requirements

- Python 3.x
- NumPy
- Pillow (PIL)

```bash
pip install numpy Pillow
```

## Usage

### ASCII Art Generator

```bash
python ascii_art.py -i <image_path> -o <output_file> [-w width] [-b bg_adjust] [-t tolerance]
```

### Binary Art Generator

```bash
python binary_art.py -i <image_path> -o <output_file> [-w width] [-b bg_adjust] [-t tolerance]
```

### Arguments

| Argument | Short | Long | Description | Default |
|----------|-------|------|-------------|---------|
| Image Path | `-i` | `--image_path` | Path to the input image file | Required |
| Output File | `-o` | `--output_file` | Path to save the generated art | Required |
| Width | `-w` | `--width` | Width of the output art | 100 |
| Background Adjustment | `-b` | `--bg_adjust` | Background adjustment type (`bright`, `dark`, `none`) | none |
| Tolerance | `-t` | `--tolerance` | Tolerance for background color removal | 30 |
| Background Tolerance | N/A | `--bg_tolerance` | Tolerance for determining background pixels | 150 |
| Fill Character | N/A | `--fill_char` | Character to fill background with if bg_adjust is "none" | space |

## Examples

Generate ASCII art with default settings:
```bash
python ascii_art.py -i path/to/image.jpg -o output.txt
```

Generate Binary art with custom width and dark background:
```bash
python binary_art.py -i path/to/image.png -o output.txt -w 150 -b dark
```

## Technical Details

### Image Processing Pipeline

1. **Image Loading**: Opens and validates the input image
2. **Resizing**: Maintains aspect ratio while resizing to desired width
3. **Grayscale Conversion**: Converts image to grayscale for processing
4. **Pixel Mapping**: 
   - ASCII: Maps pixels to characters based on intensity
   - Binary: Maps pixels to 1's and 0's based on threshold
5. **Background Processing**: Applies background adjustments if specified
6. **Output Generation**: Formats and saves the final art to a text file

### Functions

#### Common to Both Scripts:
- `resize_image(image, new_width=100)`: Resizes while maintaining aspect ratio
- `grayscale_image(image)`: Converts to grayscale
- `map_pixels_to_ascii/binary(image, bg_adjust, bg_tolerance, fill_char)`: Maps pixels to characters

## Known Limitations

- Very large images may require significant processing time
- Output quality depends on the input image contrast
- Some detail loss is expected during conversion
- Background removal may not be perfect for complex images

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PIL/Pillow library for image processing
- NumPy for efficient array operations

## Contact
> This code isn't perfect yet, but if you know how to improve it, I'd be happy to see your suggestions.

For bug reports and feature requests, please open an issue on the project repository.

---
> Made with ❤️ using Python