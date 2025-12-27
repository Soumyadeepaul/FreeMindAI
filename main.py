import streamlit as st
import sqlite3
from databaseCreator import init_databases

# ---------- INIT ----------
init_databases()

st.set_page_config(
    page_title="FreeMind AI",
    page_icon="logo.png",
    layout="wide"
)

# ---------- HIDE SIDEBAR PAGES ----------
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------- DB CONNECTION ----------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# ---------- UI STYLE ----------
st.markdown("""
<style>
.centered-box {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    max-width: 500px;
}
</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
with st.container():
    st.markdown("<div class='centered-box'>", unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align:center;'>A place where nobody judges you.</h3>",
        unsafe_allow_html=True
    )

    if st.button("Start your counselling with FreeMind  →", use_container_width=True):

        # ---------- SESSION-BASED AUTH ----------
        if "user" in st.session_state:
            # already logged in → go to app
            st.switch_page("pages/Pin.py")

        elif "pending_user" in st.session_state:
            # email verified, PIN pending
            st.switch_page("pages/Pin.py")

        else:
            # fresh user
            st.switch_page("pages/Auth.py")

    st.markdown("</div>", unsafe_allow_html=True)
