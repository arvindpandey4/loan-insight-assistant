# Loan Insight Assistant - RAG System

A Retrieval-Augmented Generation (RAG) system for intelligent loan data search and analysis using FAISS vector database and Sentence Transformers.

## 🎯 Project Overview

This project implements a complete RAG pipeline that processes loan application data, generates semantic embeddings, and enables intelligent search capabilities. The system allows you to search for similar loan applications using natural language queries.

## ✨ Features

- **Data Exploration & Validation**: Comprehensive data quality checks and statistics
- **Feature Engineering**: Intelligent text representation combining multiple loan attributes
- **Semantic Embeddings**: Using Sentence Transformers (all-MiniLM-L6-v2)
- **FAISS Vector Search**: Fast similarity search with cosine similarity
- **Filtered Search**: Combine semantic search with attribute filters
- **Interactive Search**: Command-line interface for queries

## 📊 Pipeline Components

### 1. Data Processing
- Loads and validates loan dataset (1000 records, 47 columns)
- Creates rich text representations combining:
  - Customer demographics
  - Financial details
  - Credit history
  - Application notes
  - Customer feedback

### 2. Embedding Generation
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Embedding dimension: 384
- Normalized embeddings for cosine similarity

### 3. FAISS Index
- IndexFlatIP for exact cosine similarity search
- Optimized for datasets < 10,000 records
- 1000 vectors indexed

## 📁 Project Structure

```
Loan_Insight_Assistant_RAG/
├── hdfc_loan_dataset_full_enriched - hdfc_loan_dataset_full_enriched.csv  # Input data
│
├── # 🎯 Main Pipeline
├── rag/
│   ├── pipeline_orchestrator.py    # Modular pipeline (Recommended ⭐)
│   ├── data_loader.py              # Data loading & validation
│   ├── text_processor.py           # Text representation & chunking
│   ├── embedding_generator.py      # Embedding generation
│   └── vector_store.py             # FAISS vector store
│
├── # 🔍 Search & Usage
├── search_loans.py                 # Search engine & demo
│
├── # 📊 Output Artifacts
├── output/
│   ├── processed_loan_data_with_embeddings.csv
│   ├── loan_faiss_index.bin
│   ├── loan_embeddings.npy
│   ├── validation_report.json
│   └── validation_report.txt
│
├── # 📚 Documentation
├── README.md                       # This file
├── MODULAR_ARCHITECTURE.md         # Modular design guide
├── PROJECT_SUMMARY.md              # Project summary
├── QUICK_REFERENCE.md              # Quick reference
├── ARCHITECTURE.md                 # System architecture
├── requirements.txt                # Dependencies
└── LICENSE
```

### 🆕 New Modular Structure

The pipeline has been refactored into **separate modules** for better maintainability:

- **`data_loader.py`** - Loads and validates CSV data
- **`text_processor.py`** - Creates text representations
- **`embedding_generator.py`** - Generates embeddings
- **`vector_store.py`** - Manages FAISS index
- **`pipeline_orchestrator.py`** - Orchestrates everything

See [MODULAR_ARCHITECTURE.md](MODULAR_ARCHITECTURE.md) for detailed documentation.

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
```

### Installation

1. Clone the repository:
```bash
cd Loan_Insight_Assistant_RAG
```

2. Create virtual environment (if not already created):
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install pandas numpy sentence-transformers faiss-cpu
```

### Build the RAG Pipeline

**Option 1: Modular Pipeline (Recommended) ⭐**
```bash
.venv\Scripts\python.exe rag\pipeline_orchestrator.py
```

**Option 2: Monolithic Pipeline (Legacy)**
```bash
python build_rag_pipeline.py
```

Both options produce the same results. The modular version offers better code organization and reusability.

This will:
1. ✅ Load and explore the loan dataset
2. ✅ Validate data quality
3. ✅ Create text representations
4. ✅ Generate embeddings using Sentence Transformers
5. ✅ Build FAISS index
6. ✅ Save all artifacts to `output/` directory

### Expected Output

```
🚀 Starting RAG Pipeline for Loan Insight Assistant
================================================================================
📥 Loading data...
✅ Loaded 1000 records with 47 columns

🔍 Exploring data...
✅ Data exploration complete
   - Records: 1000
   - Numeric columns: 20
   - Text columns: 27

✔️  Validating data quality...
✅ Validation complete: Good

📝 Creating text representations...
✅ Created text representations for 1000 records
   Average text length: 580 characters

🤖 Generating embeddings...
✅ Generated 1000 embeddings of dimension 384

📊 Creating FAISS index...
✅ FAISS index created with 1000 vectors

💾 Saving artifacts...
✅ Pipeline completed successfully!
```

## 🔍 Using the Search Engine

### Demo Mode

Run pre-configured demo searches:

```bash
python search_loans.py
```

This demonstrates 5 different search scenarios:
1. Home loans in urban areas
2. Approved loans with excellent credit
3. Business expansion loans
4. Personal loans (filtered by approval status)
5. Urban property loans for young professionals

### Interactive Mode

Launch interactive search:

```bash
python search_loans.py --interactive
```

Example queries:
- `home loan with good credit score`
- `business loan for manufacturing`
- `personal loan for medical emergency`
- `approved loans for salaried professionals`

### Programmatic Usage

```python
from search_loans import LoanSearchEngine

# Initialize search engine
engine = LoanSearchEngine()

# Simple search
results = engine.search("home loan for young professional", k=5)

# Print results
engine.print_results(results)

# Search with filters
results = engine.search_by_filters(
    query="personal loan for salaried professionals",
    filters={'Loan_Status': 'Approved', 'Property_Area': 'Urban'},
    k=3
)
```

## 📋 Deliverables

### 1. Processed CSV
**File**: `output/processed_loan_data_with_embeddings.csv`
- Original data + `text_representation` column
- 1000 records with 48 columns

### 2. FAISS Index
**File**: `output/loan_faiss_index.bin`
- Binary FAISS index file
- IndexFlatIP type (exact search)
- 1000 vectors, 384 dimensions

### 3. Embeddings
**File**: `output/loan_embeddings.npy`
- NumPy array of embeddings
- Shape: (1000, 384)
- Normalized for cosine similarity

### 4. Data Validation Report
**Files**: 
- `output/validation_report.json` (machine-readable)
- `output/validation_report.txt` (human-readable)

**Includes**:
- Data overview (1000 records, 47 columns)
- Data quality score: **Good**
- Missing value analysis
- Loan status distribution (65.3% approved, 34.7% rejected)
- CIBIL score statistics (mean: 653, range: 384-878)
- Sample text representations
- Embedding and index metadata

## 📊 Data Quality Report

### Overview
- **Total Records**: 1,000
- **Total Columns**: 47
- **Numeric Columns**: 20
- **Text Columns**: 27
- **Quality Score**: Good ✅

### Key Statistics
- **Loan Approval Rate**: 65.3%
- **Average CIBIL Score**: 653
- **CIBIL Range**: 384 - 878
- **Average Text Length**: 580 characters

### Missing Values
- Business_Type: 79.9%
- Co-signer_Relationship: 23.4%

## 🔧 Technical Details

### Embedding Model
- **Name**: sentence-transformers/all-MiniLM-L6-v2
- **Dimension**: 384
- **Normalization**: L2 normalized
- **Similarity Metric**: Cosine similarity (via inner product)

### FAISS Configuration
- **Index Type**: IndexFlatIP (exact search)
- **Metric**: METRIC_INNER_PRODUCT (cosine similarity for normalized vectors)
- **Total Vectors**: 1,000

### Search Performance
- **Exact Search**: Sub-millisecond for k=5
- **Scalability**: Can handle up to 10K records efficiently with current config
- **For larger datasets**: Recommend IndexIVFFlat with training

## 🎨 Sample Queries

### Business Use Cases

1. **Find Similar Applications**
   ```python
   results = engine.search("home loan 3000000 rupees good credit score")
   ```

2. **Risk Assessment**
   ```python
   results = engine.search("low income high loan amount rejected")
   ```

3. **Customer Segmentation**
   ```python
   results = engine.search_by_filters(
       "self-employed business owners",
       filters={'Employment_Status': 'Self-Employed'}
   )
   ```

4. **Loan Product Matching**
   ```python
   results = engine.search("young professional first time home buyer")
   ```

## 🛠️ Customization

### Change Embedding Model

Edit `build_rag_pipeline.py`:
```python
pipeline.generate_embeddings(model_name='sentence-transformers/all-mpnet-base-v2')
```

### Adjust Search Parameters

Edit `search_loans.py`:
```python
results = engine.search(query, k=10)  # Return top 10 instead of 5
```

### Add Custom Filters

```python
results = engine.search_by_filters(
    query="your query",
    filters={
        'Loan_Status': 'Approved',
        'CIBIL_Score': lambda x: x > 700,  # Custom condition
        'Property_Area': 'Urban'
    }
)
```

## 📈 Performance Metrics

- **Pipeline Execution Time**: ~45 seconds
- **Embedding Generation**: ~33 seconds (1000 records)
- **Index Creation**: <1 second
- **Search Query Time**: <10ms for top-5 results

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more embedding models
- Implement query expansion
- Add relevance feedback
- Create web interface
- Add LLM integration for answer generation

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Sentence Transformers library
- FAISS by Meta AI
- HDFC Bank loan dataset

## 📧 Contact

For questions or issues, please open a GitHub issue.
