import os
import sys
import datetime
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS

# Add src to python path for jarvis imports
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jarvis.audio.speech import SpeechManager
from jarvis.services.ai_service import AIService
from jarvis.services.weather_service import WeatherService
from jarvis.services.browser_service import BrowserService
from jarvis.services.web_service import WebService
from jarvis.assistant.conversation import ConversationHandler
from jarvis.assistant.commands import CommandProcessor

# Web deployments do not have access to the server machine's speakers or GUI.
# The browser handles audio cues, speech output, and browser actions instead.
import jarvis.assistant.commands as _command_module
import jarvis.assistant.conversation as _conversation_module
_command_module.play_start_sound = lambda: None
_command_module.play_end_sound = lambda: None
_conversation_module.play_end_sound = lambda: None


class WebBrowserService(BrowserService):
    """Browser actions are executed by the visitor's browser via web/app.js."""

    def open_website(self, name):
        return name in self.WEBSITES

    def search_google(self, query):
        return True

    def play_on_youtube(self, song):
        return True

app = Flask(__name__, static_folder="web", static_url_path="")
CORS(app)


class WebSpeechManager(SpeechManager):
    """
    Web-adapted SpeechManager that records spoken messages
    so they can be returned as JSON to the web frontend,
    while optionally triggering local TTS.
    """

    def __init__(self, enable_local_tts=False):
        super().__init__()
        self.spoken_messages = []
        self.enable_local_tts = enable_local_tts

    def speak(self, text):
        if not text:
            return
        text_str = str(text).strip()
        safe_str = text_str.encode('ascii', errors='ignore').decode('ascii')
        print(f"JARVIS [WEB]: {safe_str if safe_str else text_str}")
        self.spoken_messages.append(text_str)

        if self.enable_local_tts:
            try:
                super().speak(text_str)
            except Exception as e:
                print(f"Local TTS warning: {e}")

    def clear_messages(self):
        self.spoken_messages = []


# Global JARVIS instances
speech_manager = WebSpeechManager(enable_local_tts=False)
ai_service = AIService()
weather_service = WeatherService()
browser_service = WebBrowserService()
web_service = WebService()

conversation_handler = ConversationHandler(
    speech_manager=speech_manager,
    ai_service=ai_service,
    web_service=web_service,
)

command_processor = CommandProcessor(
    speech_manager=speech_manager,
    browser_service=browser_service,
    weather_service=weather_service,
    ai_service=ai_service,
    conversation_handler=conversation_handler,
)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "JARVIS"})


@app.route("/")
def index():
    """Serve main JARVIS web application interface."""
    return send_from_directory("web", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve frontend static files (css, js, images)."""
    return send_from_directory("web", filename)


@app.route("/api/sounds/<sound_name>")
def serve_sound(sound_name):
    """Serve original audio notification assets."""
    sounds_dir = ROOT_DIR / "assets" / "sounds"
    sound_path = sounds_dir / sound_name
    if sound_path.exists():
        return send_file(sound_path, mimetype="audio/mpeg")
    return jsonify({"error": "Sound file not found"}), 404


@app.route("/api/info", methods=["GET"])
def get_info():
    """Return system info, author details, tech stack, and commands for web UI."""
    return jsonify({
        "name": "JARVIS AI Voice Assistant",
        "version": "2.0 Web Edition",
        "status": "ONLINE",
        "author": {
            "name": "Ansh Tyagi",
            "role": "B.Tech — Artificial Intelligence & Data Science",
            "github": "https://github.com/AnshTyagi2006",
            "linkedin": "https://www.linkedin.com/in/ansh-tyagi2006/",
            "email": "anshtyagiansh0@gmail.com"
        },
        "tech_stack": [
            "Python 3.10+", "SpeechRecognition", "PyAudio", "pyttsx3",
            "PyWhatKit", "PyJokes", "DuckDuckGo DDGS", "OpenAI SDK", "Flask"
        ],
        "ai_available": ai_service.is_available,
        "supported_commands": [
            {"command": "Jarvis", "description": "Wake word activation"},
            {"command": "Open YouTube", "description": "Opens YouTube in browser"},
            {"command": "Play Believer", "description": "Plays song directly on YouTube"},
            {"command": "Tell me the weather in Delhi", "description": "Reports weather forecast"},
            {"command": "What is the time / date?", "description": "Speaks current time or date"},
            {"command": "Tell me a joke", "description": "Generates a hilarious programmer joke"},
            {"command": "Search Python tutorials", "description": "Performs live web search"},
            {"command": "Latest news headlines", "description": "Retrieves trending news updates"}
        ]
    })


@app.route("/api/process_command", methods=["POST"])
def process_command():
    """
    Process incoming user command string and execute Python JARVIS logic.
    Returns spoken responses, status, and sound triggers.
    """
    data = request.get_json() or {}
    user_command = data.get("command", "").strip()

    if not user_command:
        return jsonify({
            "status": "empty",
            "response": "I didn't catch that. Please speak or type a command.",
            "messages": ["I didn't catch that. Please speak or type a command."],
            "sound": "ding_end.mp3"
        })

    # Clear previous messages
    speech_manager.clear_messages()

    # Process command through core JARVIS CommandProcessor
    try:
        should_continue = command_processor.process_command(user_command)
        messages = speech_manager.spoken_messages.copy()
        
        # If no message recorded by speak(), fallback response
        if not messages:
            messages = ["Command processed successfully."]

        full_response = " ".join(messages)

        return jsonify({
            "status": "success",
            "command": user_command,
            "response": full_response,
            "messages": messages,
            "should_continue": should_continue,
            "sound": "ding_end.mp3",
            "ai_used": ai_service.is_available
        })

    except Exception as e:
        print(f"Error processing command '{user_command}': {e}")
        return jsonify({
            "status": "error",
            "command": user_command,
            "response": f"An error occurred while executing command: {str(e)}",
            "messages": [f"An error occurred: {str(e)}"],
            "sound": "ding_end.mp3"
        }), 500


@app.route("/api/listen", methods=["POST"])
def trigger_backend_listen():
    """Trigger server-side microphone speech recognition if needed."""
    try:
        recognized_text = speech_manager.listen()
        return jsonify({
            "status": "success",
            "recognized_text": recognized_text
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 60)
    print("Starting JARVIS AI Web Assistant Backend Server...")
    print(f"Listening on http://0.0.0.0:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False)
