"""
Example script demonstrating the usage of the PPTXExtractor module.
"""

from pptx_extractor import PPTXExtractor, extract_all
import json

def main():
    # Example PowerPoint file path
    pptx_path = "example.pptx"
    
    # Directory to save extracted images
    images_dir = "extracted_images"
    
    try:
        # Method 1: Using the convenience function
        print("Method 1: Using extract_all()")
        text_content, image_info = extract_all(pptx_path, images_dir)
        
        # Print extracted text
        print("\nExtracted Text:")
        for slide in text_content:
            print(f"\nSlide {slide['slide_number']}:")
            print(slide['text'])
        
        # Print image information
        print("\nExtracted Images:")
        print(json.dumps(image_info, indent=2))
        
        # Method 2: Using the PPTXExtractor class directly
        print("\nMethod 2: Using PPTXExtractor class")
        extractor = PPTXExtractor(pptx_path)
        
        # Extract text only
        text_content = extractor.extract_text()
        print("\nText extraction completed")
        
        # Extract images only
        image_info = extractor.extract_images(images_dir)
        print("Image extraction completed")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 