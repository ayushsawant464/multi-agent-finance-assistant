# streamlit_app/main.py

import streamlit as st
import requests

st.title("🎙️ Finance Assistant")

option = st.radio("How would you like to interact?", ["Text", "Voice"])

if option == "Text":
    user_query = st.text_input("Ask your financial question...")
    if st.button("Submit") and user_query:
        response = requests.post("http://localhost:8000/query", params={"question": user_query})
        st.write(response.json()["response"])

elif option == "Voice":
    audio_file = st.file_uploader("Upload your question (WAV)", type=["wav"])
    if audio_file and st.button("Submit Voice"):
        response = requests.post("http://localhost:8000/voice", files={"file": audio_file})
        result = response.json()
        st.write(f"**You said:** {result['query']}")
        st.write(f"**Assistant:** {result['response']}")
