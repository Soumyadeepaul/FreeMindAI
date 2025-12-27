from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import VectorMatching
import os
from chat_db import append_message, get_conversation
from tools.tool1_findNearest import findNearestPsychiatrists
from tools.tool2_playMusic import play_spotify_music
from tools.tool3_appointmentTracker import schedule_appointment
import prompts as Prompts
from datetime import datetime
import streamlit as st

load_dotenv()


# Global variables for reuse
llm = None

def agentPrerequisites():
    global llm
    api_key = st.secrets["GEMINI_API_KEY"]
    # -------------------------
    # SETUP GEMINI LLM
    # -------------------------
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.2
    )
    
    # -------------------------
    # PROMPT WITH PDF KNOWLEDGE
    # -------------------------
    template = Prompts.prompt1()

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "designation": "Psychiatrist",
    })

    return response
################################################################################
import json
def agent(question,id,counsellingID):
    global llm
    if not llm: 
        api_key = st.secrets["GEMINI_API_KEY"]
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=api_key,
            temperature=0.2
        )
    # Bind tools
    tools = [findNearestPsychiatrists,play_spotify_music,schedule_appointment]
    llm_with_tool = llm.bind_tools(tools)

    # Run extraction LLM (this may or may not call a tool)
    extract_prompt = ChatPromptTemplate.from_template(Prompts.prompt2())
    extract_chain = extract_prompt | llm_with_tool
    extracted = extract_chain.invoke({"designation": "Psychiatrist","question": question,"email":id, "counsellingID" : counsellingID, "dateTime":datetime.now()})
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




#################################################################################
def medicalReportAgent(id,counsellingID):
    global llm

    if not llm:
        print("ERROR in Report Agent")
        return
    # previousChat = ""

    # # Load chat history
    # try:
    #     with open("chat_history.txt", "r") as f:
    #         previousChat = f.read()
    # except FileNotFoundError:
    #     previousChat = ""

    previousChat = get_conversation(id,counsellingID)

    if previousChat== "":
        return {"problems_identified":"Chat is empty", "remedies":"Start your counselling"}

    # --------------------------
    # 1️⃣ DEFINE Pydantic Schema 
    # --------------------------
    class MedicalReport(BaseModel):
        patient: str = Field(
            description="Name of the patient"
        )
        problems_identified: list[str] = Field(
            description="Short list of possible psychological or emotional issues in maximum 4 words each"
        )
        remedies: list[str] = Field(
            description="Short friendly coping steps or remedies in maximum 7 words each"
        )

    # --------------------------
    # 2️⃣ Create the output parser
    # --------------------------
    output_parser = PydanticOutputParser(pydantic_object=MedicalReport)
    format_instructions = output_parser.get_format_instructions()

    # --------------------------
    # 3️⃣ Create the prompt
    # --------------------------
    prompt = ChatPromptTemplate.from_template(Prompts.prompt5())
    # --------------------------
    # 4️⃣ Build chain using LCEL
    # --------------------------
    chain = prompt | llm | output_parser

    # --------------------------
    # 5️⃣ Execute chain
    # --------------------------
    parsed_output = chain.invoke({
        "designation": "Psychologist",
        "previousChat": previousChat,
        "format_instructions": format_instructions
    })

    return parsed_output
