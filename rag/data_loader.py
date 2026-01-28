"""
Data Loader Module
Simple data loading from CSV
"""

import pandas as pd


class LoanDataLoader:
    """Simple CSV data loader"""
    
    def __init__(self, csv_path):
        """Initialize data loader with CSV path"""
        self.csv_path = csv_path
        self.df = None
        
    def load_data(self):
        """Load the CSV data"""
        print("📥 Loading data...")
        self.df = pd.read_csv(self.csv_path)
        print(f"✅ Loaded {len(self.df)} records with {len(self.df.columns)} columns")
        return self
    
    def get_dataframe(self):
        """Return the loaded dataframe"""
        return self.df
