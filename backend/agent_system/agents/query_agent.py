import json
import os
from typing import Optional
from groq import Groq
from pydantic import ValidationError

from ..schemas import QueryIntentSchema, IntentType, ComplianceTone
from ..prompts import QUERY_ANALYSIS_PROMPT

class QueryUnderstandingAgent:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.client = None
        if self.api_key:
            try:
                # Groq 1.0.0+ initialization
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"[ERROR] Failed to initialize Groq client: {e}")
                self.client = None
        else:
            print("[WARN] Groq API Key missing. QueryUnderstandingAgent will fail.")

    def analyze_query(self, query: str) -> QueryIntentSchema:
        if not self.client:
            return self._fallback_intent(query)

        prompt = QUERY_ANALYSIS_PROMPT.format(query=query)

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON only."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model_name,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Validate with Pydantic
            return QueryIntentSchema(**data)

        except (json.JSONDecodeError, ValidationError) as e:
            print(f"[ERROR] Failed to parse intent: {e}")
            return self._fallback_intent(query)
        except Exception as e:
            print(f"[ERROR] LLM Error: {e}")
            return self._fallback_intent(query)

    def _fallback_intent(self, query: str) -> QueryIntentSchema:
        """Simple keyword fallback"""
        query_lower = query.lower()
        intent = IntentType.GENERAL_INQUIRY
        tone = ComplianceTone.NEUTRAL
        
        if "reject" in query_lower:
            intent = IntentType.WHY_REJECTED
        elif "approve" in query_lower:
            intent = IntentType.WHY_APPROVED
        elif "similar" in query_lower:
            intent = IntentType.SIMILAR_CASES
        elif "risk" in query_lower:
            intent = IntentType.RISK_ANALYSIS
        
        if "audit" in query_lower:
            tone = ComplianceTone.AUDIT

        return QueryIntentSchema(
            intent=intent,
            compliance_tone=tone,
            confidence_score=0.5
        )
