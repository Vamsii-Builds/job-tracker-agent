import streamlit as st
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
