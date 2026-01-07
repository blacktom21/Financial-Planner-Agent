# Financial Advisor AI - System Architecture

## Overview

Financial Advisor AI is an intelligent, agent-based financial planning system that uses multiple specialized AI agents to provide comprehensive financial advice. The system is designed to help users manage expenses, plan investments, and achieve financial goals through personalized, AI-powered recommendations.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Login   │  │ Register │  │ Dashboard│  │Add Expense│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer (Flask)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Route Handlers & Controllers             │   │
│  │  - Authentication Routes                              │   │
│  │  - Dashboard Routes                                   │   │
│  │  - API Endpoints                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Agent Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Expense    │  │     Risk     │  │    Budget    │      │
│  │   Tracker    │  │   Analyzer   │  │  Optimizer   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Future     │  │  Investment  │  │   Monthly    │      │
│  │   Planner    │  │   Advisor    │  │   Planner    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    Market    │  │    Critic    │                        │
│  │   Advisor    │  │    Agent     │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      LLM Integration Layer                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         FinancialLLM (Hugging Face / Ollama)          │   │
│  │  - Provides AI-powered financial advice              │   │
│  │  - Fallback to rule-based recommendations            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              SQLite Database (finance.db)             │   │
│  │  - Users & Authentication                             │   │
│  │  - User Profiles                                      │   │
│  │  - Expenses (detailed tracking)                      │   │
│  │  - Investments                                        │   │
│  │  - Risk Reports                                       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent Layer

#### Expense Tracker Agent
- **Purpose**: Records and aggregates user expenses
- **Responsibilities**:
  - Add expenses with detailed information
  - Categorize expenses
  - Generate monthly summaries
  - Track payment methods and patterns
- **Data Flow**: User Input → Database → Aggregated Reports

#### Risk Analyzer Agent
- **Purpose**: Evaluates financial risk using deterministic rules
- **Responsibilities**:
  - Calculate risk scores (0-100)
  - Assess emergency fund adequacy
  - Analyze EMI burden
  - Evaluate savings rate
- **Output**: Risk level (LOW/MEDIUM/HIGH), score, reasons

#### Budget Optimizer Agent
- **Purpose**: Suggests expense reductions and optimizations
- **Responsibilities**:
  - Analyze expenses by category
  - Suggest specific reductions
  - Calculate potential savings
  - Provide LLM-powered budget advice
- **Output**: Suggestions with amounts, LLM advice

#### Future Planner Agent
- **Purpose**: Projects future financial readiness
- **Responsibilities**:
  - Calculate emergency fund timelines
  - Plan for financial goals
  - Project monthly contributions needed
  - Provide planning advice
- **Output**: Goal timelines, monthly contributions, advice

#### Investment Advisor Agent
- **Purpose**: Provides investment recommendations
- **Responsibilities**:
  - Analyze current portfolio
  - Suggest investment allocations
  - Assess portfolio risk
  - Provide personalized advice
- **Output**: Portfolio analysis, recommendations, risk assessment

#### Market Advisor Agent
- **Purpose**: Market-aware SIP investment recommendations
- **Responsibilities**:
  - Analyze market conditions (bull/bear/volatile/stable)
  - Calculate SIP allocations based on market
  - Suggest specific fund types
  - Provide beginner-friendly explanations
- **Output**: SIP plan, allocations, fund recommendations, tips

#### Monthly Planner Agent
- **Purpose**: Self-sufficient agent for comprehensive monthly planning
- **Responsibilities**:
  - Create complete monthly financial plans
  - Generate recommendations
  - Create action items
  - Suggest budget allocations
  - Provide AI insights
- **Output**: Complete monthly plan with all components

#### Critic Agent
- **Purpose**: Validates financial data and assigns confidence
- **Responsibilities**:
  - Check data consistency
  - Identify unrealistic values
  - Assign confidence scores
  - Generate warnings
- **Output**: Confidence score, warnings list

### 2. LLM Integration

#### FinancialLLM Class
- **Providers Supported**:
  - Hugging Face Inference API (free tier)
  - Ollama (local, completely free)
  - Rule-based fallback
- **Functionality**:
  - Context-aware financial advice
  - Question type detection
  - Personalized recommendations
  - Beginner-friendly explanations

### 3. Data Model

#### Database Schema
```
users
├── id (PK)
├── username (UNIQUE)
├── email (UNIQUE)
├── password_hash
└── full_name

user_profile
├── user_id (PK, FK → users)
├── monthly_income
├── emergency_fund
├── total_emi
├── age
├── occupation
├── financial_goals
├── risk_tolerance
└── investment_experience

expenses
├── id (PK)
├── user_id (FK → users)
├── category
├── subcategory
├── amount
├── date
├── month
├── description
├── payment_method
├── is_recurring
└── tags

investments
├── id (PK)
├── user_id (FK → users)
├── investment_type
├── amount
├── current_value
├── expected_return
├── risk_level
└── notes
```

## Data Flow

### Expense Tracking Flow
```
User Input → Expense Form → API Endpoint → Expense Tracker Agent
    → Database → Monthly Summary → Dashboard Display
```

### Financial Analysis Flow
```
User Profile + Expenses → Financial State → Multiple Agents
    → Risk Analysis → Budget Optimization → Investment Advice
    → Monthly Plan → Dashboard Display
```

### SIP Planning Flow
```
User Profile → Market Analysis → SIP Calculations → Allocations
    → Fund Recommendations → Beginner Tips → Dashboard Display
```

## Security Architecture

### Authentication
- Session-based authentication
- Password hashing (Werkzeug)
- Protected routes with `@login_required` decorator
- User data isolation by user_id

### Data Protection
- SQL injection prevention (parameterized queries)
- Input validation
- Error handling without exposing internals

## Scalability Considerations

### Current Design
- SQLite database (suitable for single-user or small deployments)
- Synchronous agent execution
- In-memory session storage

### Future Enhancements
- PostgreSQL for production
- Redis for session management
- Async agent execution
- Caching layer for market data
- Real-time market data integration

## Technology Stack

- **Backend**: Python 3.11+, Flask 3.1.2
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **LLM**: Hugging Face API / Ollama / Rule-based
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Charts**: Chart.js
- **Authentication**: Flask Sessions, Werkzeug Security

## Agent Communication Pattern

Agents follow a **cooperative multi-agent** pattern:
1. Each agent has a specific domain expertise
2. Agents can use outputs from other agents
3. No direct agent-to-agent communication
4. All coordination happens through the application layer
5. Results are aggregated in the dashboard

## Error Handling Strategy

- **Database Errors**: Graceful fallbacks with default values
- **LLM Errors**: Fallback to rule-based recommendations
- **Agent Errors**: Try-catch blocks with default responses
- **User Input Errors**: Validation and clear error messages

## Performance Optimizations

- Database connection pooling
- Efficient SQL queries with indexes
- Lazy loading of LLM responses
- Caching of market conditions (can be enhanced)

## Future Architecture Enhancements

1. **Microservices**: Split agents into separate services
2. **Message Queue**: For async agent processing
3. **Real-time Updates**: WebSocket for live dashboard updates
4. **Machine Learning**: Predictive models for expense patterns
5. **API Gateway**: For external integrations (banks, market data)

