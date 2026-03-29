import mysql.connector
import streamlit as st

def get_connection():
    """Returns a connection to the MySQL database using streamlit secrets."""
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"])
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def execute_query(query, params=(), fetch=False):
    """Executes a parameterized query."""
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
        st.error(f"SQL Error: {e}")
        if conn:
            conn.close()
        return None

def get_categories():
    """Fetches all categories from the database."""
    return execute_query("SELECT * FROM categories", fetch=True)

def add_expense(date, category, amount, description, source="Manual"):
    """Inserts a new expense into the database."""
    query = """
        INSERT INTO expenses (date, category, amount, description, raw_text_source)
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(query, (date, category, amount, description, source))

def clear_all_expenses():
    """Deletes all expenses from the database."""
    return execute_query("TRUNCATE TABLE expenses")

