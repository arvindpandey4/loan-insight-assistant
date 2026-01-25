"""
LangChain RAG Retriever Module
Implements LangChain integration for semantic retrieval with query routing
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
import pandas as pd
from dataclasses import dataclass
import json

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
import faiss


@dataclass
class RetrievalResult:
    """Data class for retrieval results"""
    query: str
    documents: List[Document]
    scores: List[float]
    indices: List[int]
    metadata: Dict
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'query': self.query,
            'num_results': len(self.documents),
            'documents': [
                {
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': float(score)
                }
                for doc, score in zip(self.documents, self.scores)
            ],
            'metadata': self.metadata
        }


class LoanEmbeddings(Embeddings):
    """LangChain-compatible embedding wrapper for Sentence Transformers"""
    
    def __init__(self, embedding_generator):
        """
        Initialize with embedding generator
        
        Parameters:
        -----------
        embedding_generator : EmbeddingGenerator
            The embedding generator instance
        """
        self.embedding_generator = embedding_generator
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs (batch)"""
        embeddings = self.embedding_generator.generate_embeddings(
            texts,
            normalize=True,
            show_progress=False
        )
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed query (single)"""
        embedding = self.embedding_generator.encode_query(text, normalize=True)
        return embedding[0].tolist()


class LoanFAISSVectorStore(VectorStore):
    """LangChain-compatible FAISS vector store for loan data"""
    
    def __init__(self, embedding_function: Embeddings, index: faiss.Index, 
                 documents: List[Document], embedding_array: np.ndarray):
        """
        Initialize FAISS vector store
        
        Parameters:
        -----------
        embedding_function : Embeddings
            LangChain embeddings instance
        index : faiss.Index
            FAISS index
        documents : List[Document]
            List of LangChain documents
        embedding_array : np.ndarray
            Embedding array
        """
        self.embedding_function = embedding_function
        self.index = index
        self.documents = documents
        self._embedding_array = embedding_array
        
    def add_documents(self, documents: List[Document], **kwargs) -> None:
        """Add documents (not implemented for existing index)"""
        raise NotImplementedError("Use LoanRAGRetriever.create_from_embeddings()")
    
    def add_texts(self, texts: List[str], metadatas: List[dict] = None, **kwargs) -> List[str]:
        """Add texts (not implemented for existing index)"""
        raise NotImplementedError("Use LoanRAGRetriever.create_from_embeddings()")
    
    @classmethod
    def from_texts(cls, texts: List[str], embedding: Embeddings, **kwargs) -> "LoanFAISSVectorStore":
        """Create from texts (not supported - use from_embeddings)"""
        raise NotImplementedError("Use from_embeddings() instead")
    
    def similarity_search(self, query: str, k: int = 5, **kwargs) -> List[Document]:
        """Search for similar documents"""
        query_embedding = self.embedding_function.embed_query(query)
        query_embedding = np.array([query_embedding]).astype('float32')
        
        distances, indices = self.index.search(query_embedding, k)
        
        return [self.documents[i] for i in indices[0] if i >= 0]
    
    def similarity_search_with_score(self, query: str, k: int = 5, 
                                     **kwargs) -> List[Tuple[Document, float]]:
        """Search for similar documents with scores"""
        query_embedding = self.embedding_function.embed_query(query)
        query_embedding = np.array([query_embedding]).astype('float32')
        
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx >= 0:
                results.append((self.documents[idx], float(score)))
        
        return results
    
    @classmethod
    def from_embeddings(cls, texts: List[str], embeddings: Embeddings, 
                       df: pd.DataFrame, index: faiss.Index, 
                       embedding_array: np.ndarray) -> "LoanFAISSVectorStore":
        """Create vector store from texts and embeddings"""
        # Create LangChain documents
        documents = []
        for i, text in enumerate(texts):
            metadata = {
                'index': i,
                **{col: str(val) for col, val in df.iloc[i].items()}
            }
            doc = Document(page_content=text, metadata=metadata)
            documents.append(doc)
        
        return cls(embeddings, index, documents, embedding_array)


class LoanRAGRetriever:
    """
    LangChain-based RAG Retriever for Loan Insight Assistant
    Provides semantic search with optional query routing for accuracy
    """
    
    def __init__(self, vector_store: LoanFAISSVectorStore, 
                 embedding_generator, df: pd.DataFrame):
        """
        Initialize RAG retriever
        
        Parameters:
        -----------
        vector_store : LoanFAISSVectorStore
            The vector store instance
        embedding_generator : EmbeddingGenerator
            The embedding generator instance
        df : pd.DataFrame
            Original dataframe for context
        """
        self.vector_store = vector_store
        self.embedding_generator = embedding_generator
        self.df = df
        self.retrieval_history = []
        
    def retrieve(self, query: str, k: int = 5, 
                return_score: bool = True) -> RetrievalResult:
        """
        Retrieve similar loan records for a query
        
        Parameters:
        -----------
        query : str
            The search query
        k : int
            Number of results to retrieve
        return_score : bool
            Whether to return similarity scores
            
        Returns:
        --------
        RetrievalResult
            Result object containing documents, scores, and metadata
        """
        print(f"\n[SEARCH] Retrieving documents for query: '{query}'")
        
        if return_score:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            documents = [doc for doc, _ in results]
            scores = [score for _, score in results]
        else:
            documents = self.vector_store.similarity_search(query, k=k)
            scores = [None] * len(documents)
        
        indices = [doc.metadata.get('index', -1) for doc in documents]
        
        # Store in history
        result = RetrievalResult(
            query=query,
            documents=documents,
            scores=scores,
            indices=indices,
            metadata={
                'k': k,
                'num_results': len(documents),
                'embedding_model': self.embedding_generator.model_name
            }
        )
        
        self.retrieval_history.append(result)
        
        return result
    
    def retrieve_batch(self, queries: List[str], k: int = 5) -> List[RetrievalResult]:
        """
        Retrieve for multiple queries
        
        Parameters:
        -----------
        queries : List[str]
            List of queries
        k : int
            Number of results per query
            
        Returns:
        --------
        List[RetrievalResult]
            List of retrieval results
        """
        print(f"\n[SEARCH] Batch retrieving for {len(queries)} queries...")
        results = [self.retrieve(query, k=k) for query in queries]
        return results
    
    def explain_retrieval(self, result: RetrievalResult) -> Dict:
        """
        Provide detailed explanation of retrieval results
        
        Parameters:
        -----------
        result : RetrievalResult
            The retrieval result to explain
            
        Returns:
        --------
        Dict
            Explanation with analysis
        """
        explanation = {
            'query': result.query,
            'interpretation': self._interpret_query(result.query),
            'num_results_returned': len(result.documents),
            'similarity_scores': [float(s) for s in result.scores if s is not None],
            'documents_summary': []
        }
        
        for doc, score in zip(result.documents, result.scores):
            doc_summary = {
                'customer': doc.metadata.get('Customer_Name', 'Unknown'),
                'loan_amount': doc.metadata.get('Loan_Amount', 'Unknown'),
                'status': doc.metadata.get('Application_Status', 'Unknown'),
                'similarity_score': float(score) if score else None,
                'key_attributes': {}
            }
            
            # Extract key attributes
            for key in ['Age', 'Annual_Income', 'Credit_Score', 'Employment_Status']:
                if key in doc.metadata:
                    doc_summary['key_attributes'][key] = doc.metadata[key]
            
            explanation['documents_summary'].append(doc_summary)
        
        return explanation
    
    def _interpret_query(self, query: str) -> Dict:
        """
        Interpret query to understand intent
        
        Parameters:
        -----------
        query : str
            The query to interpret
            
        Returns:
        --------
        Dict
            Query interpretation
        """
        query_lower = query.lower()
        
        interpretation = {
            'is_statistical': any(word in query_lower for word in 
                                 ['average', 'mean', 'total', 'count', 'how many', 'top']),
            'is_explanatory': any(word in query_lower for word in 
                                 ['why', 'explain', 'show similar', 'pattern', 'reason']),
            'is_demographic_focused': any(word in query_lower for word in 
                                         ['age', 'gender', 'income', 'credit score']),
            'is_status_focused': any(word in query_lower for word in 
                                    ['approved', 'rejected', 'pending', 'status']),
            'raw_query': query
        }
        
        return interpretation
    
    def get_retrieval_history(self) -> List[Dict]:
        """Get all retrieval history"""
        return [result.to_dict() for result in self.retrieval_history]
    
    def save_retrieval_history(self, filepath: str) -> None:
        """Save retrieval history to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.get_retrieval_history(), f, indent=2)
        print(f"[OK] Saved retrieval history to {filepath}")


def create_retriever_from_pipeline(pipeline_output_dir: str, 
                                  embedding_generator) -> LoanRAGRetriever:
    """
    Factory function to create retriever from existing pipeline output
    
    Parameters:
    -----------
    pipeline_output_dir : str
        Path to pipeline output directory
    embedding_generator : EmbeddingGenerator
        The embedding generator instance
        
    Returns:
    --------
    LoanRAGRetriever
        Initialized retriever
    """
    from pathlib import Path
    from .data_loader import LoanDataLoader
    from .vector_store import FAISSVectorStore
    
    output_dir = Path(pipeline_output_dir)
    
    # Load data
    df = pd.read_csv(output_dir / 'processed_loan_data_with_embeddings.csv')
    
    # Load embeddings
    embeddings = np.load(output_dir / 'loan_embeddings.npy')
    
    # Create FAISS index
    faiss_store = FAISSVectorStore()
    faiss_store.create_index(embeddings, index_type='flat')
    
    # Create LangChain components
    loan_embeddings = LoanEmbeddings(embedding_generator)
    vector_store = LoanFAISSVectorStore.from_embeddings(
        texts=df['text_representation'].tolist(),
        embeddings=loan_embeddings,
        df=df,
        index=faiss_store.index,
        embedding_array=embeddings
    )
    
    # Create retriever
    retriever = LoanRAGRetriever(vector_store, embedding_generator, df)
    
    return retriever