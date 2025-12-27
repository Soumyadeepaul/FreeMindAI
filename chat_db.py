import sqlite3
from typing import Optional

# -------------------------------
# DATABASE INITIALIZATION
# -------------------------------

DB_NAME = "chat_database.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    client_id TEXT NOT NULL,
    counselling_id TEXT NOT NULL,
    conversation TEXT,
    PRIMARY KEY (client_id, counselling_id)
)
""")

conn.commit()

# -------------------------------
# CHAT HISTORY FUNCTIONS
# -------------------------------

def append_message(client_id: str, counselling_id: str, role: str, message: str) -> None:
    """
    Append a message to a client's counselling session.
    """
    new_line = f"{role.upper()}: {message}\n"

    c.execute("""
        SELECT conversation FROM chat_history
        WHERE client_id = ? AND counselling_id = ?
    """, (client_id, counselling_id))

    row = c.fetchone()

    if row:
        updated_conversation = row[0] + new_line
        c.execute("""
            UPDATE chat_history
            SET conversation = ?
            WHERE client_id = ? AND counselling_id = ?
        """, (updated_conversation, client_id, counselling_id))
    else:
        c.execute("""
            INSERT INTO chat_history (client_id, counselling_id, conversation)
            VALUES (?, ?, ?)
        """, (client_id, counselling_id, new_line))

    conn.commit()


def get_conversation(client_id: str, counselling_id: str) -> str:
    """
    Get full conversation text for a specific counselling session.
    """
    c.execute("""
        SELECT conversation FROM chat_history
        WHERE client_id = ? AND counselling_id = ?
    """, (client_id, counselling_id))

    row = c.fetchone()
    return row[0] if row else ""


def clear_conversation(client_id: str, counselling_id: str) -> None:
    """
    Delete a single counselling session.
    """
    c.execute("""
        DELETE FROM chat_history
        WHERE client_id = ? AND counselling_id = ?
    """, (client_id, counselling_id))

    conn.commit()


def clear_all_client_conversations(client_id: str) -> None:
    """
    Delete all counselling sessions of a client.
    """
    c.execute("""
        DELETE FROM chat_history
        WHERE client_id = ?
    """, (client_id,))

    conn.commit()


def list_counselling_sessions(client_id: str):
    """
    List all counselling IDs for a client.
    """
    c.execute("""
        SELECT counselling_id FROM chat_history
        WHERE client_id = ?
    """, (client_id,))

    return [row[0] for row in c.fetchall()]

def get_all_counselling_ids(client_id: str):
    c.execute("""
        SELECT counselling_id
        FROM chat_history
        WHERE client_id = ?
        ORDER BY counselling_id
    """, (client_id,))

    details=[row[0] for row in c.fetchall()]
    # print(details)
    return details



# -------------------------------
# EXAMPLE USAGE
# -------------------------------
# if __name__ == "__main__":
#     client_id = "2"
#     counselling_id = "session_1"

#     append_message(client_id, counselling_id, "user", "I feel anxious today")
#     append_message(client_id, counselling_id, "assistant", "I am here with you. You are safe.")

#     print("Conversation:")
#     print(get_conversation(client_id, counselling_id))

#     print("All sessions:", list_counselling_sessions(client_id))

    # clear_conversation(client_id, counselling_id)
    # clear_all_client_conversations(client_id)
