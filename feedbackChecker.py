import sqlite3

conn = sqlite3.connect("feedback.db")
c = conn.cursor()

c.execute("SELECT email, feedback FROM feedback")
rows = c.fetchall()

if not rows:
    print("No feedback found.")
else:
    for i, (email, feedback) in enumerate(rows, start=1):
        print(f"\n{i}. Email: {email}")
        print(f"   Feedback: {feedback}")

conn.close()
