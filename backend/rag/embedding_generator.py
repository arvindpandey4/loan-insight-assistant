"""
Embedding Generator Module
Handles embedding generation using Sentence Transformers
"""

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Generate embeddings using Sentence Transformers"""
    
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """Initialize with a model name"""
        self.model_name = model_name
        self.model = None
        self.embeddings = None
        self.metadata = {}
        
    def load_model(self):
        """Load the sentence transformer model"""
        print(f"\n[MODEL] Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        print(f"[OK] Model loaded successfully")
        return self
    
    def generate_embeddings(self, texts, batch_size=32, normalize=True, show_progress=True):
        """
        Generate embeddings for a list of texts
        
        Parameters:
        -----------
        texts : list
            List of text strings to embed
        batch_size : int
            Batch size for encoding
        normalize : bool
            Whether to L2 normalize embeddings (for cosine similarity)
        show_progress : bool
            Whether to show progress bar
            
        Returns:
        --------
        numpy.ndarray
            Array of embeddings with shape (len(texts), embedding_dim)
        """
        print(f"\n[EMBED] Generating embeddings for {len(texts)} texts...")
        
        if self.model is None:
            self.load_model()
        
        # Generate embeddings
        print("   Encoding texts...")
        self.embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        # Store metadata
        self.metadata['model_name'] = self.model_name
        self.metadata['total_embeddings'] = self.embeddings.shape[0]
        self.metadata['embedding_dimension'] = self.embeddings.shape[1]
        self.metadata['normalized'] = normalize
        self.metadata['batch_size'] = batch_size
        
        print(f"[OK] Generated {self.embeddings.shape[0]} embeddings of dimension {self.embeddings.shape[1]}")
        
        return self.embeddings
    
    def encode_query(self, query, normalize=True):
        """
        Encode a single query text
        
        Parameters:
        -----------
        query : str
            Query text to encode
        normalize : bool
            Whether to normalize the embedding
            
        Returns:
        --------
        numpy.ndarray
            Query embedding
        """
        if self.model is None:
            self.load_model()
        
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=normalize,
            convert_to_numpy=True
        )
        
        return query_embedding
    
    def save_embeddings(self, filepath):
        """Save embeddings to a numpy file"""
        if self.embeddings is None:
            raise ValueError("No embeddings to save. Generate embeddings first.")
        
        np.save(filepath, self.embeddings)
        print(f"[OK] Saved embeddings to {filepath}")
        return self
    
    def load_embeddings(self, filepath):
        """Load embeddings from a numpy file"""
        self.embeddings = np.load(filepath)
        print(f"[OK] Loaded embeddings from {filepath}")
        print(f"   Shape: {self.embeddings.shape}")
        return self
    
    def get_embeddings(self):
        """Return the generated embeddings"""
        return self.embeddings
    
    def get_metadata(self):
        """Return embedding metadata"""
        return self.metadata
    
    def get_model(self):
        """Return the loaded model"""
        return self.model