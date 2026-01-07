# Setup Guide - Financial Advisor AI

## Complete Setup Instructions

### Step 1: Prerequisites

Ensure you have:
- **Python 3.11 or higher** installed
- **pip** (Python package manager)
- **Git** (for cloning the repository)

Check Python version:
```bash
python --version
# Should show Python 3.11.x or higher
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/financial_agentic_ai.git
cd financial_agentic_ai
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.1.2
- Werkzeug 3.1.4
- requests 2.31.0

### Step 5: Initialize Database

```bash
python init_db.py
```

This creates:
- `memory/finance.db` - SQLite database
- All required tables (users, expenses, investments, etc.)

**If you have an existing database**, run:
```bash
python fix_db.py
```

This adds any missing columns to existing tables.

### Step 6: Configure LLM (Optional)

#### Option A: Hugging Face (Recommended for beginners)

1. Create account at [Hugging Face](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create a new token
4. Set environment variable:

**Windows PowerShell:**
```powershell
$env:HUGGINGFACE_API_KEY="your-token-here"
```

**Windows CMD:**
```cmd
set HUGGINGFACE_API_KEY=your-token-here
```

**Linux/Mac:**
```bash
export HUGGINGFACE_API_KEY="your-token-here"
```

#### Option B: Ollama (Local, Completely Free)

1. Download and install [Ollama](https://ollama.ai/)
2. Start Ollama service:
   ```bash
   ollama serve
   ```
3. Download a model:
   ```bash
   ollama pull mistral
   ```
4. Set environment variables:

**Windows:**
```powershell
$env:OLLAMA_URL="http://localhost:11434"
$env:LLM_PROVIDER="ollama"
```

**Linux/Mac:**
```bash
export OLLAMA_URL="http://localhost:11434"
export LLM_PROVIDER="ollama"
```

#### Option C: No LLM (Rule-Based)

If you don't configure an LLM, the system will use intelligent rule-based recommendations. This works perfectly fine but with less personalized advice.

### Step 7: Set Secret Key (Production)

For production, change the secret key:

**Windows:**
```powershell
$env:SECRET_KEY="your-random-secret-key-here"
```

**Linux/Mac:**
```bash
export SECRET_KEY="your-random-secret-key-here"
```

Or create a `.env` file:
```
SECRET_KEY=your-random-secret-key-here
HUGGINGFACE_API_KEY=your-key-here
LLM_PROVIDER=huggingface
```

### Step 8: Run the Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 9: Access the Application

1. Open browser: `http://127.0.0.1:5000`
2. You'll be redirected to login page
3. Click "Create a new account"
4. Register with:
   - Username
   - Email
   - Password (min 6 characters)
   - Full name

### Step 10: Complete Your Profile

After registration and login:

1. You'll be prompted to complete your profile
2. Enter:
   - **Monthly Income**: Your take-home salary
   - **Total EMI**: All loan EMIs combined
   - **Emergency Fund**: Current savings
   - **Age**: Your age
   - **Occupation**: Your profession
   - **Risk Tolerance**: Conservative/Moderate/High/Aggressive
   - **Investment Experience**: Beginner/Intermediate/Advanced
   - **Financial Goals**: e.g., "Buy house in 5 years, Retire at 50"

3. Click "Save Profile & Continue"

### Step 11: Start Using the System

#### Add Expenses
1. Click "Add Expense" on dashboard
2. Fill in:
   - Category (Food, Transportation, etc.)
   - Subcategory (optional)
   - Amount
   - Date
   - Payment method
   - Description
   - Mark if recurring
   - Tags (optional)

#### View Dashboard
- **Auto-Generated Monthly Plan**: Created automatically
- **Risk Analysis**: Your financial risk score
- **Budget Recommendations**: Expense reduction suggestions
- **Investment Recommendations**: SIP plans based on market
- **Future Planning**: Goal timelines

#### Get SIP Investment Plan
1. Click "Get SIP Recommendations" on dashboard
2. View market-aware investment suggestions
3. See fund recommendations
4. Read beginner tips

#### Ask AI Advisor
1. Type your question in the prompt box
2. Click "Ask" or press Enter
3. Get personalized AI advice

## Troubleshooting

### Database Errors

**Error**: `table user_profile has no column named total_emi`

**Solution**:
```bash
python fix_db.py
```

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### LLM Not Working

**Error**: No AI advice, only rule-based

**Solutions**:
1. Check API key is set correctly
2. For Ollama, ensure service is running: `ollama serve`
3. Check internet connection (for Hugging Face)
4. System will use rule-based fallback (still works!)

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Change port in app.py
app.run(debug=True, host="0.0.0.0", port=5001)
```

### Session Errors

**Error**: `Bad Request / Invalid session`

**Solution**:
- Clear browser cookies
- Restart Flask app
- Check SECRET_KEY is set

## Development Setup

### Enable Debug Mode

Already enabled by default in `app.py`:
```python
app.run(debug=True)
```

### Database Location

Database file: `memory/finance.db`

To reset database:
```bash
rm memory/finance.db
python init_db.py
```

### Logs

Flask debug mode shows logs in terminal. For production, configure proper logging.

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` to random value
- [ ] Set `debug=False` in production
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper SSL/HTTPS
- [ ] Configure environment variables securely
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Set up monitoring

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using PostgreSQL

1. Install PostgreSQL
2. Create database
3. Update `memory/db.py` to use PostgreSQL connection
4. Update connection string

## Next Steps

1. **Add Expenses**: Track your spending
2. **Review Dashboard**: See your financial health
3. **Get SIP Plan**: Start investing
4. **Ask Questions**: Use AI advisor
5. **Set Goals**: Plan for the future

## Support

If you encounter issues:
1. Check this setup guide
2. Review [ARCHITECTURE.md](ARCHITECTURE.md)
3. Check GitHub issues
4. Open a new issue with details

---

**Happy Financial Planning! 💰**

