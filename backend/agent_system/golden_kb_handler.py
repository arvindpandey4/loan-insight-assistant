import json
from pathlib import Path
from typing import Optional, Dict, Any
from difflib import SequenceMatcher

class GoldenKB:
    """Golden Knowledge Base for instant, curated responses to common queries"""
    
    def __init__(self):
        self.kb_path = Path(__file__).parent / "golden_kb.json"
        self.entries = []
        self.load_kb()
    
    def load_kb(self):
        """Load the Golden KB from JSON file"""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entries = data.get('entries', [])
            print(f"[GoldenKB] Loaded {len(self.entries)} entries")
        except Exception as e:
            print(f"[GoldenKB] Error loading KB: {e}")
            self.entries = []
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def find_best_match(self, query: str, threshold: float = 0.65) -> Optional[Dict[str, Any]]:
        """
        Find the best matching entry in the Golden KB
        
        Args:
            query: User's query text
            threshold: Minimum similarity score (0-1) to consider a match
        
        Returns:
            Matching entry dict or None
        """
        query_lower = query.lower().strip()
        best_match = None
        best_score = 0.0
        
        for entry in self.entries:
            for question in entry.get('questions', []):
                # Calculate similarity
                score = self.similarity_score(query_lower, question.lower())
                
                # Also check if query contains the question or vice versa
                if question.lower() in query_lower or query_lower in question.lower():
                    score = max(score, 0.8)  # Boost score for substring matches
                
                if score > best_score:
                    best_score = score
                    best_match = entry
        
        # Return match only if above threshold
        if best_score >= threshold:
            print(f"[GoldenKB] Match found! Score: {best_score:.2f}, ID: {best_match.get('id')}")
            return {
                **best_match,
                'confidence_score': best_score
            }
        
        print(f"[GoldenKB] No match found. Best score: {best_score:.2f}")
        return None
    
    def get_answer(self, query: str) -> Optional[str]:
        """
        Get curated answer from Golden KB if query matches
        
        Args:
            query: User's query text
        
        Returns:
            Curated answer string or None
        """
        match = self.find_best_match(query)
        if match:
            return match.get('answer')
        return None

# Global instance
golden_kb = GoldenKB()
