from datetime import datetime
from memory.db import get_connection


class ExpenseTrackerAgent:
    """
    This agent records and aggregates expenses.
    It does NOT make decisions or recommendations.
    """

    def add_expense(self, user_id, category, amount, month, description=None, 
                   subcategory=None, date=None, payment_method=None, 
                   is_recurring=False, tags=None):
        """
        Add expense with detailed information
        Helps agents get more context about spending patterns
        """
        conn = get_connection()
        cur = conn.cursor()
        
        # Use current date if not provided
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Convert tags list to string
        tags_str = ",".join(tags) if isinstance(tags, list) else tags

        cur.execute(
            """
            INSERT INTO expenses (user_id, category, subcategory, amount, date, month, 
                                 description, payment_method, is_recurring, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, category, subcategory, amount, date, month, description, 
             payment_method, 1 if is_recurring else 0, tags_str, datetime.utcnow().isoformat())
        )

        conn.commit()
        conn.close()
    
    def get_detailed_expenses(self, user_id, month):
        """Get detailed expense breakdown with all fields"""
        conn = get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                SELECT category, subcategory, SUM(amount) as total, 
                       payment_method, COUNT(*) as transaction_count
                FROM expenses
                WHERE user_id = ? AND month = ?
                GROUP BY category, subcategory, payment_method
                ORDER BY total DESC
            """, (user_id, month))
            
            rows = cur.fetchall()
            conn.close()
            
            return [
                {
                    "category": row["category"],
                    "subcategory": row["subcategory"],
                    "amount": row["total"],
                    "payment_method": row["payment_method"],
                    "transactions": row["transaction_count"]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error getting detailed expenses: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def monthly_summary(self, user_id, month):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE user_id = ? AND month = ?
                GROUP BY category
                """,
                (user_id, month)
            )

            rows = cur.fetchall()
            conn.close()

            summary = {row["category"]: row["total"] for row in rows}
            total_expenses = sum(summary.values())

            return {
                "by_category": summary,
                "total": total_expenses
            }
        except Exception as e:
            # Return default empty summary on any error
            return {
                "by_category": {},
                "total": 0
            }
