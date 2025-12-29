import streamlit as st
import agent as agent
from chat_db import get_all_counselling_ids

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FreeMind AI",
    page_icon="logo.png",
    layout="wide"
)

# Hide pages from sidebar
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

# ---------------- AUTH GUARD ----------------
if "user" not in st.session_state:
    st.switch_page("main.py")

# ---------------- SESSION STATES ----------------
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if "init_done" not in st.session_state:
    bot_reply = agent.agentPrerequisites()
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    st.session_state.init_done = True

if "counselling_sessions" not in st.session_state:
    st.session_state.counselling_sessions = []

if "current_counselling_started" not in st.session_state:
    st.session_state.current_counselling_started = False

if "active_counselling" not in st.session_state:
    st.session_state.active_counselling = None

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo.png", width=100)

with col2:
    st.markdown(
        "<h2 style='margin-top:10px;'>FreeMind AI Agent</h2>",
        unsafe_allow_html=True
    )

# ---------------- SIDEBAR ----------------
st.session_state["id"] = st.session_state.get("user")
st.session_state["counsellingID"] = st.session_state.get("active_counselling")

if st.session_state.sidebar_open:

    st.sidebar.markdown("### 👤 Profile")
    st.sidebar.write(st.session_state.get("user", "Unknown User"))

    st.sidebar.divider()

    st.sidebar.markdown("### 🧠 Counselling Sessions")
    client_id = st.session_state["id"]

    if not st.session_state.counselling_sessions:
        st.session_state.counselling_sessions = get_all_counselling_ids(client_id)

    if st.session_state.counselling_sessions:
        for i in range(len(st.session_state.counselling_sessions)):
            if st.sidebar.button(
                f"Counselling {i + 1}",
                key=f"counselling_{i}",
                use_container_width=True
            ):
                st.session_state.active_counselling = i + 1
                st.session_state.messages = []
                st.session_state.current_counselling_started = True
    else:
        st.sidebar.caption("No counselling yet")

    if st.sidebar.button("➕ New Counselling", use_container_width=True):
        st.session_state.counselling_sessions.append("started")
        st.session_state.active_counselling = len(st.session_state.counselling_sessions)
        st.session_state.messages = []
        st.session_state.current_counselling_started = True

    st.sidebar.divider()

    # 🔧 FIX: session-only logout (no file access)
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("Home.py")

# ---------------- CHAT UI ----------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your message…")

if user_input:

    if not st.session_state.current_counselling_started:
        st.session_state.counselling_sessions.append("started")
        st.session_state.active_counselling = len(st.session_state.counselling_sessions)
        st.session_state.current_counselling_started = True

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    bot_reply = agent.agent(
        user_input,
        st.session_state.get("user", "Unknown User"),
        st.session_state.active_counselling
    )

    # 🔧 FIX: handle music tool result
    if isinstance(bot_reply, dict) and bot_reply.get("status") == "success":
        song = bot_reply.get("song", "")
        url = bot_reply.get("url", "")

        msg = f"🎵 Recommended Song: {song}"
        st.session_state.messages.append(
            {"role": "assistant", "content": msg}
        )

        st.chat_message("assistant").markdown(
            f"""
            🎵 **Recommended Song:** {song}  
            <a href="{url}" target="_blank">▶ Open on Spotify</a>
            """,
            unsafe_allow_html=True
        )
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )
        st.chat_message("assistant").write(bot_reply)

