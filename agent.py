from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

import VectorMatching
from chat_db import append_message, get_conversation
from tools.tool1_findNearest import findNearestPsychiatrists
from tools.tool2_playMusic import play_spotify_music
from tools.tool3_appointmentTracker import schedule_appointment
import prompts as Prompts
from datetime import datetime
import streamlit as st

# ------------------------------------------------------------------
# GLOBAL LLM (REUSED)
# ------------------------------------------------------------------
llm = None


# ------------------------------------------------------------------
# INITIALIZE LLM
# ------------------------------------------------------------------
def _get_llm():
    global llm
    if llm is None:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=st.secrets["GEMINI_API_KEY"],
            temperature=0.2
        )
    return llm


# ------------------------------------------------------------------
# BOOTSTRAP RESPONSE (WELCOME MESSAGE)
# ------------------------------------------------------------------
def agentPrerequisites():
    llm = _get_llm()

    prompt = ChatPromptTemplate.from_template(Prompts.prompt1())
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "designation": "Psychiatrist"
    })


# ------------------------------------------------------------------
# MAIN AGENT
# ------------------------------------------------------------------
def agent(question, id, counsellingID):
    llm = _get_llm()

    # -------- sanitize inputs --------
    question = question or ""
    id = id or ""
    counsellingID = counsellingID or ""
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(question,id,counsellingID,date_time)

    # -------- bind tools --------
    tools = [
        findNearestPsychiatrists,
        play_spotify_music,
        schedule_appointment
    ]
    llm_with_tools = llm.bind_tools(tools)

    # -------- extraction chain --------
    extract_prompt = ChatPromptTemplate.from_template(Prompts.prompt2())
    extract_chain = extract_prompt | llm_with_tools

    extracted = extract_chain.invoke({
        "designation": "Psychiatrist",
        "question": "HI i am fine",
        "email": "paulsoumyadeep344@gmail.com",
        "counsellingID": "1",
        "dateTime": "2025-12-27 22:12"
    })

    # ------------------------------------------------------------------
    # TOOL CALL HANDLING (LANGCHAIN SAFE)
    # ------------------------------------------------------------------
    tool_calls = extracted.additional_kwargs.get("tool_calls", [])

    if tool_calls:
        tool_result = None

        for call in tool_calls:
            name = call["name"]
            args = call["args"]

            if name == "findNearestPsychiatrists":
                tool_result = findNearestPsychiatrists.invoke(args)
            elif name == "play_spotify_music":
                tool_result = play_spotify_music.invoke(args)
            elif name == "schedule_appointment":
                tool_result = schedule_appointment.invoke(args)

        qa_prompt = ChatPromptTemplate.from_template(Prompts.prompt4())
        tool_chain = qa_prompt | llm | StrOutputParser()

        final_answer = tool_chain.invoke({
            "tool_result": tool_result,
            "question": question,
            "designation": "Psychiatrist"
        })

        append_message(id, counsellingID, "user", question)
        append_message(id, counsellingID, "agent", final_answer)

        return final_answer

    # ------------------------------------------------------------------
    # NORMAL CHAT MODE (NO TOOL)
    # ------------------------------------------------------------------
    issue_text = extracted.content[0]["text"].strip()

    context = VectorMatching.vectorMatch(issue_text)
    history = get_conversation(id, counsellingID)

    qa_prompt = ChatPromptTemplate.from_template(Prompts.prompt3())
    qa_chain = qa_prompt | llm | StrOutputParser()

    final_answer = qa_chain.invoke({
        "designation": "Psychiatrist",
        "history": history,
        "question": question,
        "context": context
    })

    append_message(id, counsellingID, "user", question)
    append_message(id, counsellingID, "agent", final_answer)

    return final_answer


# ------------------------------------------------------------------
# MEDICAL REPORT AGENT
# ------------------------------------------------------------------
def medicalReportAgent(id, counsellingID):
    llm = _get_llm()

    history = get_conversation(id, counsellingID)
    if not history:
        return {
            "patient": id,
            "problems_identified": ["No conversation found"],
            "remedies": ["Start counselling first"]
        }

    class MedicalReport(BaseModel):
        patient: str
        problems_identified: list[str]
        remedies: list[str]

    output_parser = PydanticOutputParser(pydantic_object=MedicalReport)

    prompt = ChatPromptTemplate.from_template(Prompts.prompt5())
    chain = prompt | llm | output_parser

    return chain.invoke({
        "designation": "Psychologist",
        "previousChat": history,
        "format_instructions": output_parser.get_format_instructions()
    })


