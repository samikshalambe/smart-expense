import mysql.connector
from mysql.connector import errorcode
import bcrypt
import streamlit as st

def get_db_connection(create_db=False):
    # Read credentials from st.secrets instead of hardcoding them
    config = {
        'user': st.secrets["mysql"]["user"],
        'password': st.secrets["mysql"]["password"],
        'host': st.secrets["mysql"]["host"],
        'port': int(st.secrets["mysql"]["port"]),
    }

    if not create_db:
        config['database'] = st.secrets["mysql"]["database"]

    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        return err

def initialize_db():
    # 1. Connect to MySQL to create the database
    conn = get_db_connection(create_db=True)
    if isinstance(conn, mysql.connector.Error):
        print(f"Error connecting to MySQL: {conn}")
        return

    cursor = conn.cursor()

    try:
        db_name = st.secrets["mysql"]["database"]
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        print(f"Database '{db_name}' verified/created.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    finally:
        cursor.close()
        conn.close()

    # 2. Reconnect to the new database to create tables
    conn = get_db_connection(create_db=False)
    cursor = conn.cursor()

    TABLES = {}
    TABLES['categories'] = (
        "CREATE TABLE IF NOT EXISTS `categories` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(255) NOT NULL UNIQUE,"
        "  `budget_limit` decimal(10,2) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
    )

    TABLES['expenses'] = (
        "CREATE TABLE IF NOT EXISTS `expenses` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `date` date NOT NULL,"
        "  `category` varchar(255) NOT NULL,"
        "  `amount` decimal(10,2) NOT NULL,"
        "  `description` text,"
        "  `raw_text_source` text,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
    )

    TABLES['users'] = (
        "CREATE TABLE IF NOT EXISTS `users` ("
        "  `username` VARCHAR(255) PRIMARY KEY,"
        "  `password_hash` VARCHAR(255) NOT NULL,"
        "  `full_name` VARCHAR(255)"
        ") ENGINE=InnoDB"
    )

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    # 3. Seed some default categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        print("Seeding default categories...")
        default_categories = [
            ('Food', 500.00),
            ('Rent', 1500.00),
            ('Utilities', 300.00),
            ('Entertainment', 200.00),
            ('Transport', 150.00),
            ('Other', 100.00)
        ]
        cursor.executemany(
            "INSERT INTO categories (name, budget_limit) VALUES (%s, %s)",
            default_categories
        )
        conn.commit()

    # 4. Seed admin user if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        print("Seeding admin user...")
        admin_pass = "admin123"
        admin_hash = bcrypt.hashpw(admin_pass.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO users (username, password_hash, full_name) VALUES (%s, %s, %s)",
            ("admin", admin_hash, "Administrator")
        )
        conn.commit()

    cursor.close()
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_db()