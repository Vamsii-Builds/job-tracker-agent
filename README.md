\# 🤖 Job Tracker Agent — LangGraph Multi-Step Agent



> A LangGraph agent that reads job descriptions, extracts structured requirements, and stores them for side-by-side comparison — built as a hands-on exercise in agent state management and tool invocation.



!\[LangGraph](https://img.shields.io/badge/LangGraph-2D6A4F?style=flat-square)

!\[OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square\&logo=openai\&logoColor=white)

!\[SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square\&logo=sqlite\&logoColor=white)

!\[Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square\&logo=streamlit\&logoColor=white)



\---



\## 🧠 What It Does



Paste a job description URL or raw text → the agent extracts structured information (required skills, experience level, responsibilities, compensation if listed) → stores it in SQLite → lets you compare multiple JDs side by side in a Streamlit dashboard.



\*\*What this project is really about:\*\* practicing LangGraph's stateful graph execution, conditional edges, and tool calling — not just chaining LLM calls.



\---



\## 🏗️ Agent Architecture



```

User Input (JD URL or text)

&#x20;       │

&#x20;       ▼

&#x20;  ┌─── START ───┐

&#x20;  │             │

&#x20;  ▼             ▼

\[fetch\_jd]   \[parse\_text]    ← conditional on input type

&#x20;       │

&#x20;       ▼

&#x20;  \[extract\_requirements]    ← structured output via OpenAI function calling

&#x20;       │

&#x20;       ▼

&#x20;  \[store\_to\_db]             ← writes to SQLite

&#x20;       │

&#x20;       ▼

&#x20;  \[summarize]               ← human-readable summary

&#x20;       │

&#x20;       ▼

&#x20;     END

```



\*\*State schema:\*\*

```python

class JobState(TypedDict):

&#x20;   input: str

&#x20;   raw\_text: str

&#x20;   extracted: JobRequirements

&#x20;   stored\_id: int

&#x20;   summary: str

```



\---



\## ⚙️ Setup



```bash

git clone https://github.com/vamsii-Builds/job-tracker-agent

cd job-tracker-agent

pip install -r requirements.txt



export OPENAI\_API\_KEY=your\_key\_here



\# Run the Streamlit app

streamlit run app.py



\# Or run the agent directly from CLI

python agent.py --input "https://jobs.example.com/ml-engineer"

```



\---



\## 📁 Project Structure



```

job-tracker-agent/

├── agent/

│   ├── graph.py           # LangGraph state graph definition

│   ├── nodes.py           # Individual node functions

│   ├── state.py           # TypedDict state schema

│   └── tools.py           # Tool definitions (fetch, store, extract)

├── db/

│   └── tracker.db         # SQLite database (auto-created)

├── app.py                 # Streamlit dashboard

├── requirements.txt

└── README.md

```



\---



\## 🖥️ Dashboard Features



\- \*\*Add JD\*\* — paste URL or raw text, agent processes it automatically

\- \*\*Compare\*\* — select 2–3 JDs to see skill overlap and differences

\- \*\*Filter\*\* — filter stored JDs by skill, experience level, or date added

\- \*\*Export\*\* — download comparison as CSV



\---



\## 📌 What I Learned



\- LangGraph's `StateGraph` is much cleaner than manual chain orchestration for multi-step workflows — especially when state needs to branch or loop

\- Conditional edges (`add\_conditional\_edges`) let you write clear decision logic without nested if/else inside nodes

\- OpenAI function calling is the right tool for structured extraction — much more reliable than prompt-engineering the JSON format

\- SQLite is perfectly fine for local agent memory; you don't always need a vector DB



\---



\## 🔮 Potential Extensions



\- \[ ] Add a "match score" node that compares JD requirements against a resume

\- \[ ] Integrate email notifications when a matching JD is added

\- \[ ] Add a memory node that learns your preferences over time



\---



\## 🔗 Related Projects



\- \[DocChat](https://github.com/vamsii-Builds/docchat) — RAG-powered PDF chatbot

\- \[FineTune Lab](https://github.com/vamsii-Builds/finetune-lab) — QLoRA fine-tuning sandbox

