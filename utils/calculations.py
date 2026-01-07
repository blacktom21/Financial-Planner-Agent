def savings_ratio(income, expenses):
    if income == 0:
        return 0
    return max((income - expenses) / income, 0)


def emi_ratio(income, emi):
    if income == 0:
        return 1
    return emi / income


def emergency_runway(emergency_fund, monthly_expenses):
    if monthly_expenses == 0:
        return float("inf")
    return emergency_fund / monthly_expenses
