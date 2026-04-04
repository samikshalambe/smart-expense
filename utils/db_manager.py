import mysql.connector
import streamlit as st


def get_connection():
    """
    Opens a fresh MySQL connection each time.
    Connection pools don't work reliably on Railway free tier because Railway
    closes idle connections, causing pool connections to go stale and fail silently.
    The @st.cache_data decorators on read functions handle the speed improvement instead.
    """
    try:
        if not hasattr(st, 'secrets') or "mysql" not in st.secrets:
            print("Database secrets not configured")
            return None

        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"]),
            connect_timeout=10,
            connection_timeout=10,
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


def execute_query(query, params=(), fetch=False):
    """Executes a parameterized query with a fresh connection."""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"SQL Error: {e}")
        try:
            conn.close()
        except Exception:
            pass
        return None


# ── Cached read helpers ─────────────────────────────────────────
# These cache DB results in memory so the same data isn't re-fetched
# on every Streamlit rerun. The connection is only opened when the
# cache expires (ttl seconds) — not on every button click or slider move.

@st.cache_data(ttl=60)
def get_categories():
    """All expense categories. Cached 60 s."""
    return execute_query("SELECT * FROM categories", fetch=True) or []


@st.cache_data(ttl=30)
def get_recent_transactions(limit=6):
    """Most recent N transactions. Cached 30 s."""
    return execute_query(
        "SELECT date, category, amount, description "
        "FROM expenses ORDER BY date DESC LIMIT %s",
        (limit,), fetch=True
    ) or []


@st.cache_data(ttl=30)
def get_all_expenses_for_charts():
    """All expenses for chart aggregation. Cached 30 s."""
    return execute_query(
        "SELECT category, amount FROM expenses", fetch=True
    ) or []


@st.cache_data(ttl=30)
def get_expense_stats():
    """Aggregate stats in one query. Cached 30 s."""
    result = execute_query("""
        SELECT
            COUNT(*)                 AS count,
            COALESCE(SUM(amount), 0) AS total,
            COALESCE(AVG(amount), 0) AS avg_amount,
            COUNT(DISTINCT category) AS category_count
        FROM expenses
    """, fetch=True)
    if result:
        return result[0]
    return {"count": 0, "total": 0.0, "avg_amount": 0.0, "category_count": 0}


def add_expense(date, category, amount, description, source="Manual"):
    """Inserts an expense and clears relevant read caches."""
    result = execute_query(
        "INSERT INTO expenses (date, category, amount, description, raw_text_source) "
        "VALUES (%s, %s, %s, %s, %s)",
        (date, category, amount, description, source)
    )
    if result:
        get_recent_transactions.clear()
        get_all_expenses_for_charts.clear()
        get_expense_stats.clear()
    return result


def clear_all_expenses():
    """Truncates expenses table and clears read caches."""
    result = execute_query("TRUNCATE TABLE expenses")
    if result is not None:
        get_recent_transactions.clear()
        get_all_expenses_for_charts.clear()
        get_expense_stats.clear()
    return result