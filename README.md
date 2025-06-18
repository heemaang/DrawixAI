# 🧠 DarwixAI – Audio Transcription & Blog Title Suggestion API

DarwixAI is a FastAPI-based service that provides:

- 🎙️ **Speech-to-Text Transcription** using Groq’s Whisper model  
- 📝 **Blog Title Generation** using Groq’s LLaMA3 model

---

## 🚀 Features

- Accepts MP3/WAV audio files for transcription  
- Returns clean text from spoken words  
- Suggests 3 relevant blog titles from any content  
- Docker-compatible & easy to deploy (e.g., Render)

---

## 🗂️ Folder Structure

```
DrawixAI/
│
├── app.py                    # Main FastAPI app
├── stt_model.py              # Whisper transcription logic (Groq)
├── requirements.txt          # Python dependencies
├── .env                      # API key configs (not committed)
├── Transcription.ipynb       # Jupyter notebook (testing)
├── transcription_output.json # Sample JSON output from Whisper
├── README.md                 # This file
├── convo.mp3                 # Test audio (optional)
└── .gitignore                # Files/folders to ignore in Git
```

---

## 🛠️ Setup (Locally)

### 1. Clone the Repository

```bash
git clone https://github.com/heemaang/DrawixAI.git
cd DrawixAI
```

### 2. Create a Virtual Environment & Install Requirements

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key
API_KEY=MY_SUPER_SECRET
```

---

## ▶️ Running the App Locally

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

Your app will now be running at:  
**🌐 http://localhost:8080**

---

## 🔁 API Endpoints (Local)

### 🎙️ /transcribe

- **Method:** POST  
- **URL:** `http://localhost:8080/transcribe`  
- **Headers:**  
  - `x-api-key: MY_SUPER_SECRET`  
- **Body (form-data):**  
  - `file`: MP3/WAV audio file

**Sample cURL:**

```bash
curl -X POST http://localhost:8080/transcribe \
  -H "x-api-key: MY_SUPER_SECRET" \
  -F "file=@convo.mp3"
```

---

### 📝 /api/suggest-titles

- **Method:** POST  
- **URL:** `http://localhost:8080/api/suggest-titles`  
- **Headers:**  
  - `x-api-key: MY_SUPER_SECRET`  
- **Body (JSON):**

```json
{
  "text": "Artificial intelligence is transforming industries by automating complex tasks..."
}
```

**Response:**

```json
{
  "suggestions": [
    "How AI is Transforming Industries",
    "The Rise of Automation in Modern Business",
    "AI & the Future of Work"
  ]
}
```

