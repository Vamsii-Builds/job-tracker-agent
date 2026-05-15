import requests
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
