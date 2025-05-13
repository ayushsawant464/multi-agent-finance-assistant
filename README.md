#   Multi-Agent Finance Assistant

An open-source, multi-agent voice-enabled assistant that delivers daily market briefs to portfolio managers. Built with CrewAI, LangGraph, FastAPI, Whisper, and Streamlit.

---

##  Use Case (Change prompts/configs as desired)



**Prompt (8 AM daily):**
 "What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"

**Response:**
"Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt due to rising yields."

---


##  Architecture Overview


### Components
- `/agents`: Specialized agents (API, Scraper, Retriever, LLM, Voice)
- `/orchestrator`: FastAPI microservices orchestrating agent logic
- `/streamlit_app`: Frontend for user input and verbal responses
- `/data_ingestion`: Data preprocessing (changes are yet to be done)
- `/docs`: Tool usage logs, prompt engineering

---

## 🛠️ Setup Instructions

### 1. Clone & Install
```bash
git clone https://github.com/ayushsawant464/multi-agent-finance-assistant
cd multi-agent-finance-assistance
pip install -r requirements.txt

