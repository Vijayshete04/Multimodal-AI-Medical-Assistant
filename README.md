# AI Medical Bot

An interactive medical assistant that combines **vision** and **voice** capabilities to provide medical insights. The bot can analyze medical images and respond to voice queries, delivering responses in both **text** and **voice** format.

![AI Medical Bot](Output/output.gif)

## Deployment Link

You can access the live deployment of this AI Medical Bot on Hugging Face Spaces:

[AI Medical Bot on Hugging Face Spaces](https://huggingface.co/spaces/AlokAhirrao/AI_MEDICAL_BOT)

---

## Features

- 🎤 **Voice Input**: Record your medical questions using your microphone.
- 🖼️ **Image Analysis**: Upload medical images for AI analysis.
- 🗣️ **Voice Output**: Receive responses in both text and voice format.
- 🤖 **Professional Doctor Simulation**: AI responds as a medical professional.
- 🔄 **Real-time Processing**: Quick analysis and response generation.

---

## Prerequisites

To run this project, you need the following:

- **Python 3.8 or higher**
- **GROQ API Key**: You can obtain this from the [GROQ platform](https://www.groq.com/).

---

## Installation

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Vijayshete04/Multimodal-AI-Medical-Assistant-Vision-to-Voice-
cd AI_MEDICAL_BOT
```

### 2. Create and Activate a Virtual Environment

It’s recommended to use a virtual environment for managing project dependencies. Run the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Required Dependencies

Once your virtual environment is activated, install all the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Your GROQ API Key

Create a `.env` file in the project root and add your **GROQ API Key**:

```
GROQ_API_KEY=your_api_key_here
```

---

## Usage

### 1. Run the Application

Start the application by running:

```bash
python app.py
```

### 2. Open the Interface

After starting the application, open your web browser and navigate to the local Gradio interface, which is typically accessible at:

[http://127.0.0.1:7860](http://127.0.0.1:7860)

### 3. Interact with the Bot

Use the interface to:

- 🎤 **Record a Question**: Speak into your microphone to ask the AI doctor a question.
- 🖼️ **Upload an Image**: Upload a medical image for analysis.
- 🗣️ **Receive Responses**: Get both **text** and **voice** responses from the AI doctor.

---

## Important Notes

- This application is for **educational purposes** only and should **not** replace professional medical advice or diagnosis.
- Ensure that **microphone permissions** are enabled on your device for voice input.
- Supported image formats: **JPG**, **PNG**.
- **Internet connection** is required for API calls and processing.

---

## License

Copyright (c) 2025, Vijay Shete

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.  
To view a copy of this license, visit [Creative Commons License](http://creativecommons.org/licenses/by-nc/4.0/).

You are free to:
- Share: Copy and redistribute the material in any medium or format.
- Adapt: Remix, transform, and build upon the material.

Under the following terms:
- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. 
  You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial**: You may not use the material for commercial purposes.

For permissions beyond the scope of this license, contact [vijayshete815@gmail.com]

## Disclaimer

This application is for **educational purposes** only. It should **not** be used as a substitute for professional medical advice, diagnosis, or treatment.