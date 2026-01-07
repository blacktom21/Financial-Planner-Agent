class CriticAgent:
    """
    Audits realism and assigns confidence.
    """

    def review(self, state, risk):
        warnings = []
        confidence = 1.0

        income = state["income"]
        expenses = state["total_expenses"]
        emi = state["total_emi"]

        if emi > income:
            warnings.append("EMI exceeds income")
            confidence -= 0.4

        if expenses > income:
            warnings.append("Expenses exceed income")
            confidence -= 0.3

        if income <= 0:
            warnings.append("Invalid income")
            confidence -= 0.5

        return {
            "confidence": max(round(confidence, 2), 0.0),
            "warnings": warnings
        }
