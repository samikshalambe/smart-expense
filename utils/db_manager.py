import mysql.connector
from mysql.connector import pooling
import streamlit as st


# ── Connection Pool ─────────────────────────────────────────────
# Created once per app session and reused — eliminates the 300-800ms
# TCP handshake cost on every single query.

@st.cache_resource
def _get_pool():
    """
    Creates a persistent MySQL connection pool.
    cache_resource keeps this alive for the whole Streamlit session —
    it is NOT recreated on every rerun.
    """
    try:
        if not hasattr(st, 'secrets') or "mysql" not in st.secrets:
            print("Database secrets not configured")
            return None

        pool = pooling.MySQLConnectionPool(
            pool_name="smartexpense_pool",
            pool_size=3,                        # 3 connections shared across reruns
            pool_reset_session=True,
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"]),
            connect_timeout=10,
        )
        return pool
    except Exception as e:
        print(f"Connection pool creation failed: {e}")
        return None


def get_connection():
    """Gets a connection from the pool (fast — no TCP handshake)."""
    pool = _get_pool()
    if not pool:
        return None
    try:
        return pool.get_connection()
    except Exception as e:
        print(f"Could not get connection from pool: {e}")
        return None


def execute_query(query, params=(), fetch=False):
    """Executes a parameterized query using a pooled connection."""
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
        conn.close()   # returns connection to pool, doesn't close TCP
        return result
    except Exception as e:
        print(f"SQL Error: {e}")
        try:
            conn.close()
        except Exception:
            pass
        return None


# ── Cached read functions ───────────────────────────────────────
# ttl=60 means data is re-fetched from DB at most once per minute.
# Cuts DB round trips from ~5 per rerun to ~1 per minute per function.

@st.cache_data(ttl=60)
def get_categories():
    """Fetches all categories. Cached for 60 seconds."""
    return execute_query("SELECT * FROM categories", fetch=True) or []


@st.cache_data(ttl=30)
def get_recent_transactions(limit=6):
    """Fetches recent transactions. Cached for 30 seconds."""
    return execute_query(
        "SELECT date, category, amount, description FROM expenses ORDER BY date DESC LIMIT %s",
        (limit,), fetch=True
    ) or []


@st.cache_data(ttl=30)
def get_all_expenses_for_charts():
    """Fetches all expenses for chart aggregation. Cached for 30 seconds."""
    return execute_query("SELECT category, amount FROM expenses", fetch=True) or []


@st.cache_data(ttl=30)
def get_expense_stats():
    """Fetches transaction stats in a single query. Cached for 30 seconds."""
    result = execute_query("""
        SELECT
            COUNT(*)                        AS count,
            COALESCE(SUM(amount), 0)        AS total,
            COALESCE(AVG(amount), 0)        AS avg_amount,
            COUNT(DISTINCT category)        AS category_count
        FROM expenses
    """, fetch=True)
    if result:
        return result[0]
    return {"count": 0, "total": 0, "avg_amount": 0, "category_count": 0}


def add_expense(date, category, amount, description, source="Manual"):
    """Inserts a new expense and clears relevant caches."""
    query = """
        INSERT INTO expenses (date, category, amount, description, raw_text_source)
        VALUES (%s, %s, %s, %s, %s)
    """
    result = execute_query(query, (date, category, amount, description, source))
    if result:
        # Clear caches so next load gets fresh data
        get_recent_transactions.clear()
        get_all_expenses_for_charts.clear()
        get_expense_stats.clear()
    return result


def clear_all_expenses():
    """Deletes all expenses and clears caches."""
    result = execute_query("TRUNCATE TABLE expenses")
    if result is not None:
        get_recent_transactions.clear()
        get_all_expenses_for_charts.clear()
        get_expense_stats.clear()
    return result