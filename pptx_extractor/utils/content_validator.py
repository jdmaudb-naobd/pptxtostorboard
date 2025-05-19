"""
Content Validator
Checks content for brand names, company names, and other restricted content
"""

import re
from typing import Dict, List, Set, Tuple
import spacy
import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

class ContentValidator:
    def __init__(self, custom_lists_path: str = None):
        """
        Initialize the content validator
        
        Args:
            custom_lists_path: Path to custom lists of restricted terms
        """
        # Load spaCy for named entity recognition
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load BGE-M3 for semantic similarity
        self.model = SentenceTransformer("BAAI/bge-m3")
        
        # Initialize restricted terms
        self.restricted_terms = {
            "companies": set(),
            "brands": set(),
            "products": set()
        }
        
        # Load custom lists if available
        if custom_lists_path and os.path.exists(custom_lists_path):
            with open(custom_lists_path, 'r') as f:
                custom_lists = json.load(f)
                for category in self.restricted_terms:
                    if category in custom_lists:
                        self.restricted_terms[category].update(custom_lists[category])

    def validate_content(self, text: str) -> Dict[str, List[Dict[str, any]]]:
        """
        Validate content for restricted terms and return findings
        
        Returns:
            Dictionary with categories and their findings
        """
        findings = {
            "companies": [],
            "brands": [],
            "products": [],
            "other": []
        }
        
        # Check for exact matches
        for category, terms in self.restricted_terms.items():
            for term in terms:
                pattern = r'\b' + re.escape(term) + r'\b'
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    findings[category].append({
                        "term": term,
                        "context": self._get_context(text, match.start(), match.end()),
                        "position": (match.start(), match.end())
                    })
        
        # Use spaCy for named entity recognition
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                findings["other"].append({
                    "term": ent.text,
                    "type": ent.label_,
                    "context": self._get_context(text, ent.start_char, ent.end_char),
                    "position": (ent.start_char, ent.end_char)
                })
        
        return findings

    def _get_context(self, text: str, start: int, end: int, context_window: int = 50) -> str:
        """Get context around a matched term"""
        context_start = max(0, start - context_window)
        context_end = min(len(text), end + context_window)
        return text[context_start:context_end]

    def suggest_replacements(self, term: str) -> List[str]:
        """
        Suggest generic replacements for restricted terms
        """
        generic_terms = {
            "company": ["healthcare company", "pharmaceutical company", "biotech company"],
            "brand": ["medication", "treatment", "therapy"],
            "product": ["medical device", "therapeutic option", "treatment option"]
        }
        
        # Encode the term
        term_embedding = self.model.encode([term])[0]
        
        # Find most similar generic terms
        suggestions = []
        for category, replacements in generic_terms.items():
            replacement_embeddings = self.model.encode(replacements)
            similarities = np.dot(replacement_embeddings, term_embedding)
            best_idx = np.argmax(similarities)
            suggestions.append(replacements[best_idx])
        
        return suggestions

    def add_restricted_term(self, term: str, category: str):
        """Add a new restricted term"""
        if category in self.restricted_terms:
            self.restricted_terms[category].add(term)

    def remove_restricted_term(self, term: str, category: str):
        """Remove a restricted term"""
        if category in self.restricted_terms:
            self.restricted_terms[category].discard(term)

    def save_restricted_terms(self, path: str):
        """Save the current restricted terms"""
        with open(path, 'w') as f:
            json.dump({k: list(v) for k, v in self.restricted_terms.items()}, f, indent=2)

    def load_restricted_terms(self, path: str):
        """Load restricted terms"""
        with open(path, 'r') as f:
            terms = json.load(f)
            for category, terms_list in terms.items():
                self.restricted_terms[category] = set(terms_list) 