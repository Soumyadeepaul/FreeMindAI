import streamlit as st
import sqlite3
import hashlib
import os

st.set_page_config(page_title="PIN Verification", layout="centered")

# Hide pages from sidebar
st.set_page_config()
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:has(a[href*="Auth"]) {
    display: none;
}
[data-testid="stSidebarNav"] ul li:has(a[href*="Pin"]) {
    display: none;
}
[data-testid="stSidebarNav"] ul li:has(a[href*="App"]) {
    display: none;
}
[data-testid="stSidebarNav"] ul li:has(a[href*="Medical_Report"]) {
    display: none;
}
[data-testid="stSidebarNav"] ul li:has(a[href*="About_Us"]) {
    display: none;
}
</style>
""", unsafe_allow_html=True)

def hash_value(v):
    return hashlib.sha256(str(v).encode()).hexdigest()

# Guard
if "pending_user" not in st.session_state:
    st.switch_page("c:\MTech\LLM Project\Main.py")

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

st.title("🔐 PIN Verification")
st.caption("We ask for this PIN so our conversations stay personal, private, and protected.")

pin = st.text_input("Enter your 4-digit PIN", type="password", max_chars=4)

if st.button("Verify PIN"):
    c.execute(
        "SELECT pin FROM users WHERE email=?",
        (st.session_state["pending_user"],)
    )
    db_pin = c.fetchone()
    print(st.session_state["pending_user"],db_pin)
    if db_pin or db_pin[0] == hash_value(pin):
        st.session_state["user"] = st.session_state["pending_user"]
        # del st.session_state["pending_user"]
        st.switch_page("pages/App.py")
    else:
        st.error("Invalid PIN")
