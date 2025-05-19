"""
Abbreviation Handler
Detects and manages abbreviations in medical/scientific content
"""

import re
from typing import Dict, List, Set, Tuple
import spacy
import json
import os

class AbbreviationHandler:
    def __init__(self, custom_dict_path: str = None):
        """
        Initialize the abbreviation handler
        
        Args:
            custom_dict_path: Path to custom abbreviations dictionary
        """
        # Load spaCy model for text processing
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common medical/scientific abbreviations
        self.known_abbreviations = {
            "FDA": "Food and Drug Administration",
            "EMA": "European Medicines Agency",
            "RCT": "Randomized Controlled Trial",
            # Add more common abbreviations
        }
        
        # Load custom abbreviations if available
        if custom_dict_path and os.path.exists(custom_dict_path):
            with open(custom_dict_path, 'r') as f:
                custom_abbrevs = json.load(f)
                self.known_abbreviations.update(custom_abbrevs)

    def find_abbreviations(self, text: str) -> List[Tuple[str, str]]:
        """
        Find abbreviations and their definitions in text
        
        Returns:
            List of tuples (abbreviation, definition)
        """
        abbreviations = []
        
        # Pattern for abbreviations in parentheses
        pattern = r'\(([A-Z][A-Za-z0-9]+)\)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            abbrev = match.group(1)
            # Look for definition before the abbreviation
            context_before = text[:match.start()].strip()
            words = context_before.split()[-6:]  # Look at last 6 words
            
            if words:
                # Try to match capital letters in abbreviation with words
                definition = self._find_definition(abbrev, ' '.join(words))
                if definition:
                    abbreviations.append((abbrev, definition))
        
        return abbreviations

    def _find_definition(self, abbrev: str, text: str) -> str:
        """
        Find the definition of an abbreviation in the given text
        """
        words = text.split()
        abbrev_chars = list(abbrev.lower())
        
        # Try to match first letters of words with abbreviation
        matched_words = []
        word_idx = len(words) - 1
        char_idx = len(abbrev_chars) - 1
        
        while char_idx >= 0 and word_idx >= 0:
            if words[word_idx].lower().startswith(abbrev_chars[char_idx]):
                matched_words.insert(0, words[word_idx])
                char_idx -= 1
            word_idx -= 1
        
        if len(matched_words) == len(abbrev):
            return ' '.join(matched_words)
        
        return None

    def highlight_abbreviations(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Highlight abbreviations in text and return mapping
        
        Returns:
            Tuple of (highlighted_text, abbreviation_dict)
        """
        highlighted_text = text
        abbrev_dict = {}
        
        # Find all abbreviations
        found_abbrevs = self.find_abbreviations(text)
        
        # Add known abbreviations
        for abbrev, definition in found_abbrevs:
            self.known_abbreviations[abbrev] = definition
        
        # Highlight all known abbreviations in text
        for abbrev in self.known_abbreviations:
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            highlighted_text = re.sub(
                pattern,
                lambda m: f'<mark>{m.group()}</mark>',
                highlighted_text
            )
            abbrev_dict[abbrev] = self.known_abbreviations[abbrev]
        
        return highlighted_text, abbrev_dict

    def create_abbreviations_table(self) -> List[Dict[str, str]]:
        """
        Create a table of all found abbreviations
        
        Returns:
            List of dictionaries with abbreviation and definition
        """
        return [
            {"abbreviation": abbrev, "definition": defn}
            for abbrev, defn in sorted(self.known_abbreviations.items())
        ]

    def save_abbreviations(self, path: str):
        """Save the current abbreviations dictionary"""
        with open(path, 'w') as f:
            json.dump(self.known_abbreviations, f, indent=2)

    def load_abbreviations(self, path: str):
        """Load custom abbreviations dictionary"""
        with open(path, 'r') as f:
            self.known_abbreviations.update(json.load(f)) 