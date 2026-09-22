<div align="center">

# 🤖 JARVIS — AI Voice Assistant

### A modular Python AI voice assistant with a web interface, voice interaction, web search, automation, and optional OpenAI-powered responses.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Optional-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-8B5CF6?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

### 🌐 Live Web App

**[Launch JARVIS](https://jarvis-ai-voice-assistant.up.railway.app/)**

`Wake Word: "Jarvis"` • `Voice-Controlled` • `Web Interface` • `Modular Services` • `AI + Web Search`

</div>

---

## 🧠 What is JARVIS?

**JARVIS** is a modular Python-based AI voice assistant designed for hands-free interaction.

The project combines a Python assistant core with a Flask-powered web interface. Users can interact with JARVIS through the browser, while the underlying assistant routes commands to dedicated services for web search, weather, YouTube, browser actions, jokes, information retrieval, and optional AI-generated responses.

The application is also deployed publicly on **Railway**, allowing anyone to access the web interface without installing Python, VS Code, or the project locally.

---

## 🌐 Live Web Application

### Public URL

[**https://jarvis-ai-voice-assistant-production.up.railway.app/**](https://jarvis-ai-voice-assistant.up.railway.app/)

The public deployment provides a browser-based interface for interacting with JARVIS.

### Example interactions

```text
Tell me the weather in Chandigarh
Who created you?
Open YouTube
Search for Python tutorials
Tell me a joke
What is the date?
```

> **Deployment:** Railway  
> **Application server:** Flask + Gunicorn  
> **Public networking:** Railway-generated HTTPS domain

---

## ✨ Core Capabilities

| Capability | What JARVIS can do |
|---|---|
| 🎙️ **Voice Activation** | Detect the `"Jarvis"` wake word and capture spoken commands |
| 🌐 **Web Interface** | Interact with JARVIS through a browser-based UI |
| 🔊 **Speech Response** | Convert responses into spoken output |
| 🌐 **Web & Browser Automation** | Open websites, perform searches, and trigger browser actions |
| ▶️ **YouTube Control** | Search and play requested videos |
| 🌤️ **Information Retrieval** | Handle weather, date, time, sports, and general information queries |
| 🔎 **Web Search** | Search the web for current or general information |
| 😂 **Entertainment** | Generate jokes on demand |
| 🤖 **AI Intelligence** | Use OpenAI for conversational responses when configured |
| 🔄 **Fallback Handling** | Fall back to web search when the optional AI service is unavailable |
| 🚀 **Public Deployment** | Access the web application from any device through the Railway URL |

---

## 🏗️ Architecture

```text
                         USER
                    ┌──────┴──────┐
                    │             │
                 Browser      Local Voice
                    │             │
                    ▼             ▼
              ┌──────────┐   ┌───────────────┐
              │ Web UI    │   │ Speech Input  │
              │ HTML/CSS/ │   │ SpeechRecogn. │
              │ JavaScript│   └───────┬───────┘
              └────┬─────┘           │
                   │                 │
                   └────────┬────────┘
                            ▼
                    ┌───────────────┐
                    │ Flask Server  │
                    │   server.py   │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │ JARVIS Core   │
                    │ Assistant /   │
                    │ Command Logic │
                    └───────┬───────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Local Tasks      Services       AI / Web
        Date / Time      Browser        OpenAI
        Jokes            YouTube        Web Search
                         Weather
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     JARVIS Response
```

### Web deployment flow

```text
GitHub Repository
       │
       ▼
    Railway
       │
       ▼
 Flask + Gunicorn
       │
       ▼
 Public HTTPS Domain
       │
       ▼
 Any User / Any Device
```

---

## 💬 Example Commands

| Command | JARVIS action |
|---|---|
| `"Jarvis"` | Activates the assistant |
| `"Open YouTube"` | Opens YouTube |
| `"Play Believer"` | Searches and plays the requested video |
| `"Tell me the weather"` | Retrieves weather information |
| `"Tell me the weather in Chandigarh"` | Retrieves Chandigarh weather |
| `"What is the date?"` | Reports the current date |
| `"Tell me a joke"` | Generates a joke |
| `"Search for Python tutorials"` | Performs a web search |
| `"Who created you?"` | Generates an assistant response |
| `"What is the latest cricket score?"` | Searches for sports information |

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| 🐍 **Python** | Core application and orchestration |
| 🌐 **Flask** | Web server and REST API |
| ⚡ **Gunicorn** | Production WSGI server |
| 🎨 **HTML / CSS / JavaScript** | Browser-based JARVIS interface |
| 🎙️ **SpeechRecognition** | Speech-to-text input |
| 🎤 **PyAudio** | Local microphone access |
| 🔊 **pyttsx3** | Local text-to-speech output |
| ▶️ **PyWhatKit** | YouTube and browser automation |
| 😂 **PyJokes** | Joke generation |
| 🔔 **playsound3** | Local audio notifications |
| 🔎 **DDGS** | Web search |
| 🌐 **Requests** | HTTP/API requests |
| 🔐 **python-dotenv** | Environment configuration |
| 🤖 **OpenAI SDK** | Optional AI responses |
| 🚀 **Railway** | Public cloud deployment |

---

## 📂 Project Structure

```text
JARVIS-AI-VOICE-ASSISTANT/
│
├── assets/
│   └── sounds/                  # Audio assets
│
├── src/
│   └── jarvis/
│       ├── main.py              # Local JARVIS entry point
│       ├── assistant/           # Command processing & conversation
│       ├── audio/               # Speech recognition & TTS
│       └── services/            # Browser, weather, search & AI
│
├── web/
│   ├── index.html               # Web interface
│   ├── style.css                # Web UI styling
│   └── app.js                   # Frontend interaction logic
│
├── server.py                    # Flask web server / API
├── run_web.py                   # Web application launcher
├── Procfile                     # Production process definition
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Python project configuration
├── .env.example                 # Environment variable template
├── .gitignore
├── README.md
└── tests/                       # Automated tests
```

---

## ⚙️ Run JARVIS Locally

### 1. Clone the repository

```bash
git clone https://github.com/AnshTyagi2006/JARVIS-AI-VOICE-ASSISTANT.git
cd JARVIS-AI-VOICE-ASSISTANT
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\env\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install JARVIS

```bash
python -m pip install -e .
```

### 6. Run the local voice assistant

```bash
python -m jarvis.main
```

### 7. Run the web interface locally

```bash
python server.py
```

Then open:

```text
http://127.0.0.1:5000
```

The Flask server also exposes:

```text
GET /health
GET /api/info
POST /api/process_command
POST /api/listen
```

---

## 🚀 Railway Deployment

The current production web application is deployed on **Railway**.

### Deployment configuration

The project is connected directly to the GitHub repository:

```text
https://github.com/AnshTyagi2006/JARVIS-AI-VOICE-ASSISTANT
```

Railway builds the project and runs the Flask application with Gunicorn.

### Production start command

```bash
gunicorn server:app
```

Railway supplies the runtime `PORT`, and the application listens on the Railway-assigned port.

### Public domain

```text
https://jarvis-ai-voice-assistant-production.up.railway.app/
```

### Health endpoint

```text
https://jarvis-ai-voice-assistant.up.railway.app/health
```

Expected response:

```json
{
  "service": "JARVIS",
  "status": "ok"
}
```

### Continuous deployment

The Railway service is connected to the GitHub repository. New commits pushed to the configured branch can trigger a new deployment.

---

## 🔐 Environment Variables

JARVIS can operate without OpenAI, but the optional AI response layer requires an API key.

Create a local `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

For Railway, add the variable through the service's **Variables** settings:

```text
OPENAI_API_KEY = your_openai_api_key_here
```

> 🔒 Never commit `.env` or expose your API key in source code.

The repository includes `.env.example` as a safe configuration template.

---

## 🔄 AI Fallback

The optional AI layer is designed with a fallback path:

```text
             User Command
                  │
                  ▼
          ┌───────────────┐
          │ OpenAI Enabled│
          └───────┬───────┘
                  │
            Available?
             /        \
           Yes         No
            │           │
            ▼           ▼
       AI Response   Web Search
            │           │
            └─────┬─────┘
                  ▼
            JARVIS Response
```

This allows core functionality to remain available even when the optional AI service is not configured.

---

## 🧪 Testing

The project includes automated tests for core application behavior.

Run:

```bash
pytest
```

For a deployment smoke test, verify:

```text
/
 /health
 /api/info
 /api/process_command
```

The production health endpoint can be checked at:

```text
https://jarvis-ai-voice-assistant-production.up.railway.app/health
```

---

## 🗺️ Roadmap

- [ ] Improved intent classification
- [ ] Conversation memory
- [ ] Offline speech recognition
- [ ] Dedicated sports-data integration
- [ ] Expanded automated testing
- [ ] More browser automation capabilities
- [ ] Additional AI tools and integrations
- [ ] Improved mobile voice interaction

---

## 📜 License

Licensed under the **MIT License**.

---

## 👤 Author

<div align="center">

### Ansh Tyagi

**B.Tech — Artificial Intelligence & Data Science**

<a href="https://github.com/AnshTyagi2006">
  <img src="https://img.shields.io/badge/GitHub-AnshTyagi2006-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
<a href="https://www.linkedin.com/in/ansh-tyagi2006/">
  <img src="https://img.shields.io/badge/LinkedIn-Ansh%20Tyagi-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>

<br><br>

⭐ **If you find JARVIS useful, consider giving the repository a star.**

</div>
