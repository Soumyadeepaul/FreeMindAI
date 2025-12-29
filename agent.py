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



def agent(question, id, counsellingID):
    llm = _get_llm()
    print("agent")

    # -------- sanitize inputs --------
    question = question or ""
    id = id or ""
    counsellingID = counsellingID or ""
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(question, id, counsellingID, date_time)

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
        "question": question,
        "email": id,
        "counsellingID": counsellingID,
        "dateTime": date_time
    })
    print(extracted)

    # -------- detect tool calls (SAFE) --------
    tool_calls = extracted.additional_kwargs.get("tool_calls", [])
    tool_result = None

    # -------------------------------------------------------------------
    # 1️⃣ TOOL MODE
    # -------------------------------------------------------------------
    if tool_calls:
        for call in tool_calls:
            name = call["name"]
            args = call["args"]

            if name == "findNearestPsychiatrists":
                tool_result = findNearestPsychiatrists.invoke(args)

            elif name == "play_spotify_music":
                tool_result = play_spotify_music.invoke(args)

                # 🔑 RETURN MUSIC RESULT DIRECTLY
                append_message(id, counsellingID, "user", question)
                append_message(
                    id,
                    counsellingID,
                    "agent",
                    f"Recommended song: {tool_result.get('song')}"
                )
                print(tool_result)
                return tool_result

            elif name == "schedule_appointment":
                tool_result = schedule_appointment.invoke(args)

        # ---- other tools still go through prompt4 ----
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

    # -------------------------------------------------------------------
    # 2️⃣ NORMAL MODE (NO TOOL)
    # -------------------------------------------------------------------
    else:
        # 🔧 FIXED Gemini extraction
        issue_text = extracted.content.strip()

        top3match = VectorMatching.vectorMatch(issue_text)
        previousChat = get_conversation(id, counsellingID)

        qa_prompt = ChatPromptTemplate.from_template(Prompts.prompt3())
        qa_chain = qa_prompt | llm | StrOutputParser()

        final_answer = qa_chain.invoke({
            "designation": "Psychiatrist",
            "history": previousChat,
            "question": question,
            "context": top3match
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



