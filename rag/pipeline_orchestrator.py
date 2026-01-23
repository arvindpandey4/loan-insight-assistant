"""
Pipeline Orchestrator
Main script that orchestrates the entire RAG pipeline using modular components
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data_loader import LoanDataLoader
from text_processor import LoanTextProcessor
from embedding_generator import EmbeddingGenerator
from vector_store import FAISSVectorStore


class LoanRAGPipeline:
    """Orchestrate the complete RAG pipeline"""
    
    def __init__(self, csv_path, output_dir='./output', 
                 model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the pipeline
        
        Parameters:
        -----------
        csv_path : str
            Path to the loan dataset CSV file
        output_dir : str
            Directory to save output artifacts
        model_name : str
            Name of the sentence transformer model to use
        """
        self.csv_path = csv_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.model_name = model_name
        
        # Initialize components
        self.data_loader = None
        self.text_processor = None
        self.embedding_generator = None
        self.vector_store = None
        
        # Data storage
        self.df = None
        self.processed_df = None
        self.texts = None
        self.embeddings = None
        
        # Validation report
        self.validation_report = {}
        
    def run_full_pipeline(self):
        """Execute the complete RAG pipeline"""
        print("🚀 Starting RAG Pipeline for Loan Insight Assistant")
        print("="*80)
        
        # Step 1: Load and validate data
        self._load_data()
        
        # Step 2: Process texts
        self._process_texts()
        
        # Step 3: Generate embeddings
        self._generate_embeddings()
        
        # Step 4: Create vector store
        self._create_vector_store()
        
        # Step 5: Save artifacts
        self._save_artifacts()
        
        # Step 6: Test the system
        self._test_search()
        
        print("\n" + "="*80)
        print("✅ Pipeline completed successfully!")
        print(f"📁 All outputs saved to: {self.output_dir}")
        print("="*80)
        
        return self
    
    def _load_data(self):
        """Step 1: Load data"""
        print("\n" + "="*80)
        print("STEP 1: DATA LOADING")
        print("="*80)
        
        self.data_loader = LoanDataLoader(self.csv_path)
        self.data_loader.load_data()
        
        self.df = self.data_loader.get_dataframe()
        
        # Store basic info
        self.validation_report['total_records'] = len(self.df)
        self.validation_report['total_columns'] = len(self.df.columns)
        
        return self
    
    def _process_texts(self):
        """Step 2: Process texts and create representations"""
        print("\n" + "="*80)
        print("STEP 2: TEXT PROCESSING AND FEATURE ENGINEERING")
        print("="*80)
        
        self.text_processor = LoanTextProcessor(self.df)
        self.text_processor.create_text_representations()
        
        self.processed_df = self.text_processor.get_processed_dataframe()
        self.texts = self.text_processor.get_text_representations()
        
        # Store basic metadata
        self.validation_report['total_texts'] = len(self.texts)
        self.validation_report['avg_text_length'] = int(sum(len(t) for t in self.texts) / len(self.texts))
        
        return self
    
    def _generate_embeddings(self):
        """Step 3: Generate embeddings"""
        print("\n" + "="*80)
        print("STEP 3: EMBEDDING GENERATION")
        print("="*80)
        
        self.embedding_generator = EmbeddingGenerator(self.model_name)
        self.embeddings = self.embedding_generator.generate_embeddings(
            self.texts,
            batch_size=32,
            normalize=True,
            show_progress=True
        )
        
        # Update validation report
        self.validation_report.update(self.embedding_generator.get_metadata())
        
        return self
    
    def _create_vector_store(self):
        """Step 4: Create FAISS vector store"""
        print("\n" + "="*80)
        print("STEP 4: VECTOR STORE CREATION")
        print("="*80)
        
        self.vector_store = FAISSVectorStore()
        
        # Choose index type based on dataset size
        index_type = 'flat' if len(self.embeddings) < 10000 else 'ivf'
        
        self.vector_store.create_index(
            self.embeddings,
            index_type=index_type,
            nlist=100,
            nprobe=10
        )
        
        # Update validation report
        self.validation_report.update(self.vector_store.get_metadata())
        
        return self
    
    def _save_artifacts(self):
        """Step 5: Save all artifacts to disk"""
        print("\n" + "="*80)
        print("STEP 5: SAVING ARTIFACTS")
        print("="*80)
        print("\n💾 Saving artifacts...")
        
        # 1. Save processed CSV with text representations
        csv_path = self.output_dir / 'processed_loan_data_with_embeddings.csv'
        self.processed_df.to_csv(csv_path, index=False)
        print(f"   ✅ Saved processed CSV: {csv_path}")
        
        # 2. Save FAISS index
        index_path = self.output_dir / 'loan_faiss_index.bin'
        self.vector_store.save_index(index_path)
        
        # 3. Save embeddings
        embeddings_path = self.output_dir / 'loan_embeddings.npy'
        self.embedding_generator.save_embeddings(embeddings_path)
        
        # 4. Save validation report
        self.validation_report['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.validation_report['artifacts'] = {
            'processed_csv': str(csv_path),
            'faiss_index': str(index_path),
            'embeddings': str(embeddings_path)
        }
        
        report_path = self.output_dir / 'validation_report.json'
        with open(report_path, 'w') as f:
            json.dump(self.validation_report, f, indent=2)
        print(f"   ✅ Saved validation report: {report_path}")
        
        # 5. Create human-readable report
        txt_report_path = self.output_dir / 'validation_report.txt'
        self._create_text_report(txt_report_path)
        print(f"   ✅ Saved text report: {txt_report_path}")
        
        return self
    
    def _create_text_report(self, path):
        """Create a human-readable text report"""
        with open(path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("LOAN INSIGHT ASSISTANT - PIPELINE EXECUTION REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Generated: {self.validation_report.get('timestamp', 'N/A')}\n\n")
            
            # Data Overview
            f.write("1. DATA OVERVIEW\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Records: {self.validation_report.get('total_records', 'N/A')}\n")
            f.write(f"Total Columns: {self.validation_report.get('total_columns', 'N/A')}\n")
            f.write(f"Data Quality: {self.validation_report.get('data_quality_score', 'N/A')}\n\n")
            
            # Text Processing
            f.write("2. TEXT PROCESSING\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Texts: {self.validation_report.get('total_texts', 'N/A')}\n")
            f.write(f"Average Length: {self.validation_report.get('avg_text_length', 'N/A'):.0f} chars\n\n")
            
            # Embeddings
            f.write("3. EMBEDDINGS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Model: {self.validation_report.get('model_name', 'N/A')}\n")
            f.write(f"Dimension: {self.validation_report.get('embedding_dimension', 'N/A')}\n")
            f.write(f"Total Embeddings: {self.validation_report.get('total_embeddings', 'N/A')}\n\n")
            
            # Vector Store
            f.write("4. VECTOR STORE\n")
            f.write("-" * 80 + "\n")
            f.write(f"Index Type: {self.validation_report.get('index_type', 'N/A')}\n")
            f.write(f"Total Vectors: {self.validation_report.get('total_vectors', 'N/A')}\n")
            f.write(f"Metric: {self.validation_report.get('metric', 'N/A')}\n\n")
            
            # Artifacts
            f.write("5. OUTPUT ARTIFACTS\n")
            f.write("-" * 80 + "\n")
            artifacts = self.validation_report.get('artifacts', {})
            for key, value in artifacts.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
    
    def _test_search(self):
        """Step 6: Test the search functionality"""
        print("\n" + "="*80)
        print("STEP 6: TESTING SEARCH FUNCTIONALITY")
        print("="*80)
        
        query = "Home loan with high CIBIL score"
        print(f"\n🔍 Testing search with query: '{query}'")
        
        # Encode the query
        query_embedding = self.embedding_generator.encode_query(query, normalize=True)
        
        # Search
        distances, indices = self.vector_store.search(query_embedding, k=3)
        
        print(f"\n📋 Top 3 results:")
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0]), 1):
            print(f"\n{i}. Similarity: {dist:.4f}")
            print(f"   Loan ID: {self.processed_df.iloc[idx]['Loan_ID']}")
            print(f"   Customer: {self.processed_df.iloc[idx]['Customer_Name']}")
            print(f"   Purpose: {self.processed_df.iloc[idx]['Purpose_of_Loan']}")
            print(f"   Status: {self.processed_df.iloc[idx]['Loan_Status']}")
            print(f"   Text: {self.processed_df.iloc[idx]['text_representation'][:150]}...")
        
        return self


def main():
    """Main execution function"""
    # Configuration
    CSV_PATH = 'hdfc_loan_dataset_full_enriched - hdfc_loan_dataset_full_enriched.csv'
    OUTPUT_DIR = './output'
    MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
    
    # Create and run pipeline
    pipeline = LoanRAGPipeline(
        csv_path=CSV_PATH,
        output_dir=OUTPUT_DIR,
        model_name=MODEL_NAME
    )
    
    pipeline.run_full_pipeline()


if __name__ == "__main__":
    main()
