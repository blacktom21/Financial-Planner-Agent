# 💰 Financial Advisor AI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, AI-powered financial planning system that acts as your personal financial advisor. Get personalized advice on investments, savings, debt management, and expense optimization through a multi-agent system powered by LLM technology.

## 🌟 Features

### Core Features
- 🔐 **User Authentication** - Secure login and registration
- 📊 **Financial Dashboard** - Comprehensive overview of financial health
- 💰 **Expense Tracking** - Detailed expense tracking with categories, payment methods, and tags
- 📈 **Risk Analysis** - Automated risk assessment with actionable warnings
- 💼 **Investment Advisor** - AI-powered investment recommendations
- 📅 **Monthly Planning** - Self-sufficient agent creates comprehensive monthly plans
- 🎯 **Goal Planning** - Timeline-based financial goal planning
- 🤖 **LLM-Powered Advice** - Personalized financial advice using free LLM models

### Advanced Features
- 📊 **Market-Aware SIP Plans** - Investment recommendations based on market conditions
- 🏷️ **Detailed Expense Tracking** - Track subcategories, payment methods, recurring expenses
- 💡 **Beginner-Friendly** - Clear explanations and step-by-step guidance
- 🔄 **Auto-Generated Plans** - Monthly plans created automatically on dashboard
- 💬 **Interactive Prompts** - Ask questions and get AI-powered responses

## 🏗️ Architecture

This project uses a **multi-agent system architecture** where specialized agents work together:

- **Expense Tracker Agent** - Records and aggregates expenses
- **Risk Analyzer Agent** - Calculates financial risk scores
- **Budget Optimizer Agent** - Suggests expense reductions
- **Future Planner Agent** - Plans for financial goals
- **Investment Advisor Agent** - Provides investment recommendations
- **Market Advisor Agent** - Market-aware SIP recommendations
- **Monthly Planner Agent** - Self-sufficient monthly planning
- **Critic Agent** - Validates data and assigns confidence

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
- **[THEORY.md](THEORY.md)** - Theoretical foundation and concepts
- **[SETUP.md](SETUP.md)** - Detailed setup instructions

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial_agentic_ai.git
   cd financial_agentic_ai
   ```

2. **Create virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open browser: `http://127.0.0.1:5000`
   - Register a new account
   - Complete your financial profile
   - Start using the dashboard!

## ⚙️ Configuration

### LLM Setup (Optional but Recommended)

The system supports multiple free LLM options:

#### Option 1: Hugging Face (Free Tier)
1. Get API key from [Hugging Face](https://huggingface.co/settings/tokens)
2. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:HUGGINGFACE_API_KEY="your-api-key-here"
   
   # Linux/Mac
   export HUGGINGFACE_API_KEY="your-api-key-here"
   ```

#### Option 2: Ollama (Local, Completely Free)
1. Install [Ollama](https://ollama.ai/)
2. Download a model:
   ```bash
   ollama pull mistral
   ```
3. Set environment variables:
   ```bash
   $env:OLLAMA_URL="http://localhost:11434"
   $env:LLM_PROVIDER="ollama"
   ```

#### Option 3: Rule-Based (No LLM)
If no LLM is configured, the system uses intelligent rule-based advice (still very useful!).

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Secret key for Flask sessions (change in production!)
SECRET_KEY=your-secret-key-here

# LLM Configuration
LLM_PROVIDER=huggingface  # or "ollama" or "none"
HUGGINGFACE_API_KEY=your-hf-key
OLLAMA_URL=http://localhost:11434
LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

## 📖 Usage Guide

### First Time Setup

1. **Register Account**
   - Go to `/register`
   - Create account with username, email, and password

2. **Complete Profile**
   - Enter monthly income, EMI, emergency fund
   - Set age, occupation, risk tolerance
   - Define financial goals

3. **Track Expenses**
   - Click "Add Expense" on dashboard
   - Fill in detailed information:
     - Category and subcategory
     - Amount and date
     - Payment method
     - Description and tags
     - Mark if recurring

4. **View Dashboard**
   - Auto-generated monthly plan
   - Risk analysis
   - Budget recommendations
   - Investment suggestions
   - SIP plans based on market conditions

### Key Features

#### Expense Tracking
- **Detailed Tracking**: Category, subcategory, payment method, tags
- **Recurring Expenses**: Mark subscriptions and regular payments
- **Monthly Summaries**: Automatic categorization and totals

#### Investment Planning
- **SIP Recommendations**: Market-aware investment plans
- **Portfolio Analysis**: Current investments review
- **Fund Suggestions**: Specific fund recommendations
- **Beginner Tips**: Step-by-step guidance

#### Financial Planning
- **Monthly Plans**: Auto-generated comprehensive plans
- **Goal Planning**: Timeline-based goal achievement
- **Risk Assessment**: Financial health scoring
- **Budget Optimization**: Expense reduction suggestions

#### AI Advisor
- **Interactive Prompts**: Ask any financial question
- **Personalized Advice**: Context-aware responses
- **Market Insights**: Current market condition analysis

## 🛠️ Project Structure

```
financial_agentic_ai/
├── app.py                 # Main Flask application
├── auth.py                # Authentication system
├── config.py              # Configuration
├── init_db.py             # Database initialization
├── fix_db.py              # Database migration script
├── requirements.txt       # Python dependencies
│
├── agents/                # AI Agents
│   ├── expense_tracker.py
│   ├── risk_analyzer.py
│   ├── critic.py
│   ├── budget_optimizer.py
│   ├── future_planner.py
│   ├── investment_advisor.py
│   ├── market_advisor.py
│   └── monthly_planner.py
│
├── llm/                   # LLM Integration
│   └── local_llm.py
│
├── memory/                # Database
│   ├── db.py
│   ├── schema.sql
│   └── finance.db
│
├── templates/             # HTML Templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── setup_profile.html
│   └── add_expense.html
│
├── static/                # Static files
│   └── charts.js
│
└── utils/                  # Utilities
    └── calculations.py
```

## 🔌 API Endpoints

### Authentication
- `GET /` - Redirects to login or dashboard
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /register` - Registration page
- `POST /register` - Create new account
- `GET /logout` - Logout user

### Dashboard
- `GET /dashboard` - Main financial dashboard
- `GET /setup-profile` - Profile setup page
- `GET /add-expense` - Expense input page

### API
- `POST /api/expenses/add` - Add expense
- `POST /api/profile/update` - Update user profile
- `POST /api/investments/add` - Add investment
- `GET /api/analysis/full` - Get comprehensive analysis
- `POST /api/plan/monthly` - Create monthly plan
- `POST /api/prompt/ask` - Ask AI advisor
- `GET /api/investment/sip-plan` - Get SIP investment plan

## 🧪 Testing

```bash
# Test database connection
python -c "from memory.db import get_connection; conn = get_connection(); print('Database OK'); conn.close()"

# Test agents
python -c "from agents.monthly_planner import MonthlyPlannerAgent; print('Agents OK')"

# Test app
python -c "from app import app; print('App OK')"
```

## 🔒 Security

- Password hashing (Werkzeug)
- Session-based authentication
- SQL injection prevention (parameterized queries)
- User data isolation
- Input validation

**Note**: Change `SECRET_KEY` in production!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Hugging Face for free LLM API access
- Ollama for local LLM support
- Chart.js for beautiful visualizations

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system details

## 🗺️ Roadmap

- [ ] Real-time market data integration
- [ ] Mobile app
- [ ] Bank account integration
- [ ] Advanced portfolio analytics
- [ ] Tax optimization features
- [ ] Multi-currency support
- [ ] Export reports (PDF/Excel)
- [ ] Email notifications

---

**Built with ❤️ using Flask, SQLite, and AI/LLM technologies**

**Star ⭐ this repo if you find it helpful!**
