import bcrypt
from utils.db_manager import execute_query

def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt. Use this when creating/updating users."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_login(username: str, password: str) -> bool:
    """
    Fetches the stored bcrypt hash for the user and checks the password against it.
    Returns True if the password matches, False otherwise.
    """
    query = "SELECT password_hash FROM users WHERE username = %s"
    result = execute_query(query, (username,), fetch=True)

    if not result:
        return False

    stored_hash = result[0]['password_hash'].encode()
    return bcrypt.checkpw(password.encode(), stored_hash)

def get_user_details(username: str) -> str:
    """Retrieves the full name of the user."""
    query = "SELECT full_name FROM users WHERE username = %s"
    result = execute_query(query, (username,), fetch=True)
    return result[0]['full_name'] if result else "User"