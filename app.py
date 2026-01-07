"""
Financial Advisor AI - Main Application
Professional financial planning system with LLM-powered advice
"""
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from datetime import datetime
import os

from agents.expense_tracker import ExpenseTrackerAgent
from agents.risk_analyzer import RiskAnalyzerAgent
from agents.critic import CriticAgent
from agents.budget_optimizer import BudgetOptimizerAgent
from agents.future_planner import FuturePlannerAgent
from agents.investment_advisor import InvestmentAdvisorAgent
from agents.monthly_planner import MonthlyPlannerAgent
from agents.market_advisor import MarketAdvisorAgent
from auth import register_user, authenticate_user, get_user_profile, update_user_profile, login_required
from memory.db import get_connection

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-2024")

# Custom Jinja2 filter for number formatting
@app.template_filter('currency')
def currency_filter(value):
    """Format number as currency"""
    if value is None:
        return "0"
    try:
        return f"{float(value):,.0f}"
    except (ValueError, TypeError):
        return "0"

@app.template_filter('percent')
def percent_filter(value):
    """Format number as percentage"""
    if value is None:
        return "0.0"
    try:
        return f"{float(value):.1f}"
    except (ValueError, TypeError):
        return "0.0"

# Initialize agents
expense_agent = ExpenseTrackerAgent()
risk_agent = RiskAnalyzerAgent()
critic_agent = CriticAgent()
optimizer_agent = BudgetOptimizerAgent()
future_agent = FuturePlannerAgent()
investment_agent = InvestmentAdvisorAgent()
monthly_planner = MonthlyPlannerAgent()  # Self-sufficient monthly planner
market_advisor = MarketAdvisorAgent()  # Market-aware SIP recommendations


# ==================== AUTHENTICATION ROUTES ====================

@app.route("/")
def index():
    """Redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        success, user_id, message = authenticate_user(username, password)
        
        if success:
            session['user_id'] = user_id
            session['username'] = message
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error=message)
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        full_name = request.form.get("full_name", "").strip()
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters")
        
        success, message = register_user(username, email, password, full_name)
        
        if success:
            return render_template("login.html", success=message)
        else:
            return render_template("register.html", error=message)
    
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))


# ==================== DASHBOARD & MAIN FEATURES ====================

@app.route("/dashboard")
@login_required
def dashboard():
    """Main financial dashboard"""
    user_id = session['user_id']
    current_month = datetime.now().strftime("%Y-%m")
    
    # Get user profile
    profile = get_user_profile(user_id)
    if not profile:
        return redirect(url_for('setup_profile'))
    
    # Get expense summary
    summary = {"by_category": {}, "total": 0}
    try:
        summary_result = expense_agent.monthly_summary(user_id, current_month)
        if summary_result and isinstance(summary_result, dict):
            summary = summary_result
    except Exception:
        pass
    
    # Build financial state
    state = {
        "income": profile.get("income", 0),
        "total_expenses": summary.get("total", 0),
        "total_emi": profile.get("emi", 0),
        "emergency_fund": profile.get("emergency_fund", 0)
    }
    
    # Run all agents
    try:
        risk = risk_agent.run(state)
    except Exception:
        risk = {"risk_score": 0, "risk_level": "LOW", "reasons": [], "generated_at": ""}
    
    try:
        critic = critic_agent.review(state, risk)
    except Exception:
        critic = {"confidence": 0.0, "warnings": []}
    
    try:
        optimizer = optimizer_agent.suggest(
            summary.get("by_category", {}),
            critic.get("confidence", 0),
            financial_context=state
        )
    except Exception:
        optimizer = {"status": "skipped", "reason": "Error in optimization", "suggestions": []}
    
    # Get user context for LLM
    user_context = {
        "age": profile.get("age"),
        "risk_tolerance": profile.get("risk_tolerance"),
        "investment_experience": profile.get("investment_experience")
    }
    
    try:
        future = future_agent.plan(state, [], user_context=user_context)
    except Exception:
        future = {"status": "blocked", "reason": "Error in planning"}
    
    # Get investment analysis
    try:
        investment_analysis = investment_agent.analyze_portfolio(user_id, state)
    except Exception:
        investment_analysis = {
            "current_portfolio_value": 0,
            "existing_investments": [],
            "llm_advice": "Unable to analyze investments.",
            "recommendations": [],
            "risk_assessment": "unknown"
        }
    
    # Generate monthly plan automatically (self-sufficient agent)
    monthly_plan = None
    try:
        monthly_plan = monthly_planner.create_monthly_plan(user_id, "Create a comprehensive monthly financial plan")
    except Exception as e:
        print(f"Error generating monthly plan: {e}")
    
    return render_template(
        "dashboard.html",
        user=session.get('username', 'User'),
        expenses=summary,
        risk=risk,
        critic=critic,
        warnings=critic.get("warnings", []),
        budget=optimizer,
        future=future,
        investment=investment_analysis,
        profile=profile,
        monthly_plan=monthly_plan
    )


@app.route("/setup-profile", methods=["GET", "POST"])
@login_required
def setup_profile():
    """Initial profile setup"""
    user_id = session['user_id']
    
    if request.method == "POST":
        data = request.form
        
        update_data = {
            "income": float(data.get("income", 0)),
            "emi": float(data.get("emi", 0)),
            "emergency_fund": float(data.get("emergency_fund", 0)),
            "age": int(data.get("age", 30)) if data.get("age") else None,
            "occupation": data.get("occupation", ""),
            "risk_tolerance": data.get("risk_tolerance", "moderate"),
            "investment_experience": data.get("investment_experience", "beginner"),
            "financial_goals": data.get("financial_goals", "")
        }
        
        if update_user_profile(user_id, **update_data):
            return redirect(url_for('dashboard'))
        else:
            return render_template("setup_profile.html", error="Failed to save profile")
    
    profile = get_user_profile(user_id)
    return render_template("setup_profile.html", profile=profile)


# ==================== API ROUTES ====================

@app.route("/add-expense", methods=["GET"])
@login_required
def add_expense_page():
    """Expense input page with detailed fields"""
    return render_template("add_expense.html")


@app.route("/api/expenses/add", methods=["POST"])
@login_required
def add_expense():
    """Add expense with detailed information"""
    user_id = session['user_id']
    data = request.json
    
    try:
        expense_agent.add_expense(
            user_id,
            data.get("category", "Other"),
            float(data.get("amount", 0)),
            data.get("month", datetime.now().strftime("%Y-%m")),
            data.get("description", ""),
            data.get("subcategory"),
            data.get("date"),
            data.get("payment_method"),
            data.get("is_recurring", False),
            data.get("tags")
        )
        return jsonify({"status": "success", "message": "Expense added"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/profile/update", methods=["POST"])
@login_required
def update_profile():
    """Update user profile"""
    user_id = session['user_id']
    data = request.json
    
    update_data = {}
    if "income" in data:
        update_data["income"] = float(data["income"])
    if "emi" in data:
        update_data["emi"] = float(data["emi"])
    if "emergency_fund" in data:
        update_data["emergency_fund"] = float(data["emergency_fund"])
    if "age" in data:
        update_data["age"] = int(data["age"])
    if "occupation" in data:
        update_data["occupation"] = data["occupation"]
    if "risk_tolerance" in data:
        update_data["risk_tolerance"] = data["risk_tolerance"]
    if "investment_experience" in data:
        update_data["investment_experience"] = data["investment_experience"]
    if "financial_goals" in data:
        update_data["financial_goals"] = data["financial_goals"]
    
    if update_user_profile(user_id, **update_data):
        return jsonify({"status": "success", "message": "Profile updated"})
    else:
        return jsonify({"status": "error", "message": "Update failed"}), 400


@app.route("/api/investments/add", methods=["POST"])
@login_required
def add_investment():
    """Add investment"""
    user_id = session['user_id']
    data = request.json
    
    try:
        investment_agent.add_investment(
            user_id,
            data.get("investment_type", "Mutual Fund"),
            float(data.get("amount", 0)),
            float(data.get("expected_return", 0)),
            data.get("risk_level", "moderate"),
            data.get("notes", "")
        )
        return jsonify({"status": "success", "message": "Investment added"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/analysis/full", methods=["GET"])
@login_required
def full_analysis():
    """Get comprehensive financial analysis"""
    user_id = session['user_id']
    current_month = datetime.now().strftime("%Y-%m")
    
    profile = get_user_profile(user_id)
    summary = expense_agent.monthly_summary(user_id, current_month)
    
    state = {
        "income": profile.get("income", 0),
        "total_expenses": summary.get("total", 0),
        "total_emi": profile.get("emi", 0),
        "emergency_fund": profile.get("emergency_fund", 0)
    }
    
    risk = risk_agent.run(state)
    critic = critic_agent.review(state, risk)
    optimizer = optimizer_agent.suggest(summary.get("by_category", {}), critic.get("confidence", 0), state)
    future = future_agent.plan(state, [], user_context=profile)
    investment = investment_agent.analyze_portfolio(user_id, state)
    
    return jsonify({
        "risk": risk,
        "critic": critic,
        "budget": optimizer,
        "future": future,
        "investment": investment
    })


@app.route("/api/plan/monthly", methods=["POST"])
@login_required
def create_monthly_plan():
    """Create monthly plan based on user prompt - Self-sufficient agent"""
    user_id = session['user_id']
    data = request.json
    user_prompt = data.get("prompt", "")
    
    # Monthly planner is self-sufficient - it handles everything
    plan = monthly_planner.create_monthly_plan(user_id, user_prompt)
    
    return jsonify(plan)


@app.route("/api/prompt/ask", methods=["POST"])
@login_required
def ask_prompt():
    """Handle user prompts and get AI suggestions"""
    user_id = session['user_id']
    data = request.json
    prompt = data.get("prompt", "").strip()
    
    if not prompt:
        return jsonify({"error": "Please provide a prompt"}), 400
    
    # Get user profile for context
    profile = get_user_profile(user_id)
    current_month = datetime.now().strftime("%Y-%m")
    summary = expense_agent.monthly_summary(user_id, current_month)
    
    state = {
        "income": profile.get("income", 0),
        "total_expenses": summary.get("total", 0),
        "total_emi": profile.get("emi", 0),
        "emergency_fund": profile.get("emergency_fund", 0),
        "age": profile.get("age"),
        "risk_tolerance": profile.get("risk_tolerance"),
        "financial_goals": profile.get("financial_goals", "")
    }
    
    # Determine question type from prompt
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["invest", "investment", "portfolio", "mutual fund", "sip"]):
        question_type = "investment"
    elif any(word in prompt_lower for word in ["save", "savings", "emergency", "fund"]):
        question_type = "savings"
    elif any(word in prompt_lower for word in ["debt", "emi", "loan", "pay"]):
        question_type = "debt"
    elif any(word in prompt_lower for word in ["plan", "monthly", "budget", "allocate"]):
        question_type = "planning"
    else:
        question_type = "general"
    
    # Get AI advice
    from llm.local_llm import llm
    advice = llm.get_financial_advice(state, question_type)
    
    # Also create monthly plan if it's a planning question
    monthly_plan = None
    if "plan" in prompt_lower or "monthly" in prompt_lower:
        monthly_plan = monthly_planner.create_monthly_plan(user_id, prompt)
    
    return jsonify({
        "prompt": prompt,
        "advice": advice,
        "question_type": question_type,
        "monthly_plan": monthly_plan
    })


@app.route("/api/investment/sip-plan", methods=["GET"])
@login_required
def get_sip_plan():
    """Get market-aware SIP investment plan"""
    user_id = session['user_id']
    current_month = datetime.now().strftime("%Y-%m")
    
    profile = get_user_profile(user_id)
    summary = expense_agent.monthly_summary(user_id, current_month)
    
    state = {
        "income": profile.get("income", 0),
        "total_expenses": summary.get("total", 0),
        "total_emi": profile.get("emi", 0),
        "emergency_fund": profile.get("emergency_fund", 0)
    }
    
    user_context = {
        "age": profile.get("age"),
        "risk_tolerance": profile.get("risk_tolerance"),
        "investment_experience": profile.get("investment_experience")
    }
    
    sip_plan = market_advisor.suggest_sip_plan(user_id, state, user_context)
    
    return jsonify(sip_plan)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
