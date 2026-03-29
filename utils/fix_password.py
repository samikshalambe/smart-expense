import bcrypt
import mysql.connector

new_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="household_db"
)
cursor = conn.cursor()
cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'admin'", (new_hash,))
conn.commit()
conn.close()
print("Done! Password hash updated.")