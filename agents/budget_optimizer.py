from llm.local_llm import llm


class BudgetOptimizerAgent:
    """
    Suggests expense reductions with LLM-powered budget optimization.
    """

    def suggest(self, expenses_by_category, confidence, financial_context=None):
        if confidence < 0.7:
            return {
                "status": "skipped",
                "reason": "Low confidence in data",
                "suggestions": []
            }

        suggestions = []

        for category, amount in expenses_by_category.items():
            if amount > 0:
                cut = round(amount * 0.15, 2)
                suggestions.append({
                    "category": category,
                    "current": amount,
                    "suggested_reduction": cut,
                    "new_amount": round(amount - cut, 2),
                    "message": f"Reduce {category} by ₹{cut} per month"
                })

        # Get LLM advice for budget optimization
        llm_advice = None
        if financial_context:
            context = {
                **financial_context,
                "expenses_by_category": expenses_by_category
            }
            llm_advice = llm.get_financial_advice(context, "savings")

        return {
            "status": "suggested",
            "suggestions": suggestions,
            "llm_advice": llm_advice,
            "total_potential_savings": sum(s["suggested_reduction"] for s in suggestions)
        }
