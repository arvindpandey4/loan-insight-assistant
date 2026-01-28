# Quick Reference Guide - Loan Insight Assistant RAG

## 🚀 Quick Start (5 Minutes)

### 1. Build the Index
```bash
python build_rag_pipeline.py
```
**Output**: Creates `output/` folder with all artifacts

### 2. Run Demo Searches
```bash
python search_loans.py
```
**Output**: Shows 5 demo searches with results

### 3. Interactive Search
```bash
python search_loans.py --interactive
```
**Usage**: Enter queries, type 'quit' to exit

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `build_rag_pipeline.py` | Main pipeline - generates embeddings & index |
| `search_loans.py` | Search engine with demo & interactive modes |
| `output/loan_faiss_index.bin` | FAISS vector index (1.5 MB) |
| `output/processed_loan_data_with_embeddings.csv` | Data with text representations |
| `output/validation_report.txt` | Human-readable data report |

---

## 💻 Code Snippets

### Basic Search
```python
from search_loans import LoanSearchEngine

engine = LoanSearchEngine()
results = engine.search("home loan with good credit", k=5)
engine.print_results(results)
```

### Filtered Search
```python
results = engine.search_by_filters(
    query="business loan for startup",
    filters={'Loan_Status': 'Approved', 'Property_Area': 'Urban'},
    k=3
)
```

### Access Raw Data
```python
# Get similarity scores and indices only
indices, distances = engine.search("query", k=5, return_details=False)

# Access loan details
loan_record = engine.df.iloc[indices[0]]
print(loan_record['Loan_ID'])
print(loan_record['Customer_Name'])
```

---

## 🔍 Sample Queries

### By Purpose
- "home loan for first time buyer"
- "business expansion loan"
- "personal loan for medical emergency"
- "auto loan with fast approval"
- "education loan for graduate studies"

### By Profile
- "young professional in IT sector"
- "self-employed business owner"
- "salaried employee with family"
- "retired person with pension income"

### By Criteria
- "high CIBIL score approved loans"
- "urban property home loans"
- "low income approved applications"
- "quick disbursal emergency loans"

### By Risk
- "rejected applications with good credit"
- "approved loans with high debt ratio"
- "risky applications requiring review"

---

## 📊 Understanding Results

### Similarity Score
- **Range**: 0.0 to 1.0
- **> 0.5**: Very relevant
- **0.3-0.5**: Moderately relevant
- **< 0.3**: Loosely related

### Result Fields
```python
{
    'similarity_score': 0.5644,      # How similar (0-1)
    'loan_id': 'HDFC100354',          # Unique ID
    'customer_name': 'Saanvi Reddy',  # Customer name
    'purpose': 'Home',                 # Loan purpose
    'loan_amount': 5698029,            # Loan amount (INR)
    'loan_status': 'Approved',         # Approved/Rejected
    'cibil_score': 636,                # Credit score
    'applicant_income': 56000,         # Monthly income
    'employment_status': 'Salaried',   # Employment type
    'property_area': 'Urban',          # Property location
    'text_representation': '...'       # Full text description
}
```

---

## ⚙️ Configuration

### Change Embedding Model
Edit `build_rag_pipeline.py` line ~140:
```python
# Faster but less accurate
pipeline.generate_embeddings('sentence-transformers/all-MiniLM-L6-v2')

# Slower but more accurate
pipeline.generate_embeddings('sentence-transformers/all-mpnet-base-v2')
```

### Adjust Number of Results
Edit `search_loans.py` line ~70:
```python
results = engine.search(query, k=10)  # Change k value
```

### Modify Text Representation
Edit `build_rag_pipeline.py` lines ~130-180 in `create_text_representations()` method

---

## 🐛 Troubleshooting

### Issue: "FAISS index not found"
**Solution**: Run `python build_rag_pipeline.py` first

### Issue: "Model download failed"
**Solution**: Check internet connection, model auto-downloads from Hugging Face

### Issue: "Low similarity scores"
**Solution**: Try more specific queries or check text representation quality

### Issue: "Out of memory"
**Solution**: Reduce batch_size in `generate_embeddings()` method

---

## 📈 Performance Tips

### Faster Searches
- Use IndexIVFFlat for datasets > 10K
- Increase nprobe for better accuracy (slower)
- Decrease nprobe for faster searches (less accurate)

### Better Results
- Use longer, more specific queries
- Include multiple keywords from different aspects
- Combine semantic search with filters
- Try query variations

### Scale to Larger Datasets
```python
# In build_rag_pipeline.py, modify create_faiss_index():
if len(self.embeddings) > 10000:
    quantizer = faiss.IndexFlatIP(dimension)
    nlist = 100  # Number of clusters
    self.index = faiss.IndexIVFFlat(quantizer, dimension, nlist, 
                                     faiss.METRIC_INNER_PRODUCT)
    self.index.train(self.embeddings)
    self.index.nprobe = 20  # Clusters to search
```

---

## 🧪 Testing

### Verify Installation
```bash
python -c "import pandas, numpy, faiss, sentence_transformers; print('✅ All packages installed')"
```

### Check Index
```python
import faiss
index = faiss.read_index('output/loan_faiss_index.bin')
print(f"Vectors in index: {index.ntotal}")  # Should be 1000
```

### Validate Data
```bash
python -c "import pandas as pd; df = pd.read_csv('output/processed_loan_data_with_embeddings.csv'); print(f'✅ Loaded {len(df)} records')"
```

---

## 📦 Dependencies

```txt
pandas>=1.5.0
numpy>=1.23.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
```

**Install all**:
```bash
pip install pandas numpy sentence-transformers faiss-cpu
```

---

## 🎯 Common Use Cases

### 1. Find Similar Applications
```python
# For risk assessment
results = engine.search("loan application just like this one", k=5)
```

### 2. Customer Service
```python
# Find similar past cases
results = engine.search("customer complaint about slow approval", k=3)
```

### 3. Loan Matching
```python
# Match customer to loan type
results = engine.search_by_filters(
    "25 year old IT professional first home",
    filters={'Loan_Status': 'Approved', 'Property_Area': 'Urban'}
)
```

### 4. Pattern Analysis
```python
# Find common patterns in rejections
results = engine.search_by_filters(
    "rejected due to credit score",
    filters={'Loan_Status': 'Rejected'}
)
```

---

## 📞 Support

### Common Questions

**Q: How do I add new loan records?**
A: Add to CSV, re-run `build_rag_pipeline.py`

**Q: Can I use custom embedding models?**
A: Yes, pass any `sentence-transformers` model name

**Q: How to integrate with existing systems?**
A: Use `LoanSearchEngine` class in your Python code

**Q: Is GPU acceleration supported?**
A: Yes, install `faiss-gpu` instead of `faiss-cpu`

**Q: How to deploy as API?**
A: Wrap `LoanSearchEngine` in Flask/FastAPI

---

## 🔗 Resources

- [Sentence Transformers Docs](https://www.sbert.net/)
- [FAISS Documentation](https://faiss.ai/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

## 📄 File Structure

```
Loan_Insight_Assistant_RAG/
├── build_rag_pipeline.py              # Pipeline builder
├── search_loans.py                    # Search engine
├── hdfc_loan_dataset_full_enriched - hdfc_loan_dataset_full_enriched.csv
├── output/
│   ├── loan_faiss_index.bin          # Vector index
│   ├── processed_loan_data_with_embeddings.csv
│   ├── loan_embeddings.npy           # Embeddings backup
│   ├── validation_report.json        # Machine-readable report
│   └── validation_report.txt         # Human-readable report
├── README.md                          # Full documentation
├── PROJECT_SUMMARY.md                 # Project summary
├── QUICK_REFERENCE.md                 # This file
└── LICENSE
```

---

## ⏱️ Timing Reference

| Task | Time |
|------|------|
| Install dependencies | 2-3 min |
| Build index (first time) | ~45 sec |
| Load index | < 1 sec |
| Single search query | < 10 ms |
| Demo searches | ~5 sec |

---

**Last Updated**: January 23, 2026
**Status**: ✅ Production Ready
