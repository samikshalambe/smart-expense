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
    if not username or not password:
        return False

    try:
        query  = "SELECT password_hash FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        if not result or not result[0]:
            return False
        stored_hash = result[0].get('password_hash')
        if not stored_hash:
            return False
        stored_hash = stored_hash.encode()
        return bcrypt.checkpw(password.encode(), stored_hash)
    except Exception as e:
        # If database connection fails or any other error, return False
        print(f"Login check failed: {e}")
        return False


def register_user(username: str, password: str, full_name: str) -> bool:
    """
    Creates a new user account.
    Returns True on success, False if the username is already taken.
    """
    if not username or not password or not full_name:
        return False

    try:
        existing = execute_query(
            "SELECT username FROM users WHERE username = %s",
            (username,), fetch=True
        )
        if existing:
            return False
        hashed = hash_password(password)
        result = execute_query(
            "INSERT INTO users (username, password_hash, full_name) VALUES (%s, %s, %s)",
            (username, hashed, full_name)
        )
        return result is not None
    except Exception as e:
        # If database connection fails, return False
        print(f"User registration failed: {e}")
        return False


def get_user_details(username: str) -> str:
    """Retrieves the full name of the user."""
    if not username:
        return "User"

    try:
        query  = "SELECT full_name FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        if result and result[0] and result[0].get('full_name'):
            return result[0]['full_name']
        return "User"
    except Exception as e:
        # If database connection fails, return default
        print(f"Failed to get user details: {e}")
        return "User"