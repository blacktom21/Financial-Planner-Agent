"""
Market Advisor Agent - Provides SIP recommendations based on market conditions
Helps beginners understand market-based investment strategies
"""
from llm.local_llm import llm
from datetime import datetime
import random


class MarketAdvisorAgent:
    """
    Provides market-aware SIP investment recommendations
    Simulates market conditions and suggests appropriate SIP strategies
    """
    
    def __init__(self):
        self.llm = llm
    
    def get_market_condition(self) -> dict:
        """Get current market condition (simulated - can be replaced with real API)"""
        # In production, this would fetch from a real market API
        # For now, we simulate market conditions
        
        conditions = ["bull", "bear", "volatile", "stable"]
        weights = [0.3, 0.2, 0.3, 0.2]  # Probability distribution
        condition = random.choices(conditions, weights=weights)[0]
        
        market_data = {
            "condition": condition,
            "nifty_level": random.randint(18000, 22000),
            "sentiment": "positive" if condition == "bull" else "cautious" if condition == "bear" else "neutral",
            "volatility": "high" if condition == "volatile" else "medium" if condition == "bear" else "low",
            "recommended_strategy": self._get_strategy_for_condition(condition)
        }
        
        return market_data
    
    def _get_strategy_for_condition(self, condition: str) -> str:
        """Get investment strategy based on market condition"""
        strategies = {
            "bull": "Aggressive growth - Increase equity allocation",
            "bear": "Defensive - Focus on large-cap and debt funds",
            "volatile": "Balanced approach - Diversify across asset classes",
            "stable": "Steady accumulation - Continue regular SIPs"
        }
        return strategies.get(condition, "Balanced approach")
    
    def suggest_sip_plan(self, user_id: int, financial_state: dict, user_context: dict = None) -> dict:
        """
        Suggest comprehensive SIP plan based on:
        - Market conditions
        - User's financial situation
        - Risk tolerance
        - Investment goals
        """
        market = self.get_market_condition()
        income = financial_state.get("income", 0)
        monthly_savings = financial_state.get("income", 0) - financial_state.get("total_expenses", 0)
        age = user_context.get("age", 30) if user_context else 30
        risk_tolerance = user_context.get("risk_tolerance", "moderate") if user_context else "moderate"
        investment_experience = user_context.get("investment_experience", "beginner") if user_context else "beginner"
        
        # Calculate investable amount (50% of savings if emergency fund is built, else 30%)
        emergency_fund = financial_state.get("emergency_fund", 0)
        monthly_expenses = financial_state.get("total_expenses", 0)
        target_emergency = monthly_expenses * 6
        
        if emergency_fund >= target_emergency:
            investable_amount = monthly_savings * 0.5
        else:
            investable_amount = monthly_savings * 0.3
        
        # Build SIP recommendations based on market and user profile
        sip_plan = {
            "market_condition": market["condition"],
            "market_sentiment": market["sentiment"],
            "recommended_monthly_investment": round(investable_amount, 0),
            "sip_allocations": self._calculate_sip_allocations(
                investable_amount, risk_tolerance, market["condition"], age, investment_experience
            ),
            "strategy_explanation": self._explain_strategy(market, risk_tolerance, investment_experience),
            "beginner_tips": self._get_beginner_tips(investment_experience),
            "market_insights": market,
            "ai_advice": self._get_ai_sip_advice(financial_state, user_context, market)
        }
        
        return sip_plan
    
    def _calculate_sip_allocations(self, total_amount: float, risk_tolerance: str, 
                                 market_condition: str, age: int, experience: str) -> list:
        """Calculate SIP allocations across different fund types"""
        allocations = []
        
        # Base allocation based on risk tolerance
        if risk_tolerance in ["high", "aggressive"]:
            equity_pct = 0.7
            debt_pct = 0.2
            hybrid_pct = 0.1
        elif risk_tolerance == "moderate":
            equity_pct = 0.5
            debt_pct = 0.3
            hybrid_pct = 0.2
        else:  # conservative
            equity_pct = 0.3
            debt_pct = 0.5
            hybrid_pct = 0.2
        
        # Adjust based on market condition
        if market_condition == "bear":
            equity_pct *= 0.8  # Reduce equity in bear market
            debt_pct += 0.1
            hybrid_pct += 0.1
        elif market_condition == "bull":
            equity_pct = min(equity_pct * 1.1, 0.8)  # Increase equity but cap at 80%
        
        # Adjust for beginners - more conservative
        if experience == "beginner":
            equity_pct *= 0.8
            debt_pct += 0.1
            hybrid_pct += 0.1
        
        # Calculate amounts
        equity_amount = round(total_amount * equity_pct, 0)
        debt_amount = round(total_amount * debt_pct, 0)
        hybrid_amount = round(total_amount * hybrid_pct, 0)
        
        if equity_amount > 0:
            allocations.append({
                "type": "Equity Mutual Funds (SIP)",
                "amount": equity_amount,
                "percentage": round(equity_pct * 100, 1),
                "recommended_funds": self._get_fund_recommendations("equity", market_condition, experience),
                "explanation": "Long-term wealth creation. Higher risk, higher returns."
            })
        
        if hybrid_amount > 0:
            allocations.append({
                "type": "Hybrid/Balanced Funds (SIP)",
                "amount": hybrid_amount,
                "percentage": round(hybrid_pct * 100, 1),
                "recommended_funds": self._get_fund_recommendations("hybrid", market_condition, experience),
                "explanation": "Balanced risk-return. Good for moderate investors."
            })
        
        if debt_amount > 0:
            allocations.append({
                "type": "Debt Funds (SIP)",
                "amount": debt_amount,
                "percentage": round(debt_pct * 100, 1),
                "recommended_funds": self._get_fund_recommendations("debt", market_condition, experience),
                "explanation": "Stable returns with lower risk. Capital preservation."
            })
        
        # Add tax-saving ELSS if amount is sufficient
        if total_amount > 5000:
            elss_amount = min(round(total_amount * 0.15, 0), 12500)  # Max ₹12,500/month for ₹1.5L/year
            if elss_amount > 0:
                allocations.append({
                    "type": "ELSS (Tax Saving) - SIP",
                    "amount": elss_amount,
                    "percentage": round((elss_amount / total_amount) * 100, 1),
                    "recommended_funds": self._get_fund_recommendations("elss", market_condition, experience),
                    "explanation": "Tax deduction under Section 80C. Lock-in period: 3 years."
                })
        
        return allocations
    
    def _get_fund_recommendations(self, fund_type: str, market_condition: str, experience: str) -> list:
        """Get specific fund recommendations based on type and market"""
        recommendations = []
        
        if fund_type == "equity":
            if experience == "beginner":
                recommendations = [
                    "Large Cap Index Funds (Nifty 50)",
                    "Large Cap Active Funds (Top performers)",
                    "Multi Cap Funds (Diversified)"
                ]
            else:
                recommendations = [
                    "Large Cap Funds",
                    "Mid Cap Funds (20-30% allocation)",
                    "Small Cap Funds (10-15% allocation)",
                    "Sectoral Funds (Technology, Banking)"
                ]
        
        elif fund_type == "hybrid":
            recommendations = [
                "Aggressive Hybrid Funds (65% equity)",
                "Balanced Advantage Funds (Dynamic allocation)",
                "Conservative Hybrid Funds (20% equity)"
            ]
        
        elif fund_type == "debt":
            recommendations = [
                "Liquid Funds (Emergency fund)",
                "Short Duration Debt Funds",
                "Corporate Bond Funds",
                "Gilt Funds (Government securities)"
            ]
        
        elif fund_type == "elss":
            recommendations = [
                "Large Cap ELSS Funds",
                "Multi Cap ELSS Funds",
                "Top performing ELSS with 3+ year track record"
            ]
        
        return recommendations
    
    def _explain_strategy(self, market: dict, risk_tolerance: str, experience: str) -> str:
        """Explain the investment strategy in beginner-friendly terms"""
        condition = market["condition"]
        sentiment = market["sentiment"]
        
        explanations = {
            "bull": f"The market is in a {condition} phase with {sentiment} sentiment. "
                   f"This is a good time to continue or slightly increase equity SIPs. "
                   f"However, don't invest more than you can afford to lose.",
            "bear": f"Market is in a {condition} phase. This is actually a good time to start SIPs "
                   f"as you'll buy more units at lower prices (rupee cost averaging). "
                   f"Focus on large-cap funds and maintain discipline.",
            "volatile": f"Market is {condition}. This is normal - markets go up and down. "
                       f"Continue your SIPs regularly. Volatility is your friend in the long term.",
            "stable": f"Market is {condition}. Continue your regular SIPs. "
                     f"Consistency is key to wealth creation."
        }
        
        base_explanation = explanations.get(condition, "Continue regular SIP investments.")
        
        if experience == "beginner":
            base_explanation += " As a beginner, start with smaller amounts and increase gradually. "
            base_explanation += "Focus on large-cap and index funds initially."
        
        return base_explanation
    
    def _get_beginner_tips(self, experience: str) -> list:
        """Get beginner-friendly investment tips"""
        if experience != "beginner":
            return []
        
        return [
            "Start with ₹500-1000 per month SIPs to get comfortable",
            "Choose large-cap or index funds initially (lower risk)",
            "Set up auto-debit for SIPs - discipline is key",
            "Don't check your portfolio daily - review monthly",
            "Invest for at least 5-7 years to see good returns",
            "Don't panic during market downturns - continue SIPs",
            "Increase SIP amount by 10% every year if possible",
            "Diversify across 3-4 funds, not more",
            "Read fund fact sheets before investing",
            "Consider tax-saving ELSS funds for 80C benefits"
        ]
    
    def _get_ai_sip_advice(self, financial_state: dict, user_context: dict, market: dict) -> str:
        """Get AI-powered SIP advice"""
        context = {
            **financial_state,
            **user_context,
            "market_condition": market["condition"],
            "market_sentiment": market["sentiment"]
        }
        
        prompt = f"""
        User wants SIP investment advice. Current market condition: {market['condition']}.
        Provide specific, actionable SIP recommendations for a beginner.
        Focus on:
        1. How much to invest monthly
        2. Which types of funds to choose
        3. How to start (step-by-step)
        4. What to expect
        """
        
        advice = self.llm.get_financial_advice(context, "investment")
        return advice

