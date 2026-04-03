import bcrypt
from utils.db_manager import execute_query


def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_login(username: str, password: str) -> bool:
    """
    Fetches the stored bcrypt hash and checks the password against it.
    Returns True if the password matches, False otherwise.
    """
    try:
        query  = "SELECT password_hash FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        if not result:
            return False
        stored_hash = result[0]['password_hash'].encode()
        return bcrypt.checkpw(password.encode(), stored_hash)
    except Exception as e:
        # If database connection fails, return False (treat as invalid login)
        print(f"Login check failed: {e}")
        return False


def register_user(username: str, password: str, full_name: str) -> bool:
    """
    Creates a new user account.
    Returns True on success, False if the username is already taken.
    """
    try:
        existing = execute_query(
            "SELECT username FROM users WHERE username = %s",
            (username,), fetch=True
        )
        if existing:
            return False
        hashed = hash_password(password)
        execute_query(
            "INSERT INTO users (username, password_hash, full_name) VALUES (%s, %s, %s)",
            (username, hashed, full_name)
        )
        return True
    except Exception as e:
        # If database connection fails, return False
        print(f"User registration failed: {e}")
        return False


def get_user_details(username: str) -> str:
    """Retrieves the full name of the user."""
    try:
        query  = "SELECT full_name FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        return result[0]['full_name'] if result else "User"
    except Exception as e:
        # If database connection fails, return default
        print(f"Failed to get user details: {e}")
        return "User"