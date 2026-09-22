<div align="center">

# 🤖 JARVIS — AI Voice Assistant

### A modular Python voice assistant that listens, understands, searches, automates, and responds through speech.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Optional-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/)
[![Text-to-Speech](https://img.shields.io/badge/Text--to--Speech-pyttsx3-6C63FF?style=for-the-badge&logo=python&logoColor=white)](https://github.com/nateshmbhat/pyttsx3)
[![Speech Recognition](https://img.shields.io/badge/Speech%20Recognition-Voice%20Input-00A67E?style=for-the-badge&logo=googleassistant&logoColor=white)](https://pypi.org/project/SpeechRecognition/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

`Wake Word: "Jarvis"` • `Voice-Controlled` • `Modular Services` • `AI + Web Search`

</div>

---

## 🧠 What is JARVIS?

**JARVIS** is a modular Python-based voice assistant built to make everyday computer interaction hands-free.

Say **"Jarvis"**, give a command, and the assistant routes it to the appropriate capability — from opening websites and playing YouTube videos to checking weather, searching the web, answering questions, telling jokes, and generating AI-powered responses.

The architecture separates speech handling, command processing, and individual services, making the system easier to test, replace, and extend.

---

## ✨ Core Capabilities

| Capability | What JARVIS can do |
|---|---|
| 🎙️ **Voice Activation** | Detect the `"Jarvis"` wake word and capture spoken commands |
| 🔊 **Speech Response** | Convert responses into spoken output with audio cues |
| 🌐 **Web & Browser Automation** | Open websites, perform searches, and trigger browser actions |
| ▶️ **YouTube Control** | Search and play requested videos |
| 🌤️ **Information Retrieval** | Handle weather, date, time, sports, and general information queries |
| 🔎 **Web Search** | Search the web for current or general information |
| 😂 **Entertainment** | Generate and deliver jokes on demand |
| 🤖 **AI Intelligence** | Use OpenAI for conversational responses when configured |
| 🔄 **Fallback Handling** | Fall back to web search when the optional AI service is unavailable |

---

## 🏗️ How It Works

```text
                       🎙️ USER
                          │
                    "Jarvis, ..."
                          │
                          ▼
                ┌───────────────────┐
                │ Speech Recognition│
                └─────────┬─────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ CommandProcessor │
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Local Tasks      Services       AI / Web
   Time · Date · Joke  Browser       OpenAI
                      YouTube        Search
                      Weather
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  🔊 JARVIS Response
```

Each capability lives behind dedicated services such as `BrowserService`, `WeatherService`, `WebService`, and `AIService`, coordinated by the assistant and speech layers.

---

## 💬 Example Commands

| Say | JARVIS responds by |
|---|---|
| `"Jarvis"` | Activating the assistant |
| `"Open YouTube"` | Opening YouTube |
| `"Play Believer"` | Searching and playing the requested video |
| `"Tell me the weather"` | Retrieving weather information |
| `"What is the date?"` | Reporting the current date |
| `"Tell me a joke"` | Generating a joke |
| `"Search for Python tutorials"` | Performing a web search |
| `"What is the latest cricket score?"` | Searching for sports information |

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| 🐍 **Python** | Core application and orchestration |
| 🎙️ **SpeechRecognition** | Speech-to-text input |
| 🎤 **PyAudio** | Microphone access |
| 🔊 **pyttsx3** | Text-to-speech output |
| ▶️ **PyWhatKit** | YouTube and browser automation |
| 😂 **PyJokes** | Joke generation |
| 🔔 **playsound3** | Start/end audio notifications |
| 🔎 **DDGS** | Web search |
| 🌐 **Requests** | HTTP/API requests |
| 🔐 **python-dotenv** | Environment configuration |
| 🤖 **OpenAI SDK** | Optional AI responses |

---

## 📂 Project Structure

<details>
<summary><b>▸ View project structure</b></summary>

```text
jarvis-ai-voice-assistant/
│
├── assets/
│   └── sounds/                  # Notification sounds
├── src/
│   └── jarvis/
│       ├── main.py              # Application entry point
│       ├── assistant/           # Command processing & conversation
│       ├── audio/               # Speech recognition & TTS
│       └── services/            # Browser, weather, search & AI
│
├── .env.example                 # Environment template
├── pyproject.toml
├── README.md
└── requirements.txt
```

</details>

---

## ⚙️ Installation & Usage

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd jarvis-ai-voice-assistant
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Install dependencies

**Windows:**

```bash
env\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Install JARVIS

```bash
env\Scripts\python.exe -m pip install -e .
```

### 5. Run

```bash
env\Scripts\python.exe -m jarvis.main
```

You can also launch it from VS Code through **Run and Debug → Run JARVIS**.

---

## 🤖 Optional OpenAI Integration

JARVIS works without an OpenAI API key. To enable AI-powered responses, create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> 🔒 Keep API keys private and never commit `.env` to the repository.

### 🔄 Built-in fallback

```text
OpenAI unavailable
       ↓
Web Search
       ↓
JARVIS Response
```

This keeps the assistant useful even when the optional AI layer is unavailable.

---

## 🚀 Roadmap

- [ ] Improved intent classification
- [ ] Conversation memory
- [ ] Offline speech recognition
- [ ] Dedicated sports-data integration
- [ ] Graphical user interface
- [ ] Expanded automated testing

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
