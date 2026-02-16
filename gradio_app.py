import os
import gradio as gr
import platform
import asyncio
import time

# --- FIX FOR WINDOWS ASYNCIO ERROR ---
if platform.system() == 'Win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Importing your custom modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# System prompt for the AI Doctor
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = "No voice input provided."
    doctor_response = ""
    voice_of_doctor_path = None

    try:
        # 1. Handle Audio (Transcription)
        if audio_filepath:
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )

        # 2. Handle Image (Analysis)
        if image_filepath:
            try:
                encoded_img = encode_image(image_filepath)
                doctor_response = analyze_image_with_query(
                    query=system_prompt + speech_to_text_output, 
                    encoded_image=encoded_img, 
                    model="meta-llama/llama-4-scout-17b-16e-instruct"
                )
            except Exception as img_err:
                doctor_response = f"Error processing image: {str(img_err)}"
        else:
            doctor_response = "No image provided for analysis. Please upload a photo for a medical assessment."

        # 3. Handle Text-to-Speech (THE WINDOWS STABILITY FIX)
        if doctor_response:
            # Generate a unique filename using timestamp to avoid "Content-Length" errors/file locks
            unique_filename = f"doctor_voice_{int(time.time())}.mp3"
            
            # Clean up old mp3 files to prevent folder clutter (optional)
            for f in os.listdir():
                if f.startswith("doctor_voice_") and f.endswith(".mp3"):
                    try: os.remove(f)
                    except: pass
            
            voice_of_doctor_path = text_to_speech_with_gtts(
                input_text=doctor_response, 
                output_filepath=unique_filename
            )

    except Exception as e:
        doctor_response = f"A system error occurred: {str(e)}"

    return speech_to_text_output, doctor_response, voice_of_doctor_path

# --- UI SETUP ---

# --- CUSTOM CSS FOR THE PROFESSIONAL LOOK ---

custom_css = """

.gradio-container { background-color: #f8fafc; font-family: 'Inter', sans-serif; }

#header-container { 

    background: white; 

    padding: 20px; 

    border-radius: 12px; 

    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

    border: 1px solid #e2e8f0;

    margin-bottom: 25px;

}

.header-flex { 

    display: flex; 

    align-items: center; 

    justify-content: center; 

    gap: 20px; 

}

.logo-text { font-size: 24px; font-weight: 800; color: #1e293b; }

.medical-icons { font-size: 24px; color: #3b82f6; display: flex; gap: 10px; }

#submit-btn { background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%) !important; color: white !important; border: none !important; }

#clear-btn { background: white !important; color: #ef4444 !important; border: 1px solid #fee2e2 !important; }

.panel-box { background: white; border-radius: 10px; padding: 15px; border: 1px solid #e2e8f0; }

"""



with gr.Blocks(theme=gr.themes.Soft()) as demo:

        # Header with medical branding

    with gr.Row(elem_id="header-container"):

        gr.HTML("""

            <div class="header-flex">

                <span style="font-size: 40px;">🏥</span>

                <div>

                    <div class="logo-text">AI HEALTH <span style='color: #3b82f6;'>SOLUTIONS</span></div>

                </div>

                <div class="medical-icons">

                    <span>🧠</span><span>🎙️</span><span>🩺</span>

                </div>

                <div style="border-left: 2px solid #e2e8f0; height: 30px; margin: 0 20px;"></div>

                <h1 style="margin: 0; font-size: 20px; color: #475569;">Digital Doctor Consultation</h1>

            </div>

        """)



    with gr.Row():

        # Input Section

        with gr.Column(scale=1):

            with gr.Group(elem_classes="panel-box"):

                gr.Markdown("### 📥 Patient Records")

                input_image = gr.Image(label="Upload Diagnostic Image", type="filepath")

                input_audio = gr.Audio(label="Voice Symptoms", sources=["microphone"], type="filepath")

                

                with gr.Row():

                    submit_btn = gr.Button("🩺 Run Analysis", variant="primary", elem_id="submit-btn")

                    clear_btn = gr.Button("🗑️ Reset", elem_id="clear-btn")



        # Output Section

        with gr.Column(scale=1):

            with gr.Group(elem_classes="panel-box"):

                gr.Markdown("### 📋 Medical Assessment")

                stt_display = gr.Textbox(label="Patient Speech Transcription", lines=2)

                doctor_display = gr.Textbox(label="AI Doctor's Advice", lines=10)

                audio_display = gr.Audio(label="Playback Voice Diagnosis", autoplay=True)



    # Wire up the logic

    submit_btn.click(

        fn=process_inputs,

        inputs=[input_audio, input_image],

        outputs=[stt_display, doctor_display, audio_display]

    )



    clear_btn.click(
        lambda: (None, None, "", "", None),
        inputs=None,
        outputs=[input_audio, input_image, stt_display, doctor_display, audio_display]
    )


if __name__ == "__main__":
    # max_threads=1 is safer for Windows file operations
    demo.launch(
    share=True,
    show_error=True
    )