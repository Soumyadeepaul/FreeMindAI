import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from ics import Calendar, Event
from dotenv import load_dotenv
import os
from langchain.tools import tool
import streamlit as st

load_dotenv()


def get_email_credentials():
    FROM_EMAIL = st.secrets["EMAIL_ID"]
    APP_PASSWORD = st.secrets["EMAIL_APP_PASSWORD"]
    return FROM_EMAIL, APP_PASSWORD


@tool
def schedule_appointment(
    user_id: str,
    counselling_id: str,
    start_time: str,
    end_time: str
):
    """
    Schedule a counselling appointment and send a calendar invite email.
    """

    # ---- Create ICS ----
    FROM_EMAIL, APP_PASSWORD = get_email_credentials()
    cal = Calendar()
    event = Event()
    event.name = "Counselling Session - FreeMind AI"
    event.begin = start_time
    event.end = end_time
    event.description = "Follow-up mental health counselling session"
    cal.events.add(event)

    ics_content = cal.serialize()

    # ---- Email ----
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = user_id
    msg["Subject"] = "Counselling Session - FreeMind AI"

    body = (
            "Hello,\n\n"
            "Your appointment has been scheduled.\n\n"
            "To continue your counselling, please keep your Counselling ID handy:\n"
            f"Counselling ID: {counselling_id}\n\n"
            "Please find the calendar invite attached.\n\n"
            "If you have any questions, feel free to reach out.\n"
            "We are here to support you.\n\n"
            "Warm regards,\n"
            "FreeMind AI Counselling Team"
        )
    msg.attach(MIMEText(body, "plain"))

    part = MIMEBase("text", "calendar", method="REQUEST")
    part.set_payload(ics_content)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=appointment.ics")
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    return "Appointment email sent successfully, appointment date and time starts from {start_time} and ends at {end_time}"
