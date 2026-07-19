import os
import sqlite3
import hashlib

# Resolve the absolute path to your database file
db_path = os.path.join("instance", "app.db")
print(f"Connecting directly to database binary file at: {db_path}")

# Generate a secure fallback hash password matching standard auth workflows
raw_password = "Admin123!"
salt = os.urandom(16)
password_hash_val = "pbkdf2:sha256:600000$" + hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt, 600000).hex()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if an admin account already exists to prevent duplicate key entries
cursor.execute("SELECT id FROM user WHERE username = 'admin';")
existing_user = cursor.fetchone()

if not existing_user:
    # 🧠 Injecting using only the exact three active columns: username, password
    query = "INSERT INTO user (username, password) VALUES ('admin', ?);"
    cursor.execute(query, (password_hash_val,))
    conn.commit()
    print("\n👑 MASTER ACCOUNT CREATION SUCCESSFUL!")
    print("   👉 Username: admin")
    print("   👉 Password: Admin123!")
else:
    print("\nℹ️ Account 'admin' already exists. Updating master password configuration...")
    cursor.execute("UPDATE user SET password = ? WHERE username = 'admin';", (password_hash_val,))
    conn.commit()
    print("👑 Master password updated successfully!")

conn.close()
