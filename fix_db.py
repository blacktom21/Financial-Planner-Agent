"""
Fix database schema - add missing columns and update structure
"""
from memory.db import get_connection

def fix_database():
    """Add missing columns to existing tables"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Check and add columns to user_profile if they don't exist
        cur.execute("PRAGMA table_info(user_profile)")
        columns = [row[1] for row in cur.fetchall()]
        
        # Add missing columns
        if "total_emi" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN total_emi REAL DEFAULT 0")
            print("Added total_emi column")
        
        if "age" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN age INTEGER")
            print("Added age column")
        
        if "occupation" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN occupation TEXT")
            print("Added occupation column")
        
        if "financial_goals" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN financial_goals TEXT")
            print("Added financial_goals column")
        
        if "risk_tolerance" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN risk_tolerance TEXT")
            print("Added risk_tolerance column")
        
        if "investment_experience" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN investment_experience TEXT")
            print("Added investment_experience column")
        
        if "updated_at" not in columns:
            cur.execute("ALTER TABLE user_profile ADD COLUMN updated_at TEXT")
            # Update existing rows with current timestamp
            cur.execute("UPDATE user_profile SET updated_at = datetime('now') WHERE updated_at IS NULL")
            print("Added updated_at column")
        
        # Check expenses table
        cur.execute("PRAGMA table_info(expenses)")
        exp_columns = [row[1] for row in cur.fetchall()]
        
        if "description" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN description TEXT")
            print("Added description column to expenses")
        
        if "created_at" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN created_at TEXT")
            cur.execute("UPDATE expenses SET created_at = datetime('now') WHERE created_at IS NULL")
            print("Added created_at column to expenses")
        
        if "subcategory" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN subcategory TEXT")
            print("Added subcategory column to expenses")
        
        if "date" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN date TEXT")
            print("Added date column to expenses")
        
        if "payment_method" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN payment_method TEXT")
            print("Added payment_method column to expenses")
        
        if "is_recurring" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN is_recurring INTEGER DEFAULT 0")
            print("Added is_recurring column to expenses")
        
        if "tags" not in exp_columns:
            cur.execute("ALTER TABLE expenses ADD COLUMN tags TEXT")
            print("Added tags column to expenses")
        
        conn.commit()
        print("Database schema updated successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error fixing database: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()

