from typing import Dict
import pandas as pd
from agent_system.retrieval_wrapper import retrieval_system

class AnalyticsService:
    def _get_df(self) -> pd.DataFrame:
        if not retrieval_system.initialized:
            retrieval_system.initialize()
        
        if retrieval_system.df is None:
            # Fallback or empty DF if something went wrong
            return pd.DataFrame()
        return retrieval_system.df

    def get_loan_status_distribution(self) -> Dict[str, int]:
        """
        Returns the count of loans for each status (Approved/Rejected).
        """
        df = self._get_df()
        if df.empty:
            return {}
        return df['Loan_Status'].value_counts().to_dict()

    def get_avg_cibil_by_status(self) -> Dict[str, float]:
        """
        Returns the average CIBIL score for each loan status.
        """
        df = self._get_df()
        if df.empty:
            return {}
        # Group by status and mean of CIBIL
        # Ensure CIBIL_Score is numeric
        if 'CIBIL_Score' not in df.columns:
            return {}
            
        result = df.groupby('Loan_Status')['CIBIL_Score'].mean().to_dict()
        return {k: round(float(v), 2) for k, v in result.items()}

    def get_rejections_by_purpose(self) -> Dict[str, int]:
        """
        Returns the count of rejected loans grouped by purpose.
        """
        df = self._get_df()
        if df.empty:
            return {}
        
        # Filter for Rejected
        if 'Loan_Status' not in df.columns or 'Purpose_of_Loan' not in df.columns:
            return {}

        rejected_df = df[df['Loan_Status'] == ' Rejected'] 
        # Note: Dataset might have leading space in " Rejected" or just "Rejected". 
        # Let's clean or check loosely. The task description implies "Rejected". 
        # I should probably check the CSV or be robust. 
        # I'll strip whitespace from the column to be safe before filtering in a copy.
        
        # A safer way without modifying the global DF too much:
        df_clean = df.copy()
        df_clean['Loan_Status'] = df_clean['Loan_Status'].astype(str).str.strip()
        
        rejected_df = df_clean[df_clean['Loan_Status'] == 'Rejected']
        
        if rejected_df.empty:
            return {}
            
        return rejected_df['Purpose_of_Loan'].value_counts().to_dict()

analytics_service = AnalyticsService()
