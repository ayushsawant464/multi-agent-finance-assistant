
from fastapi import FastAPI, UploadFile
from orchestrator.whisper_stt import transcribe_audio
from orchestrator.tts import speak_text
from agents.crew import  build_crew_with_query

app = FastAPI()

@app.post("/query")
async def query_user(question: str):
    crew = build_crew_with_query(question)
    result = crew.kickoff()
    speak_text(result)
    return {"response": result}

@app.post("/voice")
async def voice_input(file: UploadFile):
    query = transcribe_audio(file.file)
    crew = build_crew_with_query(query)
    result = crew.kickoff(inputs={"query": query})
    speak_text(str(result))
    return {"query": query, "response": result}
