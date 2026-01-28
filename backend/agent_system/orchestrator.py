from typing import Optional
from .schemas import UserQueryInput, FinalResponseSchema, IntentType
from .agents.query_agent import QueryUnderstandingAgent
from .agents.explanation_agent import ExplanationAgent
from .retrieval_wrapper import retrieval_system
from .golden_kb_handler import golden_kb
from typing import List, Dict, Any

class AgentOrchestrator:
    def __init__(self):
        self.query_agent = QueryUnderstandingAgent()
        self.explanation_agent = ExplanationAgent()
        self.conversation_history: List[Dict[str, Any]] = []
    
        # Ensure retrieval system is ready
        retrieval_system.initialize()

    def pydantic_ai_pipeline(self, user_input: UserQueryInput, conversation_context: List[Dict[str, Any]] = None) -> FinalResponseSchema:
        """
        Main pipeline with Golden KB fast-track and conversation support
        
        Args:
            user_input: User's query
            conversation_context: Optional list of previous messages for context
        """
        query_text = user_input.query_text
        
        # Update conversation history if provided
        if conversation_context:
            self.conversation_history = conversation_context
        
        print(f"\n[Orchestrator] Processing query: {query_text}")
        
        # FAST-TRACK: Check Golden KB first
        golden_answer = golden_kb.get_answer(query_text)
        if golden_answer:
            print("[Orchestrator] ✨ Golden KB match found! Returning curated answer.")
            return FinalResponseSchema(
                query=query_text,
                intent=IntentType.GENERAL,
                retrieved_case_count=0,
                summary=golden_answer,
                evidence_points=["✨ This is a curated answer from our Golden Knowledge Base"],
                risk_notes=[],
                compliance_disclaimer="This information is provided for educational purposes. Please consult with a loan officer for personalized advice.",
                structured_data=[],
                source="golden_kb"
            )
        
        # Step 1: Understand query intent
        print("[Orchestrator] Step 1: Analyzing query intent...")
        intent_schema = self.query_agent.analyze_query(query_text)
        
        # Step 2: Retrieve relevant cases (if needed)
        print(f"[Orchestrator] Step 2: Retrieving cases (intent: {intent_schema.intent})...")
        top_k = intent_schema.top_k_hint or 5
        cases = retrieval_system.retrieve_cases(query_text, top_k=top_k, filters=intent_schema.filters)
        print(f"[Orchestrator] Retrieved {len(cases)} cases")
        
        # Step 3: Generate explanation with conversation context
        print("[Orchestrator] Step 3: Generating explanation...")
        
        # Add conversation context to the explanation
        context_summary = ""
        if self.conversation_history:
            context_summary = "\n\nConversation Context:\n"
            for msg in self.conversation_history[-3:]:  # Last 3 messages for context
                role = msg.get('role', 'user')
                content = msg.get('content', '')[:100]  # Truncate for brevity
                context_summary += f"{role}: {content}...\n"
        
        enriched_query = query_text + context_summary if context_summary else query_text
        final_response = self.explanation_agent.generate_explanation(enriched_query, intent_schema, cases)
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': query_text
        })
        self.conversation_history.append({
            'role': 'assistant',
            'content': final_response.summary
        })
        
        print("[Orchestrator] ✅ Pipeline complete\n")
        return final_response
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("[Orchestrator] Conversation history cleared")

def run_orchestrator():
    """Interactive test loop"""
    orchestrator = AgentOrchestrator()
    print("=== Loan Insight Assistant (Conversational Mode) ===")
    print("Type 'exit', 'quit', or 'clear' to manage conversation\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Assistant: Goodbye! Have a great day!")
                break
            
            if query.lower() == 'clear':
                orchestrator.clear_history()
                print("Assistant: Conversation history cleared. Starting fresh!\n")
                continue
            
            user_input = UserQueryInput(query_text=query)
            response = orchestrator.pydantic_ai_pipeline(user_input)
            
            print(f"\nAssistant: {response.summary}\n")
            
            if response.evidence_points:
                print("📊 Key Points:")
                for point in response.evidence_points[:3]:
                    print(f"  • {point}")
                print()
            
        except KeyboardInterrupt:
            print("\n\nAssistant: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_orchestrator()
