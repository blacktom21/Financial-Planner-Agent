"""
LLM Integration for Financial Advisor
Supports multiple free LLM options:
1. Hugging Face Inference API (free tier)
2. Ollama (local, completely free)
3. Fallback to rule-based responses
"""
import os
import json
import requests
from typing import Dict, Any, Optional


class FinancialLLM:
    """Wrapper for LLM services to provide financial advice"""
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "huggingface")  # huggingface, ollama, or none
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model_name = os.getenv("LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
    
    def _call_huggingface(self, prompt: str) -> str:
        """Call Hugging Face Inference API (free tier available)"""
        if not self.hf_api_key:
            return None
        
        try:
            api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
            headers = {
                "Authorization": f"Bearer {self.hf_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                return str(result)
            return None
        except Exception as e:
            print(f"Hugging Face API error: {e}")
            return None
    
    def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama instance"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "mistral",  # or llama2, codellama, etc.
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            return None
        except Exception as e:
            print(f"Ollama API error: {e}")
            return None
    
    def get_financial_advice(self, context: Dict[str, Any], question_type: str = "general") -> str:
        """
        Get personalized financial advice based on user context
        
        Args:
            context: User's financial data (income, expenses, savings, etc.)
            question_type: Type of advice needed (investment, savings, debt, planning)
        """
        # Build comprehensive prompt
        prompt = self._build_prompt(context, question_type)
        
        # Try to get LLM response
        response = None
        if self.provider == "huggingface":
            response = self._call_huggingface(prompt)
        elif self.provider == "ollama":
            response = self._call_ollama(prompt)
        
        # Fallback to rule-based advice if LLM fails
        if not response or len(response.strip()) < 10:
            response = self._get_rule_based_advice(context, question_type)
        
        return response.strip()
    
    def _build_prompt(self, context: Dict[str, Any], question_type: str) -> str:
        """Build a detailed prompt for the LLM"""
        income = context.get("income", 0)
        expenses = context.get("total_expenses", 0)
        savings = context.get("emergency_fund", 0)
        emi = context.get("total_emi", 0)
        age = context.get("age", 30)
        goals = context.get("goals", [])
        
        prompt = f"""You are a professional financial advisor. Provide concise, actionable financial advice.

User Profile:
- Age: {age}
- Monthly Income: ₹{income:,.0f}
- Monthly Expenses: ₹{expenses:,.0f}
- Emergency Fund: ₹{savings:,.0f}
- Total EMI: ₹{emi:,.0f}
- Savings Rate: {((income - expenses) / income * 100) if income > 0 else 0:.1f}%
- Financial Goals: {', '.join([g.get('name', '') for g in goals]) if goals else 'Not specified'}

Question Type: {question_type}

Provide specific, practical advice in 2-3 short paragraphs. Focus on:
1. Immediate actionable steps
2. Risk assessment
3. Long-term planning suggestions

Advice:"""
        return prompt
    
    def _get_rule_based_advice(self, context: Dict[str, Any], question_type: str) -> str:
        """Fallback rule-based financial advice when LLM is unavailable"""
        income = context.get("income", 0)
        expenses = context.get("total_expenses", 0)
        savings = context.get("emergency_fund", 0)
        emi = context.get("total_emi", 0)
        monthly_savings = income - expenses
        
        advice_parts = []
        
        if question_type == "investment":
            if monthly_savings > 0:
                advice_parts.append(
                    f"With ₹{monthly_savings:,.0f} monthly savings, consider: "
                    "1) Build emergency fund to 6 months expenses, 2) Start SIP in index funds (₹5,000-10,000/month), "
                    "3) Consider tax-saving ELSS funds, 4) Diversify with debt funds for stability."
                )
            else:
                advice_parts.append("Focus on increasing income or reducing expenses before investing.")
        
        elif question_type == "savings":
            target_emergency = expenses * 6
            if savings < target_emergency:
                shortfall = target_emergency - savings
                months = shortfall / monthly_savings if monthly_savings > 0 else 999
                advice_parts.append(
                    f"Build emergency fund: Need ₹{shortfall:,.0f} more. "
                    f"At current savings rate, will take {months:.0f} months. "
                    "Prioritize this before other investments."
                )
        
        elif question_type == "debt":
            emi_ratio = (emi / income * 100) if income > 0 else 0
            if emi_ratio > 40:
                advice_parts.append(
                    f"EMI burden is {emi_ratio:.0f}% of income (high). "
                    "Consider: 1) Debt consolidation, 2) Increase income, 3) Refinance at lower rates."
                )
            else:
                advice_parts.append("Your EMI burden is manageable. Continue regular payments.")
        
        else:  # general planning
            if monthly_savings > 0:
                advice_parts.append(
                    f"Good savings rate. Allocate: 50% to emergency fund, "
                    "30% to equity investments, 20% to debt/insurance."
                )
            else:
                advice_parts.append(
                    "Expenses exceed income. Review: 1) Unnecessary subscriptions, "
                    "2) Dining out frequency, 3) Lifestyle inflation. Create strict budget."
                )
        
        return " ".join(advice_parts) if advice_parts else "Review your financial goals and create a monthly budget plan."


# Global instance
llm = FinancialLLM()

