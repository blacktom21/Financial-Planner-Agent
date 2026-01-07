"""
Authentication system for financial advisor
Simple session-based auth with password hashing
"""
from functools import wraps
from flask import session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from memory.db import get_connection
from datetime import datetime


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def register_user(username: str, email: str, password: str, full_name: str = None) -> tuple[bool, str]:
    """
    Register a new user
    Returns: (success: bool, message: str)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Check if username or email already exists
        cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cur.fetchone():
            return False, "Username or email already exists"
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Insert user
        cur.execute(
            "INSERT INTO users (username, email, password_hash, full_name, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, email, password_hash, full_name, datetime.utcnow().isoformat())
        )
        user_id = cur.lastrowid
        
        # Create default profile
        cur.execute(
            """INSERT INTO user_profile (user_id, monthly_income, emergency_fund, total_emi, updated_at)
               VALUES (?, 0, 0, 0, ?)""",
            (user_id, datetime.utcnow().isoformat())
        )
        
        conn.commit()
        return True, "Registration successful"
    
    except Exception as e:
        conn.rollback()
        return False, f"Registration failed: {str(e)}"
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> tuple[bool, int, str]:
    """
    Authenticate a user
    Returns: (success: bool, user_id: int, message: str)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, password_hash, full_name FROM users WHERE username = ? OR email = ?", (username, username))
        user = cur.fetchone()
        
        if not user:
            return False, None, "Invalid username or password"
        
        user_id, password_hash, full_name = user
        
        if check_password_hash(password_hash, password):
            return True, user_id, full_name or username
        else:
            return False, None, "Invalid username or password"
    
    except Exception as e:
        return False, None, f"Authentication error: {str(e)}"
    finally:
        conn.close()


def get_user_profile(user_id: int) -> dict:
    """Get user profile from database"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT monthly_income, emergency_fund, total_emi, age, occupation, 
                   financial_goals, risk_tolerance, investment_experience
            FROM user_profile WHERE user_id = ?
        """, (user_id,))
        
        row = cur.fetchone()
        if row:
            return {
                "income": row["monthly_income"] or 0,
                "emergency_fund": row["emergency_fund"] or 0,
                "emi": row["total_emi"] or 0,
                "age": row["age"],
                "occupation": row["occupation"],
                "financial_goals": row["financial_goals"],
                "risk_tolerance": row["risk_tolerance"],
                "investment_experience": row["investment_experience"]
            }
        return {}
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return {}
    finally:
        conn.close()


def update_user_profile(user_id: int, **kwargs) -> bool:
    """Update user profile"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Map parameter names to database column names
        column_mapping = {
            "income": "monthly_income",
            "emi": "total_emi",
            "emergency_fund": "emergency_fund",
            "age": "age",
            "occupation": "occupation",
            "financial_goals": "financial_goals",
            "risk_tolerance": "risk_tolerance",
            "investment_experience": "investment_experience"
        }
        
        # Build update query dynamically
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in column_mapping:
                db_column = column_mapping[key]
                fields.append(f"{db_column} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(datetime.utcnow().isoformat())  # updated_at
        values.append(user_id)
        
        query = f"""
            UPDATE user_profile 
            SET {', '.join(fields)}, updated_at = ?
            WHERE user_id = ?
        """
        
        cur.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error updating profile: {e}")
        return False
    finally:
        conn.close()

