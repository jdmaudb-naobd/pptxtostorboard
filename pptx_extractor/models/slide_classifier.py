"""
Hybrid Slide Classifier for PowerPoint content
Combines rule-based and ML-based classification
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List, Optional, Tuple
import re
import json
import os

class SlideClassifier:
    def __init__(self, model_name: str = "BAAI/bge-m3", custom_rules_path: Optional[str] = None):
        self.categories = [
            'title', 'disclosure', 'introduction', 'clinical_trial',
            'patient_case', 'disease_info', 'quiz', 'conclusion'
        ]
        
        # Load BGE-M3 model for semantic understanding
        self.model = SentenceTransformer(model_name)
        
        # Rule-based patterns
        self.rules = {
            'title': r'(?i)(title|welcome|overview)',
            'disclosure': r'(?i)(disclos|conflict.*interest)',
            'introduction': r'(?i)(introduction|background|overview)',
            'clinical_trial': r'(?i)(trial|study|phase|clinical|data|results)',
            'patient_case': r'(?i)(case|patient|presentation)',
            'quiz': r'(?i)(quiz|question|test|assessment)',
            'conclusion': r'(?i)(conclusion|summary|key.*points)'
        }
        
        # Load custom rules if available
        if custom_rules_path and os.path.exists(custom_rules_path):
            with open(custom_rules_path, 'r') as f:
                custom_rules = json.load(f)
                self.rules.update(custom_rules)

    def classify_slide(self, slide_content: Dict[str, any]) -> Dict[str, float]:
        """
        Classify a slide using both rule-based and semantic approaches
        
        Args:
            slide_content: Dictionary containing slide text and metadata
        """
        scores = {category: 0.0 for category in self.categories}
        
        # Rule-based classification
        text = slide_content.get('text', '')
        for category, pattern in self.rules.items():
            if re.search(pattern, text):
                scores[category] += 0.5
        
        # Semantic classification using BGE-M3
        embeddings = self.model.encode([text])
        # TODO: Implement semantic matching with pre-defined category descriptions
        
        return scores

    def train_on_examples(self, training_data: List[Tuple[Dict, str]]):
        """
        Train the classifier on example slides
        
        Args:
            training_data: List of tuples (slide_content, category)
        """
        # Update rules based on training examples
        for slide_content, category in training_data:
            text = slide_content.get('text', '').lower()
            words = set(re.findall(r'\w+', text))
            
            # Update rules for the category
            if category in self.rules:
                pattern = self.rules[category]
                # TODO: Implement pattern learning from examples
    
    def get_slide_type(self, slide_content: Dict[str, any], confidence_threshold: float = 0.7) -> Tuple[str, float]:
        """
        Get the predicted slide type and confidence score
        
        Returns:
            Tuple of (predicted_category, confidence_score)
        """
        scores = self.classify_slide(slide_content)
        predicted_category = max(scores.items(), key=lambda x: x[1])
        
        if predicted_category[1] < confidence_threshold:
            return ('unknown', predicted_category[1])
        
        return predicted_category

    def save_rules(self, path: str):
        """Save the current rule patterns"""
        with open(path, 'w') as f:
            json.dump(self.rules, f, indent=2)

    def load_rules(self, path: str):
        """Load custom rule patterns"""
        with open(path, 'r') as f:
            self.rules = json.load(f) 