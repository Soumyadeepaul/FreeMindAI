import sqlite3

def init_databases():
    # ---------- Feedback DB ----------
    feedback_conn = sqlite3.connect("feedback.db", check_same_thread=False)
    feedback_cur = feedback_conn.cursor()

    feedback_cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        email TEXT,
        feedback TEXT
    )
    """)

    feedback_conn.commit()
    feedback_conn.close()

    # ---------- Users DB ----------
    users_conn = sqlite3.connect("users.db", check_same_thread=False)
    users_cur = users_conn.cursor()

    users_cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        pin TEXT,
        token TEXT
    )
    """)

    users_conn.commit()
    users_conn.close()
