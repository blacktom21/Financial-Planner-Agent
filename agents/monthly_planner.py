"""
Monthly Planner Agent - Self-sufficient agent that creates comprehensive monthly plans
Based on user input and financial data, creates actionable monthly financial plans
"""
from llm.local_llm import llm
from memory.db import get_connection
from datetime import datetime
from agents.expense_tracker import ExpenseTrackerAgent


class MonthlyPlannerAgent:
    """
    Self-sufficient agent that creates monthly financial plans
    Takes user prompts and financial data to generate comprehensive monthly plans
    """
    
    def __init__(self):
        self.llm = llm
        self.expense_tracker = ExpenseTrackerAgent()
    
    def create_monthly_plan(self, user_id: int, user_prompt: str = None) -> dict:
        """
        Create a comprehensive monthly plan based on user's financial situation
        This is the main self-sufficient planning function
        """
        conn = get_connection()
        cur = conn.cursor()
        
        try:
            # Get user profile
            cur.execute("""
                SELECT monthly_income, emergency_fund, total_emi, age, occupation,
                       financial_goals, risk_tolerance, investment_experience
                FROM user_profile WHERE user_id = ?
            """, (user_id,))
            profile = cur.fetchone()
            
            if not profile:
                return {
                    "status": "error",
                    "message": "Please complete your profile first"
                }
            
            # Get current month expenses
            current_month = datetime.now().strftime("%Y-%m")
            expenses = self.expense_tracker.monthly_summary(user_id, current_month)
            
            # Build comprehensive financial state
            income = profile["monthly_income"] or 0
            total_expenses = expenses.get("total", 0)
            emi = profile["total_emi"] or 0
            emergency_fund = profile["emergency_fund"] or 0
            monthly_savings = income - total_expenses
            
            financial_state = {
                "income": income,
                "total_expenses": total_expenses,
                "total_emi": emi,
                "emergency_fund": emergency_fund,
                "monthly_savings": monthly_savings,
                "age": profile["age"] or 30,
                "occupation": profile["occupation"] or "",
                "financial_goals": profile["financial_goals"] or "",
                "risk_tolerance": profile["risk_tolerance"] or "moderate",
                "expenses_by_category": expenses.get("by_category", {})
            }
            
            # Create comprehensive plan
            plan = {
                "month": current_month,
                "status": "active",
                "generated_at": datetime.utcnow().isoformat(),
                "financial_summary": {
                    "income": income,
                    "expenses": total_expenses,
                    "savings": monthly_savings,
                    "savings_rate": (monthly_savings / income * 100) if income > 0 else 0,
                    "emi_burden": (emi / income * 100) if income > 0 else 0
                },
                "expense_breakdown": expenses.get("by_category", {}),
                "recommendations": self._generate_recommendations(financial_state),
                "action_items": self._generate_action_items(financial_state),
                "budget_allocation": self._suggest_budget_allocation(financial_state),
                "ai_insights": self._get_ai_insights(financial_state, user_prompt)
            }
            
            return plan
        
        except Exception as e:
            print(f"Error creating monthly plan: {e}")
            return {
                "status": "error",
                "message": f"Error creating plan: {str(e)}"
            }
        finally:
            conn.close()
    
    def _generate_recommendations(self, state: dict) -> list:
        """Generate specific recommendations based on financial state"""
        recommendations = []
        income = state.get("income", 0)
        expenses = state.get("total_expenses", 0)
        savings = state.get("monthly_savings", 0)
        emi = state.get("total_emi", 0)
        emergency_fund = state.get("emergency_fund", 0)
        
        # Savings rate recommendations
        savings_rate = (savings / income * 100) if income > 0 else 0
        if savings_rate < 20:
            recommendations.append({
                "priority": "high",
                "category": "Savings",
                "title": "Increase Savings Rate",
                "description": f"Your savings rate is {savings_rate:.1f}%. Aim for at least 20%.",
                "action": "Review expenses and identify areas to cut by 10-15%"
            })
        
        # Emergency fund recommendations
        target_emergency = expenses * 6
        if emergency_fund < target_emergency:
            shortfall = target_emergency - emergency_fund
            recommendations.append({
                "priority": "high",
                "category": "Emergency Fund",
                "title": "Build Emergency Fund",
                "description": f"You need ₹{shortfall:,.0f} more to reach 6 months expenses.",
                "action": f"Save ₹{shortfall/6:,.0f} per month for 6 months"
            })
        
        # EMI recommendations
        emi_ratio = (emi / income * 100) if income > 0 else 0
        if emi_ratio > 40:
            recommendations.append({
                "priority": "high",
                "category": "Debt Management",
                "title": "High EMI Burden",
                "description": f"EMI is {emi_ratio:.1f}% of income (should be <40%).",
                "action": "Consider debt consolidation or increasing income"
            })
        
        # Expense optimization
        if expenses > income * 0.8:
            recommendations.append({
                "priority": "medium",
                "category": "Budget",
                "title": "High Expense Ratio",
                "description": "Expenses are too high relative to income.",
                "action": "Create detailed budget and track every expense"
            })
        
        return recommendations
    
    def _generate_action_items(self, state: dict) -> list:
        """Generate actionable items for the month"""
        actions = []
        savings = state.get("monthly_savings", 0)
        
        if savings > 0:
            actions.append({
                "task": "Set up automatic transfer to savings account",
                "priority": "high",
                "due": "This week"
            })
            actions.append({
                "task": "Review and cancel unused subscriptions",
                "priority": "medium",
                "due": "This month"
            })
            actions.append({
                "task": "Set up SIP for mutual funds",
                "priority": "medium",
                "due": "This month"
            })
        else:
            actions.append({
                "task": "Create detailed expense tracking",
                "priority": "high",
                "due": "Immediately"
            })
            actions.append({
                "task": "Identify and cut unnecessary expenses",
                "priority": "high",
                "due": "This week"
            })
        
        return actions
    
    def _suggest_budget_allocation(self, state: dict) -> dict:
        """Suggest budget allocation based on 50/30/20 rule"""
        income = state.get("income", 0)
        
        if income == 0:
            return {}
        
        return {
            "needs": {
                "percentage": 50,
                "amount": income * 0.5,
                "categories": ["Rent", "EMI", "Groceries", "Utilities", "Insurance"]
            },
            "wants": {
                "percentage": 30,
                "amount": income * 0.3,
                "categories": ["Entertainment", "Dining", "Shopping", "Hobbies"]
            },
            "savings": {
                "percentage": 20,
                "amount": income * 0.2,
                "categories": ["Emergency Fund", "Investments", "Retirement"]
            }
        }
    
    def _get_ai_insights(self, state: dict, user_prompt: str = None) -> str:
        """Get AI-powered insights based on financial state and user prompt"""
        context = {
            **state,
            "user_query": user_prompt or "Create a monthly financial plan for me"
        }
        
        # Build comprehensive prompt for LLM
        prompt_context = f"""
        User's Financial Situation:
        - Monthly Income: ₹{state.get('income', 0):,.0f}
        - Monthly Expenses: ₹{state.get('total_expenses', 0):,.0f}
        - Monthly Savings: ₹{state.get('monthly_savings', 0):,.0f}
        - Emergency Fund: ₹{state.get('emergency_fund', 0):,.0f}
        - EMI: ₹{state.get('total_emi', 0):,.0f}
        - Age: {state.get('age', 30)}
        - Risk Tolerance: {state.get('risk_tolerance', 'moderate')}
        - Financial Goals: {state.get('financial_goals', 'Not specified')}
        
        User's Question/Prompt: {user_prompt or 'Create a comprehensive monthly financial plan'}
        
        Provide specific, actionable monthly financial planning advice. Focus on:
        1. Immediate actions for this month
        2. Budget optimization
        3. Savings and investment strategy
        4. Debt management if applicable
        5. Long-term goal alignment
        """
        
        # Get LLM advice
        advice = self.llm.get_financial_advice(context, "planning")
        
        return advice

