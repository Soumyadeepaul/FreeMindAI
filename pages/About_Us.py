import streamlit as st

# ---------------- FEEDBACK SECTION ----------------
import sqlite3

# Initialize DB
conn = sqlite3.connect("feedback.db", check_same_thread=False)
c = conn.cursor()



st.set_page_config(
    page_title="FreeMind AI/About Us",
    page_icon="logo.png",
    layout="wide"
)
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
</style>
""", unsafe_allow_html=True)


st.title("About Us")

st.markdown("""
### 🧠 FreeMind AI – Your Personal Mental Wellness Companion

FreeMind AI is designed to support users with:
- Friendly, conversational counselling  
- Medical-style mental health insights  
- Personalized suggestions  
- Privacy-first AI interactions  

---

### 👥 Our Mission

To make mental wellness simple, accessible, and supportive using AI-driven tools — especially helping introverts express themselves comfortably.

---

### 💡 What We Offer

- 🤝 Emotional counselling  
- 🏥 Medical-style mental health reports  
- 📈 Progress tracking  
- 🔒 Secure & private interactions  

---

### 🚀 Powered by AI  
Built using state-of-the-art LLMs and custom cognitive models.
            
---
### 💙 Created from the Heart
Created by Soumyadeep Paul, who dreamed of giving comfort to those who feel unheard and helping quiet souls find a safe space to open their hearts.
""")


# ---------------- FEEDBACK SECTION ----------------

st.markdown("---")
st.subheader("📩 Share Your Feedback")

# Initialize DB
conn = sqlite3.connect("feedback.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    email TEXT,
    feedback TEXT
)
""")
conn.commit()

# Get email from session
user_email = st.session_state.get("user")

# Feedback form
with st.form("feedback_form"):
    feedback = st.text_area(
        "Your Feedback",
        placeholder="Tell us what you feel, what we can improve, or how FreeMind AI helped you..."
    )
    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    if not feedback.strip():
        st.warning("Please write some feedback before submitting.")
    else:
        c.execute(
            "INSERT INTO feedback (email, feedback) VALUES (?, ?)",
            (user_email, feedback.strip())
        )
        conn.commit()
        st.success("Thank you for your feedback 💙 It truly helps us improve.")