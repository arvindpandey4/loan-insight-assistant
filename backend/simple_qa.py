"""
Dynamic Agentic RAG with LLM-Driven Query Processing
- LLM routes queries (Mathematical vs Semantic) via Groq API
- LLM generates Pandas queries dynamically
- LLM analyzes semantic search results
- No hardcoded query patterns
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from rag.embedding_generator import EmbeddingGenerator
from rag.vector_store import FAISSVectorStore
from rag.langchain_Retriver import LoanEmbeddings, LoanFAISSVectorStore, LoanRAGRetriever
from rag.llm_router import LLMRoutingAgent

# Paths - adjusted for backend/ folder
OUTPUT_DIR = Path(__file__).parent / "output"
FAISS_INDEX_PATH = OUTPUT_DIR / "loan_faiss_index.bin"
EMBEDDINGS_PATH = OUTPUT_DIR / "loan_embeddings.npy"
CSV_PATH = OUTPUT_DIR / "processed_loan_data_with_embeddings.csv"

def setup_system(groq_api_key: str = None):
    """
    Setup RAG system with Groq API routing
    
    Parameters:
    -----------
    groq_api_key : str, optional
        Groq API key. If None, reads from GROQ_API_KEY environment variable
    """
    
    print("[SETUP] Loading data...", flush=True)
    df = pd.read_csv(CSV_PATH)
    embeddings = np.load(EMBEDDINGS_PATH)
    
    # Store embeddings as column for similarity search
    df['embeddings'] = [embeddings[i] for i in range(len(df))]
    
    print("[SETUP] Initializing Groq API Routing Agent...", flush=True)
    # Use Groq with llama-3.3-70b-versatile (fast and accurate)
    router = LLMRoutingAgent(
        model_name="llama-3.3-70b-versatile",
        api_key=groq_api_key
    )
    
    print("[SETUP] Initializing embedding model...", flush=True)
    embedding_gen = EmbeddingGenerator(model_name='sentence-transformers/all-MiniLM-L6-v2')
    embedding_gen.load_model()
    embedding_gen.embeddings = embeddings
    
    print("[SETUP] Creating FAISS vector store...", flush=True)
    vector_store = FAISSVectorStore()
    vector_store.create_index(embeddings, index_type='flat')
    
    print("[SETUP] Creating LangChain retriever...", flush=True)
    loan_embeddings = LoanEmbeddings(embedding_gen)
    langchain_vs = LoanFAISSVectorStore.from_embeddings(
        texts=df['text_representation'].tolist(),
        embeddings=loan_embeddings,
        df=df,
        index=vector_store.index,
        embedding_array=embeddings
    )
    retriever = LoanRAGRetriever(langchain_vs, embedding_gen, df)
    
    print("[SETUP] System ready!\n", flush=True)
    return router, df, retriever, embedding_gen


def answer_query_dynamically(query: str, router: LLMRoutingAgent, df: pd.DataFrame, 
                             retriever, embedding_gen: EmbeddingGenerator) -> Tuple[str, str]:
    """
    Process query dynamically using LLM routing and generation
    
    Returns:
        (answer, method_used)
    """
    
    # Route query
    classification = router.route_query(query)
    print(f"[ROUTE] Query classified as: {classification}")
    
    if classification == "MATHEMATICAL":
        return _handle_mathematical_dynamic(query, router, df)
    else:
        return _handle_semantic_dynamic(query, router, df, retriever, embedding_gen)


def _handle_mathematical_dynamic(query: str, router: LLMRoutingAgent, 
                                 df: pd.DataFrame) -> Tuple[str, str]:
    """Handle mathematical queries with Groq-generated Pandas code"""
    
    try:
        # Get DataFrame schema for LLM context
        df_schema = router.get_df_schema(df)
        
        # Generate Pandas query dynamically using Groq
        code, explanation = router.generate_pandas_query(query, df_schema)
        
        if not code:
            return "Unable to generate query code. Please rephrase your question.", "Failed"
        
        print(f"\n[GROQ] Generated Code:\n{code}\n")
        
        # Execute query
        result, status = router.execute_pandas_query(code, df)
        
        if result is not None:
            # Format result naturally
            formatted_result = _format_mathematical_result(result, query)
            return formatted_result, "Groq-Generated Pandas Query"
        else:
            return f"Execution Error: {status}", "Failed"
    
    except Exception as e:
        return f"Error processing mathematical query: {str(e)}", "Failed"


def _handle_semantic_dynamic(query: str, router: LLMRoutingAgent, df: pd.DataFrame,
                             retriever, embedding_gen: EmbeddingGenerator) -> Tuple[str, str]:
    """Handle semantic queries using retriever + Groq analysis"""
    
    try:
        # Retrieve similar records
        print(f"\n[SEMANTIC] Retrieving relevant documents...")
        result = retriever.retrieve(query, k=10, return_score=True)
        
        if not result.documents:
            return "No relevant documents found.", "Semantic Retrieval"
        
        # Prepare context for LLM analysis
        context = _prepare_semantic_context(result, df)
        
        # Generate analysis using Groq
        print(f"[GROQ] Analyzing retrieved documents...")
        analysis = router.generate_semantic_analysis(query, context)
        
        return analysis, "Semantic Retrieval + Groq Analysis"
    
    except Exception as e:
        return f"Error in semantic query: {str(e)}", "Failed"


def _prepare_semantic_context(result, df: pd.DataFrame) -> str:
    """Prepare retrieved documents as context for LLM"""
    
    context_parts = []
    context_parts.append(f"Retrieved {len(result.documents)} relevant loan records:\n")
    
    for i, (doc, score) in enumerate(zip(result.documents, result.scores), 1):
        meta = doc.metadata
        context_parts.append(f"\nRecord {i} (Similarity: {score:.3f}):")
        context_parts.append(f"- Customer: {meta.get('Customer_Name', 'N/A')}")
        context_parts.append(f"- Loan Status: {meta.get('Loan_Status', 'N/A')}")
        context_parts.append(f"- Loan Amount: INR {meta.get('Loan_Amount', 'N/A')}")
        context_parts.append(f"- Income: INR {meta.get('Applicant_Income', 'N/A')}")
        context_parts.append(f"- Credit Score: {meta.get('CIBIL_Score', 'N/A')}")
        context_parts.append(f"- DTI Ratio: {meta.get('Debt_to_Income_Ratio', 'N/A')}")
        
        # Add other relevant fields
        for key in ['Age', 'Employment_Type', 'Loan_Purpose']:
            if key in meta:
                context_parts.append(f"- {key}: {meta[key]}")
    
    return "\n".join(context_parts)


def _format_mathematical_result(result: Any, query: str) -> str:
    """Format mathematical query results naturally"""
    
    if isinstance(result, (int, float)):
        # Determine if it's a percentage, currency, or count
        query_lower = query.lower()
        
        if 'percentage' in query_lower or 'percent' in query_lower or '%' in query_lower:
            return f"Result: {result:.2f}%"
        elif 'income' in query_lower or 'amount' in query_lower or 'loan' in query_lower:
            return f"Result: INR {result:,.2f}"
        elif 'count' in query_lower or 'how many' in query_lower:
            return f"Result: {int(result)}"
        else:
            return f"Result: {result:,.2f}"
    
    elif isinstance(result, pd.Series):
        if len(result) <= 10:
            formatted = "\n".join([f"- {idx}: {val}" for idx, val in result.items()])
            return f"Results:\n{formatted}"
        else:
            formatted = "\n".join([f"- {idx}: {val}" for idx, val in result.head(10).items()])
            return f"Top 10 Results:\n{formatted}\n... ({len(result)} total)"
    
    elif isinstance(result, pd.DataFrame):
        if len(result) <= 10:
            return f"Results:\n{result.to_string()}"
        else:
            return f"Top 10 Results:\n{result.head(10).to_string()}\n... ({len(result)} total rows)"
    
    elif isinstance(result, list):
        if len(result) <= 10:
            return "Results:\n" + "\n".join([f"- {item}" for item in result])
        else:
            return "Top 10 Results:\n" + "\n".join([f"- {item}" for item in result[:10]]) + f"\n... ({len(result)} total)"
    
    else:
        return f"Result: {str(result)}"


def main():
    """Main execution with dynamic Groq-driven query processing"""
    print("\n" + "="*80)
    print("DYNAMIC AGENTIC RAG - GROQ API POWERED")
    print("="*80 + "\n")
    
    # Check for Groq API key
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        print("âš ï¸  WARNING: GROQ_API_KEY not found in environment variables")
        print("Get your free API key at: https://console.groq.com/keys")
        print("Set it with: export GROQ_API_KEY='your-api-key-here'")
        print("\nContinuing with keyword-based routing (limited functionality)...\n")
    
    # Setup
    router, df, retriever, embedding_gen = setup_system(groq_api_key)
    
    # Interactive mode or sample queries
    print("\n" + "="*80)
    print("INTERACTIVE QUERY MODE")
    print("="*80)
    print("Enter your queries (or press Enter to use sample queries)")
    print("Type 'exit' to quit\n")
    
    # Get user input
    user_query = input("Your query: ").strip()
    
    if user_query and user_query.lower() != 'exit':
        queries = [user_query]
    else:
        # Sample queries for demonstration
        queries = [
            "What is the average income of loan applicants?",
            "How many loans were rejected in total?",
            "What percentage of applicants with high income were rejected?",
            "List the top 5 highest loan amounts that were successfully approved",
            "Why are most home loans rejected?",
            "Show similar past cases to rejected applications",
            "What risk factors appear most often in rejected loans?",
            "How do rejected applicants compare to approved profiles?",
            "What is the correlation between credit score and loan approval?",
            "Analyze the pattern of rejections for low credit scores"
        ]
    
    # Process queries dynamically
    for idx, query in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"QUERY {idx}: {query}")
        print(f"{'='*80}\n")
        
        # Route and process with Groq
        answer, method = answer_query_dynamically(query, router, df, retriever, embedding_gen)
        
        print(f"METHOD: {method}")
        print(f"\nANSWER:\n{answer}\n")
    
    # Summary
    print(f"\n{'='*80}")
    print("EXECUTION SUMMARY")
    print(f"{'='*80}\n")
    print(f"[OK] Total Queries: {len(queries)}")
    print(f"[OK] System Type: Dynamic Agentic RAG (Groq-Powered)")
    print(f"[OK] Router: Groq API-based query classification")
    print(f"[OK] Mathematical Queries: Groq-generated Pandas code")
    print(f"[OK] Semantic Queries: Retrieval + Groq analysis")
    print(f"[OK] Data Records: {len(df):,}")
    print(f"[OK] Approved: {(df['Loan_Status'] == 'Approved').sum()}")
    print(f"[OK] Rejected: {(df['Loan_Status'] == 'Rejected').sum()}")
    print(f"\n[OK] ALL QUERIES PROCESSED DYNAMICALLY WITH GROQ!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()