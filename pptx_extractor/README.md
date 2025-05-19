# PowerPoint (PPTX) Text and Image Extractor

A Python module for extracting text and images from PowerPoint (PPTX) files. This module provides an easy-to-use interface for extracting content from PowerPoint presentations.

## Features

- Extract text from all slides in a PowerPoint presentation
- Extract images from all slides and save them to a specified directory
- Get detailed information about extracted images (dimensions, format, etc.)
- Simple API with both class-based and functional interfaces

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Using the convenience function

```python
from pptx_extractor import extract_all

# Extract both text and images
text_content, image_info = extract_all("presentation.pptx", "output_images")

# Process extracted text
for slide in text_content:
    print(f"Slide {slide['slide_number']}:")
    print(slide['text'])

# Process image information
for image in image_info:
    print(f"Image: {image['filename']}")
    print(f"Dimensions: {image['dimensions']}")
```

### Using the PPTXExtractor class

```python
from pptx_extractor import PPTXExtractor

# Create an extractor instance
extractor = PPTXExtractor("presentation.pptx")

# Extract text only
text_content = extractor.extract_text()

# Extract images only
image_info = extractor.extract_images("output_images")
```

## Return Value Formats

### Text Content

The text content is returned as a list of dictionaries with the following structure:

```python
[
    {
        "slide_number": 1,
        "text": "Text content from slide 1"
    },
    {
        "slide_number": 2,
        "text": "Text content from slide 2"
    }
    # ...
]
```

### Image Information

Image information is returned as a list of dictionaries with the following structure:

```python
[
    {
        "slide_number": 1,
        "filename": "slide_1_image_1.png",
        "path": "output_images/slide_1_image_1.png",
        "dimensions": "800x600",
        "format": "png"
    }
    # ...
]
```

## Requirements

- python-pptx==0.6.21
- Pillow==10.2.0

## Example

Check out `example.py` for a complete working example of how to use this module.

## Error Handling

The module includes basic error handling for common issues:

- FileNotFoundError: When the specified PowerPoint file doesn't exist
- Various exceptions that might occur during image extraction and saving

## License

This project is open-source and available under the MIT License. 