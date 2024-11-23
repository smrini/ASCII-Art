# Enhanced ASCII Art Generator

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/dependencies-numpy%20|%20pillow-orange.svg)](https://pypi.org/project/numpy/)

A sophisticated Python-based command-line tool that converts images into ASCII art using various character sets. This enhanced version offers multiple character sets, edge enhancement, and advanced background processing capabilities.

## Features

- Multiple character set options:
  - Standard (`@%#*+=-:. `)
  - Detailed (`$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'. `)
  - Simple (`#@%-. `)
  - Binary (`10`)
  - Numbers (`8846923570`)
  - Blocks (`█▆▄▃▂▁ `)
  - Blocks2 (`██▛▌▖  `)
  - Letters (`MWBHNXKAVREDCJLITP@SZFQUG#=+<>~^",:. `)
  - Custom (user-defined character set)
- Edge enhancement with adjustable factors
- Intelligent border cleanup
- Background detection and removal
- Character-set-specific optimizations
- Aspect ratio preservation
- Adjustable output width
- Background adjustment options (bright, dark, or none)
- Customizable background tolerance
- Support for various image formats (PNG, JPG, etc.)

## Requirements

- Python 3.x
- NumPy
- Pillow (PIL)

```bash
pip install numpy Pillow
```

## Usage

```bash
python ascii_art.py -i <image_path> -o <output_file> [options]
```

### Arguments

| Argument | Short | Long | Description | Default |
|----------|-------|------|-------------|---------|
| Image Path | `-i` | `--image_path` | Path to the input image file | Required |
| Output File | `-o` | `--output_file` | Path to save the generated art | Required |
| Width | `-w` | `--width` | Width of the output art | 100 |
| Background Adjustment | `-b` | `--bg_adjust` | Background adjustment type (`bright`, `dark`, `none`) | none |
| Tolerance | `-t` | `--tolerance` | Tolerance for background color removal | 30 |
| Character Set | `-c` | `--char_set` | Character set to use (`standard`, `detailed`, `simple`, `binary`, `numbers`, `blocks`, `blocks2`, `letters`, or custom string) | standard |
---

## Examples

Generate ASCII art with default settings:
```bash
python ascii_art.py -i path/to/image.jpg -o output.txt
```

Generate ASCII art with detailed character set and edge enhancement:
```bash
python ascii_art.py -i path/to/image.png -o output.txt -w 150 -c detailed
```

Generate block-style ASCII art with dark background:
```bash
python ascii_art.py -i path/to/image.jpg -o output.txt -c blocks -b dark
```

## Technical Details

### Image Processing Pipeline

1. **Image Loading**: Opens and validates the input image
2. **Edge Enhancement**: Applies edge detection and sharpening (if enabled)
3. **Resizing**: Maintains aspect ratio while resizing to desired width
4. **Grayscale Conversion**: Converts image to grayscale for processing
5. **Background Detection**: Intelligent background detection based on character set
6. **Pixel Mapping**: Maps pixels to characters with set-specific optimizations
7. **Border Cleanup**: Advanced edge cleaning with character-set-specific handling
8. **Output Generation**: Formats and saves the final art to a text file

### Key Functions

- `enhance_edges()`: Applies edge enhancement and sharpening
- `detect_background()`: Character-set-aware background detection
- `adjust_for_char_set()`: Optimizes pixel values for different character sets
- `clean_edges_advanced()`: Intelligent border cleanup
- `map_pixels_to_ascii()`: Enhanced pixel-to-character mapping

## Known Limitations

- Very large images may require significant processing time
- Output quality depends on the input image contrast
- Some detail loss is expected during conversion
- Background removal may not be perfect for complex images
- Edge enhancement may produce artifacts on certain images

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

For bug reports and feature requests, please open an issue on the project repository.

---
> Made with ❤️ using Python
