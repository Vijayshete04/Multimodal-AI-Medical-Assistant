import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- STEP 1: AUDIO RECORDER ---
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert to MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            
            # Export and ensure the file is flushed to disk
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred during recording: {e}")

# --- STEP 2: STT TRANSCRIPTION ---
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found."
    
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        # CRITICAL FIX: Use 'with' statement so the file is 
        # automatically closed after the upload is finished.
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return f"Error: {str(e)}"

# --- TEST EXECUTION ---
if __name__ == "__main__":
    api_key = os.environ.get("GROQ_API_KEY")
    model = "whisper-large-v3"
    test_path = "patient_voice_test.mp3"
    
    # record_audio(test_path)
    # text = transcribe_with_groq(model, test_path, api_key)
    # print(f"Transcription: {text}")