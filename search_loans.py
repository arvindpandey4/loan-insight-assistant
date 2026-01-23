"""
Loan Insight Assistant - RAG System Usage Guide
This script demonstrates how to use the generated FAISS index for semantic search
"""

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class LoanSearchEngine:
    def __init__(self, 
                 csv_path='output/processed_loan_data_with_embeddings.csv',
                 index_path='output/loan_faiss_index.bin',
                 model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """Initialize the search engine"""
        print("🔧 Initializing Loan Search Engine...")
        
        # Load data
        print("   Loading processed data...")
        self.df = pd.read_csv(csv_path)
        
        # Load FAISS index
        print("   Loading FAISS index...")
        self.index = faiss.read_index(index_path)
        
        # Load embedding model
        print("   Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        
        print(f"✅ Search engine ready with {len(self.df)} loan records\n")
    
    def search(self, query, k=5, return_details=True):
        """
        Search for similar loan records
        
        Parameters:
        -----------
        query : str
            Natural language search query
        k : int
            Number of results to return
        return_details : bool
            Whether to return full details or just indices
            
        Returns:
        --------
        results : list of dict
            Search results with similarity scores and loan details
        """
        # Encode query
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        if not return_details:
            return indices[0], distances[0]
        
        # Prepare results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            record = self.df.iloc[idx]
            results.append({
                'similarity_score': float(dist),
                'loan_id': record['Loan_ID'],
                'customer_name': record['Customer_Name'],
                'purpose': record['Purpose_of_Loan'],
                'loan_amount': record['Loan_Amount'],
                'loan_status': record['Loan_Status'],
                'cibil_score': record['CIBIL_Score'],
                'applicant_income': record['Applicant_Income'],
                'employment_status': record['Employment_Status'],
                'property_area': record['Property_Area'],
                'text_representation': record['text_representation']
            })
        
        return results
    
    def print_results(self, results):
        """Pretty print search results"""
        print(f"\n📋 Found {len(results)} results:\n")
        print("="*80)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Similarity Score: {result['similarity_score']:.4f}")
            print(f"   Loan ID: {result['loan_id']}")
            print(f"   Customer: {result['customer_name']}")
            print(f"   Purpose: {result['purpose']}")
            print(f"   Amount: INR {result['loan_amount']:,.0f}")
            print(f"   Status: {result['loan_status']}")
            print(f"   CIBIL Score: {result['cibil_score']}")
            print(f"   Income: INR {result['applicant_income']:,.0f}")
            print(f"   Employment: {result['employment_status']}")
            print(f"   Area: {result['property_area']}")
            print(f"   Details: {result['text_representation'][:200]}...")
            print("-"*80)
    
    def search_by_filters(self, query, filters=None, k=10):
        """
        Search with additional filters
        
        Parameters:
        -----------
        query : str
            Natural language search query
        filters : dict
            Dictionary of column:value pairs to filter results
            Example: {'Loan_Status': 'Approved', 'Property_Area': 'Urban'}
        k : int
            Number of results to return (before filtering)
            
        Returns:
        --------
        results : list of dict
            Filtered search results
        """
        # Get more results than needed to account for filtering
        indices, distances = self.search(query, k=k*5, return_details=False)
        
        # Apply filters
        filtered_results = []
        for dist, idx in zip(distances, indices):
            record = self.df.iloc[idx]
            
            # Check if record matches all filters
            if filters:
                match = all(record[col] == val for col, val in filters.items() if col in record)
                if not match:
                    continue
            
            filtered_results.append({
                'similarity_score': float(dist),
                'loan_id': record['Loan_ID'],
                'customer_name': record['Customer_Name'],
                'purpose': record['Purpose_of_Loan'],
                'loan_amount': record['Loan_Amount'],
                'loan_status': record['Loan_Status'],
                'cibil_score': record['CIBIL_Score'],
                'applicant_income': record['Applicant_Income'],
                'employment_status': record['Employment_Status'],
                'property_area': record['Property_Area'],
                'text_representation': record['text_representation']
            })
            
            if len(filtered_results) >= k:
                break
        
        return filtered_results


def demo_searches():
    """Demonstrate various search capabilities"""
    # Initialize search engine
    engine = LoanSearchEngine()
    
    print("🎯 DEMO 1: Search for home loans")
    print("="*80)
    results = engine.search("home loan for family in urban area", k=3)
    engine.print_results(results)
    
    print("\n\n🎯 DEMO 2: Search for high CIBIL score loans")
    print("="*80)
    results = engine.search("approved loans with excellent credit history", k=3)
    engine.print_results(results)
    
    print("\n\n🎯 DEMO 3: Search for business loans")
    print("="*80)
    results = engine.search("business expansion loan for self-employed", k=3)
    engine.print_results(results)
    
    print("\n\n🎯 DEMO 4: Search with filters - Approved loans only")
    print("="*80)
    results = engine.search_by_filters(
        "personal loan for salaried professionals",
        filters={'Loan_Status': 'Approved'},
        k=3
    )
    engine.print_results(results)
    
    print("\n\n🎯 DEMO 5: Search with filters - Urban property only")
    print("="*80)
    results = engine.search_by_filters(
        "young professional looking for first home",
        filters={'Property_Area': 'Urban', 'Loan_Status': 'Approved'},
        k=3
    )
    engine.print_results(results)
    
    print("\n\n✅ Demo completed!")
    print("="*80)


def interactive_search():
    """Interactive search mode"""
    engine = LoanSearchEngine()
    
    print("\n" + "="*80)
    print("🔍 INTERACTIVE LOAN SEARCH")
    print("="*80)
    print("Enter your search queries (or 'quit' to exit)")
    print("Examples:")
    print("  - 'home loan with good credit score'")
    print("  - 'business loan for manufacturing'")
    print("  - 'personal loan for medical emergency'")
    print("="*80 + "\n")
    
    while True:
        try:
            query = input("Enter search query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            results = engine.search(query, k=5)
            engine.print_results(results)
            print("\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        # Run interactive mode
        interactive_search()
    else:
        # Run demo
        demo_searches()
