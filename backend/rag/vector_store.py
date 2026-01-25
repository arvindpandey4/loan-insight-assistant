"""
Vector Store Module
Handles FAISS index creation and vector search
"""

import numpy as np
import faiss
from pathlib import Path


class FAISSVectorStore:
    """FAISS vector store for similarity search"""
    
    def __init__(self):
        """Initialize the vector store"""
        self.index = None
        self.embeddings = None
        self.metadata = {}
        
    def create_index(self, embeddings, index_type='flat', nlist=100, nprobe=10):
        """
        Create FAISS index from embeddings
        
        Parameters:
        -----------
        embeddings : numpy.ndarray
            Array of embeddings with shape (n_samples, embedding_dim)
        index_type : str
            Type of index to create:
            - 'flat': Exact search (IndexFlatIP) - for small datasets
            - 'ivf': Approximate search (IndexIVFFlat) - for large datasets
        nlist : int
            Number of clusters for IVF index
        nprobe : int
            Number of clusters to search in IVF index
        """
        print(f"\n[FAISS] Creating FAISS index (type: {index_type})...")
        
        self.embeddings = embeddings
        dimension = embeddings.shape[1]
        n_vectors = embeddings.shape[0]
        
        if index_type == 'flat' or n_vectors < 10000:
            # Use exact search with IndexFlatIP (Inner Product)
            # For normalized embeddings, inner product = cosine similarity
            print(f"   Using IndexFlatIP (exact search) for {n_vectors} vectors...")
            self.index = faiss.IndexFlatIP(dimension)
            
        elif index_type == 'ivf':
            # Use approximate search with IVF
            print(f"   Using IndexIVFFlat (approximate search) for {n_vectors} vectors...")
            quantizer = faiss.IndexFlatIP(dimension)
            nlist = min(nlist, n_vectors // 39)  # Ensure we have enough vectors per cluster
            self.index = faiss.IndexIVFFlat(
                quantizer, 
                dimension, 
                nlist, 
                faiss.METRIC_INNER_PRODUCT
            )
            
            # Train the index
            print(f"   Training index with {nlist} clusters...")
            self.index.train(embeddings)
            self.index.nprobe = nprobe  # Number of clusters to search
            
        else:
            raise ValueError(f"Unknown index_type: {index_type}. Use 'flat' or 'ivf'.")
        
        # Add embeddings to index
        print("   Adding embeddings to index...")
        self.index.add(embeddings)
        
        # Store metadata
        self.metadata['index_type'] = str(type(self.index).__name__)
        self.metadata['dimension'] = dimension
        self.metadata['total_vectors'] = self.index.ntotal
        self.metadata['metric'] = 'cosine_similarity'
        
        if index_type == 'ivf':
            self.metadata['nlist'] = nlist
            self.metadata['nprobe'] = nprobe
        
        print(f"[OK] FAISS index created with {self.index.ntotal} vectors")
        
        return self
    
    def search(self, query_embedding, k=5):
        """
        Search for k most similar vectors
        
        Parameters:
        -----------
        query_embedding : numpy.ndarray
            Query embedding with shape (1, embedding_dim) or (embedding_dim,)
        k : int
            Number of nearest neighbors to return
            
        Returns:
        --------
        distances : numpy.ndarray
            Similarity scores for each result
        indices : numpy.ndarray
            Indices of the most similar vectors
        """
        if self.index is None:
            raise ValueError("Index not created. Call create_index() first.")
        
        # Ensure query is 2D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        return distances, indices
    
    def batch_search(self, query_embeddings, k=5):
        """
        Search for multiple queries at once
        
        Parameters:
        -----------
        query_embeddings : numpy.ndarray
            Query embeddings with shape (n_queries, embedding_dim)
        k : int
            Number of nearest neighbors to return per query
            
        Returns:
        --------
        distances : numpy.ndarray
            Similarity scores with shape (n_queries, k)
        indices : numpy.ndarray
            Indices with shape (n_queries, k)
        """
        if self.index is None:
            raise ValueError("Index not created. Call create_index() first.")
        
        distances, indices = self.index.search(query_embeddings, k)
        
        return distances, indices
    
    def save_index(self, filepath):
        """Save FAISS index to disk"""
        if self.index is None:
            raise ValueError("No index to save. Create index first.")
        
        filepath = Path(filepath)
        faiss.write_index(self.index, str(filepath))
        print(f"[OK] Saved FAISS index to {filepath}")
        
        return self
    
    def load_index(self, filepath):
        """Load FAISS index from disk"""
        filepath = Path(filepath)
        self.index = faiss.read_index(str(filepath))
        
        # Update metadata
        self.metadata['index_type'] = str(type(self.index).__name__)
        self.metadata['total_vectors'] = self.index.ntotal
        
        print(f"[OK] Loaded FAISS index from {filepath}")
        print(f"   Index type: {self.metadata['index_type']}")
        print(f"   Total vectors: {self.metadata['total_vectors']}")
        
        return self
    
    def get_index(self):
        """Return the FAISS index"""
        return self.index
    
    def get_metadata(self):
        """Return index metadata"""
        return self.metadata
    
    def get_vector_by_id(self, idx):
        """Get a specific vector by its index"""
        if self.embeddings is not None:
            return self.embeddings[idx]
        else:
            # Try to reconstruct from index
            return self.index.reconstruct(int(idx))