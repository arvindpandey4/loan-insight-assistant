"""
Text Processor Module
Handles text representation and chunking (1 row = 1 chunk)
"""

import pandas as pd
import numpy as np


class LoanTextProcessor:
    """Process loan data into text representations"""
    
    def __init__(self, df):
        """Initialize with a dataframe"""
        self.df = df
        self.processed_df = None
        self.text_representations = []
        
    def create_text_representations(self):
        """Create rich text representations for each loan record"""
        print("\n📝 Creating text representations...")
        
        # Create a copy for processing
        self.processed_df = self.df.copy()
        
        # Create comprehensive text representation for each loan
        self.text_representations = []
        
        for idx, row in self.df.iterrows():
            # Build a natural language description of the loan
            parts = []
            
            # Customer info
            if pd.notna(row.get('Customer_Name')):
                parts.append(f"Customer {row['Customer_Name']}")
            
            # Demographics
            demo_info = []
            if pd.notna(row.get('Gender')):
                demo_info.append(str(row['Gender']))
            if pd.notna(row.get('Age')):
                demo_info.append(f"{row['Age']} years old")
            if pd.notna(row.get('Married')):
                demo_info.append(f"married: {row['Married']}")
            if demo_info:
                parts.append(", ".join(demo_info))
            
            # Employment
            if pd.notna(row.get('Employment_Status')):
                parts.append(f"Employment: {row['Employment_Status']}")
            if pd.notna(row.get('Occupation')):
                parts.append(f"Occupation: {row['Occupation']}")
            
            # Financial details
            if pd.notna(row.get('Applicant_Income')):
                parts.append(f"Applicant income: INR {row['Applicant_Income']:,.0f}")
            if pd.notna(row.get('Loan_Amount')):
                parts.append(f"Loan amount: INR {row['Loan_Amount']:,.0f}")
            if pd.notna(row.get('Purpose_of_Loan')):
                parts.append(f"Purpose: {row['Purpose_of_Loan']}")
            if pd.notna(row.get('Loan_Term_Months')):
                parts.append(f"Term: {row['Loan_Term_Months']} months")
            
            # Credit info
            if pd.notna(row.get('CIBIL_Score')):
                parts.append(f"CIBIL score: {row['CIBIL_Score']}")
            if pd.notna(row.get('Credit_History')):
                parts.append(f"Credit history: {'Good' if row['Credit_History'] == 1 else 'Poor'}")
            
            # Location
            if pd.notna(row.get('Property_Area')):
                parts.append(f"Property area: {row['Property_Area']}")
            if pd.notna(row.get('City')):
                parts.append(f"City: {row['City']}")
            if pd.notna(row.get('State')):
                parts.append(f"State: {row['State']}")
            
            # Loan status
            if pd.notna(row.get('Loan_Status')):
                parts.append(f"Status: {row['Loan_Status']}")
            
            # Application text (if available)
            if pd.notna(row.get('Application_Text')):
                parts.append(f"Application: {row['Application_Text']}")
            
            # Customer feedback
            if pd.notna(row.get('Customer_Feedback')):
                parts.append(f"Feedback: {row['Customer_Feedback']}")
            
            # Agent notes
            if pd.notna(row.get('Agent_Notes')):
                parts.append(f"Notes: {row['Agent_Notes']}")
            
            # Combine all parts
            text_rep = " | ".join(parts)
            self.text_representations.append(text_rep)
            
            # Progress indicator
            if (idx + 1) % 100 == 0:
                print(f"   Processed {idx + 1}/{len(self.df)} records...")
        
        # Add text representation column
        self.processed_df['text_representation'] = self.text_representations
        
        print(f"✅ Created {len(self.text_representations)} text representations")
        
        return self
    
    def chunk_texts(self):
        """
        Core chunking: 1 row = 1 chunk, no overlap
        Returns the same texts (each row is already a complete chunk)
        """
        print(f"\n✂️  Chunking: 1 row = 1 chunk, no overlap")
        print(f"✅ {len(self.text_representations)} chunks ready")
        return self.text_representations
    
    def get_processed_dataframe(self):
        """Return the processed dataframe with text representations"""
        return self.processed_df
    
    def get_text_representations(self):
        """Return the list of text representations"""
        return self.text_representations
    
    def get_metadata(self):
        """Return text processing metadata"""
        return self.metadata
