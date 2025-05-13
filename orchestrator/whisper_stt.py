
import whisper
import tempfile
import os

model = whisper.load_model("base")

def transcribe_audio(file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(file.read())
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    os.remove(temp_audio_path)
    return result["text"]
