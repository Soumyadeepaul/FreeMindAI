🧠 FreeMindAI
Agentic AI–Powered Mental Health Counselling Platform

FreeMindAI is an agentic AI mental health counselling system built using LangChain, LLMs, and Streamlit.
It is designed to guide users step by step, remember past counselling context, use external tools when required, and generate structured medical-style counselling reports.
This project was built through a joint effort between the developer and ChatGPT, where AI was used as a thinking and debugging partner, not just a chatbot.

📌 Problem Statement
Access to mental health support is still limited for many people.

A large number of individuals:
  Cannot afford regular psychiatrist or therapist sessions
  Are introverted or uncomfortable speaking openly with others
  Have limited time due to work, study, or personal responsibilities
  Need immediate, private, and free counselling support

Mental health support requires:
  Step-by-step guidance
  Contextual memory
  Secure data handling
  Structured reports
  Optional escalation to professionals

FreeMindAI addresses these gaps using Agentic AI.

🎯 What FreeMindAI Does

FreeMindAI acts as an AI counsellor that can:
Conduct counselling conversations step by step
Maintain conversation memory across sessions
Retrieve past counselling data using RAG (Retrieval-Augmented Generation)
Generate medical-style counselling reports (PDF)

Use external tools such as:
Finding nearby psychiatrists
Scheduling appointments (Google Calendar via Mail)
Supportive actions (e.g., music guidance)

Secure sensitive patient data using:

Login / Signup
PIN-based access control
Store and display counselling history
Collect user feedback
Run as a multi-page Streamlit web application
Be deployed as a complete product

🧱 System Architecture (High Level)
User
 │
 ▼
Streamlit UI (Multi-page App)
 │
 ▼
Agent Controller (LangChain)
 │
 ├─ LLM (Reasoning + Decision Making)
 ├─ Memory (Conversation + Counselling Context)
 ├─ RAG (Past Counselling Records)
 ├─ Tool Router
 │     ├─ Psychiatrist Finder Tool
 │     ├─ Appointment Scheduler Tool
 │     └─ Other Support Tools
 │
 ▼
Response Generator
 │
 ▼
PDF Generator / UI Output

🔄 Workflow (Step-by-Step)
User Login
User signs up or logs in
Optional PIN verification for sensitive data
Counselling Session Starts
Agent greets user
Identifies emotional state
Guides the conversation step by step
Agent Reasoning
Uses LLM to understand intent

Decides whether:
Simple counselling is enough
Memory retrieval is needed
A tool must be invoked
Memory & RAG
Past counselling sessions retrieved when needed
Context injected into prompt
Ensures continuity across sessions
Tool Calling (If Required)
Agent decides to call tools (not hard-coded)

Example:

Find psychiatrist near location
Schedule appointment
Tool output is passed back to the agent
Medical Report Generation
Structured counselling summary created
Converted into a downloadable PDF medical report
Session Storage
Counselling data saved
Linked with unique user ID and counselling ID
Feedback Collection

User can submit feedback after session

🔁 Data Flow
User Input
  ↓
Streamlit UI
  ↓
Agent Prompt Builder
  ↓
LLM (Reasoning)
  ↓
Memory / RAG (Optional)
  ↓
Tool Invocation (Optional)
  ↓
Final Response
  ↓
UI Display + Data Storage
  ↓
Medical Report (PDF)

🧠 Agent Design (Important)

FreeMindAI is not a prompt-based chatbot.

It uses:
Agentic flow
Tool calling via LangChain
Separate prompt files
Explicit reasoning + action separation
Key learnings applied:
Functions ≠ Tools
Tool calling must be model-driven
Prompts must be modular and isolated
Memory must be scoped per counselling session

🗂️ Features Overview
Core AI
LangChain Agent
LLM reasoning
Tool calling
Memory configuration
RAG with vector database

Application
Streamlit multi-page UI
Login / Signup / Logout
Profile management
Counselling tabs
Counselling history
Security
PIN-based access control
User-level data isolation
Reports
Medical-style counselling reports
PDF generation

Tools
Psychiatrist search (location-based)
Appointment scheduling (Google Calendar)
Extensible tool architecture

🛠️ Tech Stack
Language: Python
Frameworks: LangChain, Streamlit
LLM: OpenAI / HuggingFace (configurable)
Vector Store: Pinecone
PDF: ReportLab
Database: SQLite / File-based (extendable)
Auth: Custom authentication + PIN system

📅 Development Timeline (Summary)
Built over 30 days
Included multiple pauses for redesign and debugging
Tool calling understanding evolved gradually
Focused on correctness over speed
Deployed only after stability

🚀 Deployment
Streamlit-based deployment
Environment variables used for API keys
GitHub repository cleaned and structured before deployment

🤝 Collaboration with AI
This project was built through a joint effort between the developer and ChatGPT.

AI was used as:
A design reviewer
A debugging assistant
A reasoning partner
An architecture validator
Not as a shortcut — but as a collaborator.

🔮 Future Improvements

Better long-term memory summarization
Multi-language counselling
Doctor dashboard
Analytics for counselling trends
Production-grade database
Role-based access

📄 Disclaimer

FreeMindAI is a technical and educational project.
It does not replace professional mental health care.

⭐ Final Note

FreeMindAI represents learning by building, honest failures, pauses, and gradual clarity.
If you are exploring Agentic AI, LangChain, or real-world LLM systems, this project may help you understand what actually works.
