import streamlit as st
import agent as agent
from pdfGenerator import generate_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FreeMind AI / Medical Report",
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

# ---------------- AUTH GUARDS ----------------
if "user" not in st.session_state:
    st.switch_page("Home.py")

if not st.session_state.get("counselling_sessions"):
    st.warning("Start a counselling session to unlock the medical report.")
    st.stop()

# ---------------- TITLE ----------------
st.title("📄 Medical Report")

# ---------------- SESSION DATA ----------------
id = st.session_state.get("id")
counsellingID = st.session_state.get("counsellingID")

if id is None or counsellingID is None:
    st.error("No counselling session selected.")
    st.stop()

# ---------------- GENERATE REPORT ----------------
report = agent.medicalReportAgent(id, counsellingID)

# ---------------- PATIENT NAME ----------------
st.markdown("### Patient Name")
if report.patient:
    st.markdown(f"- **{report.patient}**")
else:
    st.info("No patient detected.")

# ---------------- PROBLEMS IDENTIFIED ----------------
st.markdown("### 🧩 Problems Identified")
if report.problems_identified:
    for problem in report.problems_identified:
        st.markdown(f"- **{problem}**")
else:
    st.info("No problems detected.")

# ---------------- REMEDIES ----------------
st.markdown("### 💊 Remedies")
if report.remedies:
    for remedy in report.remedies:
        st.markdown(f"- {remedy}")
else:
    st.info("No remedies available.")

# ---------------- PDF DOWNLOAD ----------------
st.download_button(
    label="📄 Download Report as PDF",
    data=generate_pdf(report),
    file_name="FreeMindAI_Medical_Report.pdf",
    mime="application/pdf"
)
