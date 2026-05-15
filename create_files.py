# -*- coding: utf-8 -*-
files = {
'requirements.txt': '''langgraph
langchain
langchain-openai
openai
streamlit
python-dotenv
requests
beautifulsoup4
''',
'.gitignore': '''.env
__pycache__/
*.pyc
venv/
.DS_Store
db/tracker.db
''',
'agent/state.py': '''from typing import TypedDict

class JobState(TypedDict):
    input: str
    raw_text: str
    summary: str
    stored_id: int
''',
'agent/nodes.py': '''import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from agent.state import JobState

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def fetch_jd(state: JobState) -> JobState:
    try:
        response = requests.get(state["input"], timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        state["raw_text"] = soup.get_text()[:3000]
    except:
        state["raw_text"] = state["input"]
    return state

def extract_requirements(state: JobState) -> JobState:
    prompt = f"""Extract key info from this job description:
{state["raw_text"]}

Return a clean summary with:
- Role
- Required Skills
- Experience Level
- Responsibilities
"""
    response = llm.invoke(prompt)
    state["summary"] = response.content
    return state

def store_to_db(state: JobState) -> JobState:
    import sqlite3, os
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect("db/tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT,
            summary TEXT
        )
    """)
    cursor.execute("INSERT INTO jobs (input, summary) VALUES (?, ?)",
                   (state["input"], state["summary"]))
    conn.commit()
    state["stored_id"] = cursor.lastrowid
    conn.close()
    return state
''',
'agent/graph.py': '''from langgraph.graph import StateGraph, END
from agent.state import JobState
from agent.nodes import fetch_jd, extract_requirements, store_to_db

def build_graph():
    graph = StateGraph(JobState)
    graph.add_node("fetch_jd", fetch_jd)
    graph.add_node("extract_requirements", extract_requirements)
    graph.add_node("store_to_db", store_to_db)
    graph.set_entry_point("fetch_jd")
    graph.add_edge("fetch_jd", "extract_requirements")
    graph.add_edge("extract_requirements", "store_to_db")
    graph.add_edge("store_to_db", END)
    return graph.compile()
''',
'agent/__init__.py': '',
'app.py': '''import streamlit as st
from dotenv import load_dotenv
from agent.graph import build_graph
import sqlite3, os

load_dotenv()

st.title("Job Tracker Agent")
st.write("Paste a job description URL or raw text below.")

user_input = st.text_area("Job Description URL or Text:", height=200)

if st.button("Track Job"):
    if user_input.strip():
        with st.spinner("Agent processing..."):
            graph = build_graph()
            result = graph.invoke({"input": user_input, "raw_text": "", "summary": "", "stored_id": 0})
        st.success("Job tracked successfully!")
        st.write("### Summary")
        st.write(result["summary"])
    else:
        st.warning("Please enter a URL or job description text.")

st.write("---")
st.write("### Tracked Jobs")
if os.path.exists("db/tracker.db"):
    conn = sqlite3.connect("db/tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, input, summary FROM jobs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        with st.expander(f"Job #{row[0]} - {row[1][:50]}"):
            st.write(row[2])
else:
    st.info("No jobs tracked yet.")
'''
}

import os
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {path}")

print("All files created!")