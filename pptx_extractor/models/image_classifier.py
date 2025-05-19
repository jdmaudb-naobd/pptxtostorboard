"""
Hybrid Image Classifier for PowerPoint content
Combines pre-trained models with custom training capabilities
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
from typing import Dict, List, Tuple, Optional
import os
import json

class HybridImageClassifier:
    def __init__(self, custom_model_path: Optional[str] = None):
        self.categories = [
            'chart', 'graph', 'clinical_image', 'icon', 'shape',
            'algorithm', 'stock_photo', 'logo', 'general_image'
        ]
        
        # Load pre-trained ResNet model
        self.model = models.resnet50(pretrained=True)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, len(self.categories))
        
        # Load custom weights if available
        if custom_model_path and os.path.exists(custom_model_path):
            self.model.load_state_dict(torch.load(custom_model_path))
        
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def classify_image(self, image_path: str) -> Dict[str, float]:
        """
        Classify an image and return confidence scores for each category
        """
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Convert to dictionary of category: probability
            results = {
                category: float(prob)
                for category, prob in zip(self.categories, probabilities)
            }
            
            return results
            
        except Exception as e:
            print(f"Error classifying image {image_path}: {str(e)}")
            return {category: 0.0 for category in self.categories}

    def train_on_examples(self, training_data: List[Tuple[str, str]], epochs: int = 10):
        """
        Train the model on custom examples
        
        Args:
            training_data: List of tuples (image_path, category)
            epochs: Number of training epochs
        """
        # Implementation for fine-tuning the model on custom examples
        pass  # TODO: Implement training logic

    def get_image_metadata(self, image_path: str) -> Dict[str, any]:
        """
        Extract comprehensive image metadata including classification
        """
        classification = self.classify_image(image_path)
        
        # Get additional metadata
        with Image.open(image_path) as img:
            metadata = {
                "dimensions": img.size,
                "format": img.format,
                "mode": img.mode,
                "classification": classification,
                "predicted_type": max(classification.items(), key=lambda x: x[1])[0]
            }
        
        return metadata

    def save_model(self, path: str):
        """Save the model weights"""
        torch.save(self.model.state_dict(), path)

    def load_model(self, path: str):
        """Load model weights"""
        self.model.load_state_dict(torch.load(path)) 