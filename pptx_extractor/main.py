"""
CLI interface for the PowerPoint Storyboard Generator
"""

import argparse
import os
import json
from storyboard_generator import StoryboardGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Convert PowerPoint presentations to structured storyboard documents"
    )
    
    parser.add_argument(
        "pptx_path",
        help="Path to the input PowerPoint file"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file",
        default=None
    )
    
    parser.add_argument(
        "--output",
        help="Path for output storyboard document",
        default="storyboard.docx"
    )
    
    parser.add_argument(
        "--template",
        help="Path to template document",
        default=None
    )
    
    parser.add_argument(
        "--instructions",
        help="Path to instructions document",
        default=None
    )
    
    parser.add_argument(
        "--training-pairs",
        help="Path to directory containing training pairs",
        default=None
    )
    
    args = parser.parse_args()
    
    # Create configuration if not provided
    if not args.config:
        config = {
            "template_path": args.template,
            "instruction_path": args.instructions,
            "output_path": os.path.dirname(args.output),
            "training_pairs_path": args.training_pairs
        }
        
        config_path = "config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    else:
        config_path = args.config
    
    try:
        # Initialize generator
        generator = StoryboardGenerator(config_path)
        
        # Load training data if available
        if args.training_pairs:
            print("Loading training data...")
            generator.load_training_data()
        
        # Process PowerPoint file
        print(f"Processing {args.pptx_path}...")
        processed_content = generator.process_pptx(args.pptx_path)
        
        # Generate storyboard
        print(f"Generating storyboard at {args.output}...")
        generator.generate_storyboard(processed_content, args.output)
        
        print("Storyboard generation completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 