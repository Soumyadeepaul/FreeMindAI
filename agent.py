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
    print("same")
    return chain.invoke({
        "designation": "Psychiatrist"
    })


# ------------------------------------------------------------------
# MAIN AGENT
# ------------------------------------------------------------------
def agent(question, id, counsellingID):
    llm = _get_llm()
    print("agent")
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
    print("agent")
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
    print(id)
    print(extracted)
    # Detect tool calls
    tool_calls = []
    if hasattr(extracted, "tool_calls") and extracted.tool_calls:
        tool_calls = extracted.tool_calls
    else:
        tool_calls = extracted.additional_kwargs.get("tool_calls", [])

    tool_result = None
    print(tool_calls)

    # -------------------------------------------------------------------
    # 1️⃣ TOOL MODE — LLM decided to call findNearestPsychiatrists
    # -------------------------------------------------------------------
    if tool_calls:
        for call in tool_calls:
            name = call["name"]
            args = call["args"]

            if name == "findNearestPsychiatrists":
                tool_result = findNearestPsychiatrists.invoke(args)
            elif name == "play_spotify_music":
                tool_result = play_spotify_music.invoke(args)
            elif name == "schedule_appointment":
                tool_result = schedule_appointment.invoke(args)

        # Take tool result → convert to friendly message using prompt4
        qa_prompt = ChatPromptTemplate.from_template(Prompts.prompt4())
        tool_chain = qa_prompt | llm | StrOutputParser()

        final_answer = tool_chain.invoke({
            "tool_result": tool_result,
            "question": question,
            "designation": "Psychiatrist"
        })

        # Save conversation
        append_message(id, counsellingID, "user", question)
        append_message(id, counsellingID, "agent", final_answer)

        return final_answer

    # -------------------------------------------------------------------
    # 2️⃣ NORMAL MODE — LLM did NOT call tool
    # The LLM only returns a plain psychological issue string.
    # -------------------------------------------------------------------
    else:
        # Gemini content always looks like: [{"type":"text","text":"..."}]
        issue_text = extracted.content[0]["text"].strip()

        # Vector match
        top3match = VectorMatching.vectorMatch(issue_text)
        previousChat = get_conversation(id,counsellingID)

        qa_prompt = ChatPromptTemplate.from_template(Prompts.prompt3())
        qa_chain = qa_prompt | llm | StrOutputParser()

        final_answer = qa_chain.invoke({
            "designation": "Psychiatrist",
            "history": previousChat,
            "question": question,
            "context": top3match
        })

        append_message(id,counsellingID, "user", question)
        append_message(id,counsellingID, "agent", final_answer)

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




