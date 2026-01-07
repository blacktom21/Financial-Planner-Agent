from utils.calculations import savings_ratio, emi_ratio, emergency_runway
from datetime import datetime


class RiskAnalyzerAgent:
    """
    This agent evaluates financial risk using deterministic rules.
    No LLM is used for calculations.
    """

    def run(self, financial_state):
        income = financial_state["income"]
        total_expenses = financial_state["total_expenses"]
        total_emi = financial_state["total_emi"]
        emergency_fund = financial_state["emergency_fund"]

        risk_score = 0
        reasons = []

        # Emergency fund risk
        runway = emergency_runway(emergency_fund, total_expenses)
        if runway < 3:
            risk_score += 35
            reasons.append("Emergency fund less than 3 months")

        # EMI burden risk
        emi_load = emi_ratio(income, total_emi)
        if emi_load > 0.4:
            risk_score += 30
            reasons.append("EMI exceeds 40% of income")

        # Savings health
        save_ratio = savings_ratio(income, total_expenses)
        if save_ratio < 0.2:
            risk_score += 25
            reasons.append("Savings rate below 20%")

        # Risk level
        if risk_score >= 70:
            level = "HIGH"
        elif risk_score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "risk_score": min(risk_score, 100),
            "risk_level": level,
            "reasons": reasons,
            "generated_at": datetime.utcnow().isoformat()
        }
