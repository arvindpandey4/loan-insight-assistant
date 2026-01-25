"""
Enhanced LLM-Powered Routing Agent for Agentic RAG
Routes queries and generates executable code dynamically
Now using Groq API (much faster than Ollama!)
"""

import os
import json
import re
from typing import Tuple, Optional, Any, Dict, List
import pandas as pd
import numpy as np
from groq import Groq
from langchain_core.prompts import PromptTemplate


class LLMRoutingAgent:
    """Routes queries using LLM and generates executable code via Groq API"""
    
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", api_key: Optional[str] = None):
        """
        Initialize LLM Router with Groq API
        
        Parameters:
        -----------
        model_name : str
            Groq model to use. Options:
            - "llama-3.3-70b-versatile" (recommended, fast & accurate)
            - "llama-3.1-70b-versatile"
            - "mixtral-8x7b-32768"
            - "gemma2-9b-it"
        api_key : str, optional
            Groq API key. If None, reads from GROQ_API_KEY environment variable
        """
        self.model_name = model_name
        
        # Get API key
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            print("[ERROR] Groq API key not found!")
            print("Set GROQ_API_KEY environment variable or pass api_key parameter")
            print("Get your free API key at: https://console.groq.com/keys")
            self.available = False
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
                # Test the connection
                self._test_connection()
                self.available = True
                print(f"[OK] LLM Router initialized with Groq ({model_name})")
            except Exception as e:
                print(f"[WARN] Groq API not available ({str(e)}). Fallback: keyword-based routing")
                self.available = False
                self.client = None
    
    def _test_connection(self):
        """Test Groq API connection"""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=self.model_name,
                max_tokens=10
            )
            return True
        except Exception as e:
            raise Exception(f"Groq API connection failed: {str(e)}")
    
    def _call_groq(self, prompt: str, max_tokens: int = 500, temperature: float = 0.1) -> str:
        """
        Call Groq API with error handling
        
        Parameters:
        -----------
        prompt : str
            The prompt to send
        max_tokens : int
            Maximum tokens in response
        temperature : float
            Sampling temperature (0.0 = deterministic, 1.0 = creative)
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that generates precise code and analysis for data queries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[ERROR] Groq API call failed: {str(e)}")
            return None
    
    def route_query(self, query: str) -> str:
        """Determine if query is MATHEMATICAL or SEMANTIC"""
        
        if not self.available:
            return self._keyword_routing(query)
        
        routing_prompt = f"""Classify this query as either MATHEMATICAL or SEMANTIC.

MATHEMATICAL queries require:
- Calculations (average, sum, count, percentage, ratio)
- Aggregations (how many, total, top N)
- Filtering with numeric conditions
- Statistical operations

SEMANTIC queries require:
- Understanding context and patterns
- Analyzing reasons and causes
- Comparing similar cases
- Explaining trends or factors
- Finding related records

Query: {query}

Classification (respond with only one word - either MATHEMATICAL or SEMANTIC):"""
        
        try:
            response = self._call_groq(routing_prompt, max_tokens=10, temperature=0.1)
            
            if response:
                classification = response.strip().upper()
                
                if "MATHEMATICAL" in classification:
                    return "MATHEMATICAL"
                elif "SEMANTIC" in classification:
                    return "SEMANTIC"
            
            return self._keyword_routing(query)
        except:
            return self._keyword_routing(query)
    
    def _keyword_routing(self, query: str) -> str:
        """Fallback keyword-based routing"""
        math_keywords = ['average', 'sum', 'count', 'how many', 'percentage', 
                        'total', 'mean', 'top', 'highest', 'lowest', 'calculate',
                        'what is the', 'how much', 'percent']
        
        query_lower = query.lower()
        if any(kw in query_lower for kw in math_keywords):
            return "MATHEMATICAL"
        return "SEMANTIC"
    
    def generate_pandas_query(self, query: str, df_info: str) -> Tuple[Optional[str], str]:
        """
        Generate Pandas code to execute on DataFrame
        
        Args:
            query: User query
            df_info: JSON string describing DataFrame structure
        
        Returns:
            (executable_code, explanation)
        """
        
        if not self.available:
            return None, "LLM not available for query generation"
        
        pandas_prompt = f"""Generate Python Pandas code to answer this query about loan data.

DataFrame Schema:
{df_info}

User Query: {query}

Requirements:
1. Write code that operates on a DataFrame variable called 'df'
2. Store the final answer in a variable called 'result'
3. Use only pandas and numpy operations
4. Handle missing values appropriately
5. For percentages, multiply by 100
6. For currency, keep as numeric (formatting will be done separately)

Examples:

Query: "What is the average income?"
Code:
result = df['Applicant_Income'].mean()

Query: "How many loans were approved?"
Code:
result = (df['Loan_Status'] == 'Approved').sum()

Query: "What percentage of loans were rejected?"
Code:
total = len(df)
rejected = (df['Loan_Status'] == 'Rejected').sum()
result = (rejected / total) * 100

Query: "Top 5 highest loan amounts"
Code:
result = df.nlargest(5, 'Loan_Amount')[['Customer_Name', 'Loan_Amount']]

Now generate code for the user query. Output ONLY the Python code, no explanations or markdown formatting:"""
        
        try:
            response = self._call_groq(pandas_prompt, max_tokens=300, temperature=0.1)
            
            if response:
                code = self._extract_code(response)
                
                if code:
                    return code, f"Generated Pandas query"
                else:
                    return None, "Could not extract valid code"
            else:
                return None, "No response from Groq API"
        except Exception as e:
            return None, f"Code generation error: {str(e)}"
    
    def generate_semantic_analysis(self, query: str, context: str) -> str:
        """
        Generate semantic analysis using Groq
        
        Args:
            query: User's question
            context: Retrieved document context
        
        Returns:
            Analysis text
        """
        
        if not self.available:
            return f"LLM not available. Retrieved context:\n\n{context}"
        
        analysis_prompt = f"""You are a loan data analyst. Based on the retrieved loan records, provide a detailed analysis answering the user's query.

USER QUERY: {query}

RETRIEVED LOAN RECORDS:
{context}

INSTRUCTIONS:
1. Analyze patterns in the retrieved records
2. Identify key factors (income, credit score, DTI ratio, etc.)
3. Calculate relevant statistics (averages, counts, percentages)
4. Provide insights and conclusions
5. Be specific with numbers and percentages
6. Format your response clearly with sections

ANALYSIS:"""
        
        try:
            response = self._call_groq(analysis_prompt, max_tokens=800, temperature=0.3)
            return response if response else f"Analysis unavailable. Context:\n{context}"
        except Exception as e:
            return f"Analysis error: {str(e)}\n\nRetrieved Context:\n{context}"
    
    def execute_pandas_query(self, code: str, df: pd.DataFrame) -> Tuple[Any, str]:
        """Safely execute generated Pandas query"""
        
        try:
            # Create safe execution environment
            safe_globals = {
                'df': df,
                'pd': pd,
                'np': np,
                '__builtins__': {
                    'len': len,
                    'sum': sum,
                    'min': min,
                    'max': max,
                    'abs': abs,
                    'round': round,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip,
                }
            }
            safe_locals = {}
            
            # Execute code
            exec(code, safe_globals, safe_locals)
            
            # Get result
            result = safe_locals.get('result', None)
            
            if result is None:
                return None, "No result variable found in generated code"
            
            return result, "Executed successfully"
        
        except Exception as e:
            return None, f"Execution error: {str(e)}"
    
    @staticmethod
    def _extract_code(response: str) -> Optional[str]:
        """Extract Python code from LLM response"""
        
        # Try to find code blocks with ```python
        code_match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # Try to find code blocks with ```
        code_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # If no code block, extract lines that look like Python code
        lines = response.split('\n')
        code_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Skip empty lines and obvious explanations
            if not stripped:
                continue
            if stripped.startswith('#'):
                code_lines.append(line)  # Keep comments
                continue
            # Check if line looks like Python code
            if any(keyword in stripped for keyword in ['df[', 'df.', '=', 'result', 'pd.', 'np.']):
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        return None
    
    def get_df_schema(self, df: pd.DataFrame) -> str:
        """Get DataFrame schema as JSON for LLM context"""
        
        # Get basic info
        schema = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': []
        }
        
        # Add column details
        for col in df.columns:
            if col == 'embeddings':  # Skip embeddings column
                continue
            
            col_info = {
                'name': col,
                'type': str(df[col].dtype),
                'non_null_count': int(df[col].notna().sum()),
                'null_count': int(df[col].isna().sum()),
            }
            
            # Add statistics for numeric columns
            if df[col].dtype in ['int64', 'float64']:
                col_info['min'] = float(df[col].min())
                col_info['max'] = float(df[col].max())
                col_info['mean'] = float(df[col].mean())
                col_info['median'] = float(df[col].median())
            
            # Add unique values for categorical columns
            elif df[col].dtype == 'object':
                unique_vals = df[col].unique()
                if len(unique_vals) <= 20:
                    col_info['unique_values'] = unique_vals.tolist()
                else:
                    col_info['unique_count'] = len(unique_vals)
                    col_info['sample_values'] = unique_vals[:5].tolist()
            
            schema['columns'].append(col_info)
        
        return json.dumps(schema, indent=2, default=str)
    
    def explain_decision(self, query: str, classification: str, 
                        generated_code: Optional[str] = None) -> str:
        """Explain routing and code generation decision"""
        
        explanation = f"""
ROUTING DECISION
================
Query: {query}
Classification: {classification}
Path: {'Mathematical Analysis (Pandas)' if classification == 'MATHEMATICAL' else 'Semantic Search & Analysis'}
        """
        
        if generated_code:
            explanation += f"\n\nGenerated Code:\n{'-'*40}\n{generated_code}\n{'-'*40}"
        
        return explanation
    
    def validate_code(self, code: str) -> Tuple[bool, str]:
        """Validate generated code for safety"""
        
        # Forbidden patterns
        forbidden = [
            'import os',
            'import sys', 
            'import subprocess',
            'eval(',
            'exec(',
            'open(',
            '__import__',
            'compile(',
        ]
        
        for pattern in forbidden:
            if pattern in code:
                return False, f"Unsafe pattern detected: {pattern}"
        
        # Check for result variable
        if 'result' not in code:
            return False, "No 'result' variable found in code"
        
        return True, "Code validation passed"


# Simple fallback for when LLM is not available
class KeywordRouter:
    """Simple keyword-based router (fallback)"""
    
    MATH_KEYWORDS = [
        'average', 'mean', 'sum', 'total', 'count', 'how many',
        'percentage', 'percent', '%', 'ratio', 'calculate', 'what is',
        'top', 'highest', 'lowest', 'maximum', 'minimum'
    ]
    
    SEMANTIC_KEYWORDS = [
        'why', 'reason', 'pattern', 'compare', 'analysis', 'risk',
        'factor', 'trend', 'similar', 'related', 'context', 'explain',
        'show', 'find', 'identify'
    ]
    
    @staticmethod
    def route(query: str) -> str:
        """Route query based on keywords"""
        query_lower = query.lower()
        
        math_score = sum(1 for kw in KeywordRouter.MATH_KEYWORDS if kw in query_lower)
        semantic_score = sum(1 for kw in KeywordRouter.SEMANTIC_KEYWORDS if kw in query_lower)
        
        if math_score > semantic_score:
            return "MATHEMATICAL"
        elif semantic_score > math_score:
            return "SEMANTIC"
        else:
            # Default: check for aggregate keywords
            return "MATHEMATICAL" if any(kw in query_lower for kw in 
                ['how many', 'count', 'average', 'total']) else "SEMANTIC"