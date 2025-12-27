import streamlit as st
import sqlite3
import hashlib
import uuid

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Login | FreeMind AI",
    layout="centered"
)

# ---------------- HIDE SIDEBAR ----------------
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DB SETUP ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# ---------------- UTILS ----------------
def hash_value(v):
    return hashlib.sha256(str(v).encode()).hexdigest()

# ---------------- SESSION-BASED AUTO LOGIN ----------------
# If user already known in this session → go to PIN
if "pending_user" in st.session_state:
    st.switch_page("pages/Pin.py")

if "user" in st.session_state:
    st.session_state["pending_user"] = st.session_state["user"]
    del st.session_state["user"]
    st.switch_page("pages/Pin.py")

# ---------------- UI ----------------
st.title("Welcome to FreeMind AI")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# ---------------- LOGIN ----------------
with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute(
            "SELECT password FROM users WHERE email=?", (email,)
        )
        user = c.fetchone()

        if user and user[0] == hash_value(password):
            # move to PIN verification
            st.session_state["pending_user"] = email
            st.switch_page("pages/Pin.py")
        else:
            st.error("Invalid email or password")

# ---------------- SIGN UP ----------------
with tab2:
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    new_pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4)

    if st.button("Create Account"):
        try:
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?)",
                (
                    new_email,
                    hash_value(new_password),
                    hash_value(new_pin),
                    str(uuid.uuid4())
                )
            )
            conn.commit()

            # new user → PIN verification
            st.session_state["pending_user"] = new_email
            st.switch_page("pages/Pin.py")

        except sqlite3.IntegrityError:
            st.error("Email already exists")
