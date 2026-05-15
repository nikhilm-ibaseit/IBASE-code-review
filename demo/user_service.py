"""
User management service — demo file for AI review testing.
Contains a realistic mix of good patterns and deliberate issues
so the AI reviewer has something meaningful to analyse.
"""

import hashlib
import sqlite3


DB_PATH = "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ── Authentication ────────────────────────────────────────────────────────────

def login(username: str, password: str) -> dict | None:
    """Return user record if credentials match, else None."""
    conn = get_connection()
    cursor = conn.cursor()

    # BUG: raw string interpolation — SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "username": row[1], "role": row[3]}
    return None


def hash_password(password: str) -> str:
    # BUG: MD5 is cryptographically broken — should use bcrypt/argon2
    return hashlib.md5(password.encode()).hexdigest()


# ── User CRUD ─────────────────────────────────────────────────────────────────

def create_user(username: str, password: str, role: str = "viewer") -> int:
    """Insert a new user and return their ID."""
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    # BUG: no check for duplicate usernames before insert
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed, role),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_all_users() -> list[dict]:
    """Return every user in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # WARNING: no pagination — will load entire table into memory
    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]


def delete_user(user_id: int) -> bool:
    """Delete a user by ID. Returns True if a row was removed."""
    conn = get_connection()
    cursor = conn.cursor()

    # BUG: no authorisation check — any caller can delete any user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    return affected > 0


# ── Password reset ────────────────────────────────────────────────────────────

def reset_password(username: str, new_password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(new_password)

    # BUG: no verification of caller identity before resetting
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hashed, username),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    return affected > 0


# ── Reporting ─────────────────────────────────────────────────────────────────

def get_user_report(role: str) -> str:
    """Build a plain-text report of users with the given role."""
    users = get_all_users()

    # WARNING: filtering in Python instead of in SQL
    filtered = [u for u in users if u["role"] == role]

    lines = [f"Users with role '{role}':"]
    for u in filtered:
        lines.append(f"  [{u['id']}] {u['username']}")

    return "\n".join(lines)
