from llm.local_llm import llm


class FuturePlannerAgent:
    """
    Projects future financial readiness with LLM-powered planning advice.
    """

    def plan(self, state, goals, user_context=None):
        income = state["income"]
        expenses = state["total_expenses"]
        emergency_fund = state["emergency_fund"]

        monthly_savings = income - expenses
        plans = {}

        if monthly_savings <= 0:
            plans["status"] = "blocked"
            plans["reason"] = "No positive monthly savings"
            context = {**state, "goals": goals}
            if user_context:
                context.update(user_context)
            plans["llm_advice"] = llm.get_financial_advice(context, "savings")
            return plans

        # Emergency fund goal (6 months)
        target_emergency = expenses * 6
        remaining = max(target_emergency - emergency_fund, 0)
        months_to_emergency = remaining / monthly_savings if monthly_savings > 0 else 999

        plans["emergency_fund"] = {
            "target": round(target_emergency, 2),
            "current": emergency_fund,
            "months_to_reach": round(months_to_emergency, 1),
            "shortfall": round(remaining, 2)
        }

        # Optional user goals (simple timeline)
        goal_plans = []
        for goal in goals:
            amount = goal.get("amount", 0)
            if amount > 0 and monthly_savings > 0:
                months = amount / monthly_savings
                goal_plans.append({
                    "goal": goal.get("name", "Unnamed Goal"),
                    "amount": amount,
                    "months_to_reach": round(months, 1),
                    "monthly_contribution_needed": round(amount / max(months, 1), 2)
                })

        plans["goals"] = goal_plans
        plans["status"] = "planned"
        
        # Get LLM planning advice
        context = {**state, "goals": goals}
        if user_context:
            context.update(user_context)
        plans["llm_advice"] = llm.get_financial_advice(context, "planning")

        return plans
