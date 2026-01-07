"""
Investment Advisor Agent with LLM-powered recommendations
"""
from llm.local_llm import llm
from memory.db import get_connection
from datetime import datetime


class InvestmentAdvisorAgent:
    """
    Provides investment recommendations based on user profile and financial state
    Uses LLM for personalized advice
    """
    
    def __init__(self):
        self.llm = llm
    
    def analyze_portfolio(self, user_id: int, financial_state: dict) -> dict:
        """Analyze current investments and provide recommendations"""
        conn = get_connection()
        cur = conn.cursor()
        
        try:
            # Get existing investments
            cur.execute("""
                SELECT investment_type, SUM(amount) as total_amount, 
                       AVG(expected_return) as avg_return, risk_level
                FROM investments
                WHERE user_id = ?
                GROUP BY investment_type, risk_level
            """, (user_id,))
            
            investments = cur.fetchall()
            portfolio_value = sum(row["total_amount"] for row in investments)
            
            # Get user profile for context
            cur.execute("""
                SELECT age, risk_tolerance, investment_experience, monthly_income
                FROM user_profile WHERE user_id = ?
            """, (user_id,))
            profile = cur.fetchone()
            
            # Build context for LLM
            context = {
                "income": financial_state.get("income", 0),
                "expenses": financial_state.get("total_expenses", 0),
                "savings": financial_state.get("emergency_fund", 0),
                "age": profile["age"] if profile and profile["age"] else 30,
                "risk_tolerance": profile["risk_tolerance"] if profile and profile["risk_tolerance"] else "moderate",
                "investment_experience": profile["investment_experience"] if profile and profile["investment_experience"] else "beginner",
                "current_portfolio": portfolio_value,
                "monthly_savings": financial_state.get("income", 0) - financial_state.get("total_expenses", 0)
            }
            
            # Get LLM advice
            advice = self.llm.get_financial_advice(context, "investment")
            
            # Calculate recommendations
            recommendations = self._calculate_recommendations(context, investments)
            
            return {
                "current_portfolio_value": portfolio_value,
                "existing_investments": [
                    {
                        "type": row["investment_type"],
                        "amount": row["total_amount"],
                        "expected_return": row["avg_return"],
                        "risk": row["risk_level"]
                    }
                    for row in investments
                ],
                "llm_advice": advice,
                "recommendations": recommendations,
                "risk_assessment": self._assess_risk(context, investments)
            }
        
        except Exception as e:
            print(f"Error analyzing portfolio: {e}")
            return {
                "current_portfolio_value": 0,
                "existing_investments": [],
                "llm_advice": "Unable to analyze portfolio at this time.",
                "recommendations": [],
                "risk_assessment": "unknown"
            }
        finally:
            conn.close()
    
    def _calculate_recommendations(self, context: dict, investments: list) -> list:
        """Calculate specific investment recommendations"""
        recommendations = []
        monthly_savings = context.get("monthly_savings", 0)
        age = context.get("age", 30)
        risk_tolerance = context.get("risk_tolerance", "moderate")
        
        if monthly_savings <= 0:
            return [{"type": "warning", "message": "Increase savings before investing"}]
        
        # Emergency fund first
        emergency_fund = context.get("savings", 0)
        monthly_expenses = context.get("expenses", 0)
        target_emergency = monthly_expenses * 6
        
        if emergency_fund < target_emergency:
            recommendations.append({
                "type": "priority",
                "category": "Emergency Fund",
                "amount": min(monthly_savings * 0.5, target_emergency - emergency_fund),
                "message": "Build emergency fund to 6 months expenses"
            })
        
        # Investment allocation based on age and risk
        investable_amount = monthly_savings * 0.5 if emergency_fund >= target_emergency else monthly_savings * 0.3
        
        if risk_tolerance in ["high", "aggressive"]:
            recommendations.append({
                "type": "equity",
                "category": "Equity Mutual Funds (SIP)",
                "amount": investable_amount * 0.7,
                "message": "High growth potential, suitable for long-term"
            })
            recommendations.append({
                "type": "debt",
                "category": "Debt Funds",
                "amount": investable_amount * 0.3,
                "message": "Stability and regular income"
            })
        elif risk_tolerance == "moderate":
            recommendations.append({
                "type": "equity",
                "category": "Balanced/Hybrid Funds",
                "amount": investable_amount * 0.6,
                "message": "Balanced risk-return profile"
            })
            recommendations.append({
                "type": "debt",
                "category": "Debt Funds + Fixed Deposits",
                "amount": investable_amount * 0.4,
                "message": "Capital preservation"
            })
        else:  # conservative
            recommendations.append({
                "type": "debt",
                "category": "Fixed Deposits + Debt Funds",
                "amount": investable_amount * 0.8,
                "message": "Low risk, stable returns"
            })
            recommendations.append({
                "type": "equity",
                "category": "Large Cap Equity Funds",
                "amount": investable_amount * 0.2,
                "message": "Limited equity exposure for growth"
            })
        
        # Tax-saving investments
        if investable_amount > 5000:
            recommendations.append({
                "type": "tax_saving",
                "category": "ELSS (Tax Saving Mutual Funds)",
                "amount": min(150000 / 12, investable_amount * 0.2),  # ₹1.5L per year
                "message": "Tax deduction under Section 80C"
            })
        
        return recommendations
    
    def _assess_risk(self, context: dict, investments: list) -> str:
        """Assess overall portfolio risk"""
        if not investments:
            return "no_investments"
        
        high_risk_count = sum(1 for inv in investments if inv["risk_level"] in ["high", "very_high"])
        total_investments = len(investments)
        
        if high_risk_count / total_investments > 0.6:
            return "high"
        elif high_risk_count / total_investments > 0.3:
            return "moderate"
        else:
            return "low"
    
    def add_investment(self, user_id: int, investment_type: str, amount: float, 
                      expected_return: float, risk_level: str, notes: str = None):
        """Record a new investment"""
        conn = get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                INSERT INTO investments (user_id, investment_type, amount, current_value, 
                                       expected_return, risk_level, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, investment_type, amount, amount, expected_return, risk_level, notes,
                  datetime.utcnow().isoformat()))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding investment: {e}")
            return False
        finally:
            conn.close()

