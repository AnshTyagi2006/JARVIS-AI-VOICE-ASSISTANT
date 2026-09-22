import datetime
import pyjokes

from jarvis.audio.sounds import play_end_sound, play_start_sound


class CommandProcessor:
    """Processes commands given to JARVIS."""

    def __init__(
        self,
        speech_manager,
        browser_service,
        weather_service,
        ai_service,
        conversation_handler=None,
    ):
        self.speech = speech_manager
        self.browser = browser_service
        self.weather = weather_service
        self.ai = ai_service
        self.conversation = conversation_handler

    def process_command(self, command):
        """
        Process a single user command.

        Returns:
            True  -> keep JARVIS running
            False -> exit JARVIS
        """

        if not command:
            return True

        command = command.lower().strip()

        # -------------------------
        # Greetings
        # -------------------------

        if command in ["hello", "hey", "hi", "hello jarvis", "hey jarvis", "hi jarvis"]:
            self.speech.speak("Hello! I am JARVIS. How can I assist you today?")
            play_end_sound()
            return True

        # -------------------------
        # General conversation
        # -------------------------

        if "how r u" in command or "how are you" in command:
            self.speech.speak("All systems operational and ready for your commands.")
            play_end_sound()
            return True

        if "who created you" in command or "who made you" in command or "who built you" in command:
            self.speech.speak("I was designed and built by Ansh Tyagi using Python and web technologies.")
            play_end_sound()
            return True

        # -------------------------
        # Date
        # -------------------------

        if "date" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speech.speak(f"Today's date is {current_date}.")
            print(f"Date is {current_date}")
            play_end_sound()
            return True

        # -------------------------
        # Time
        # -------------------------

        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speech.speak(f"The current time is {current_time}.")
            print(f"The time is {current_time}.")
            play_end_sound()
            return True

        # -------------------------
        # Websites
        # -------------------------

        website_commands = {
            "google": "Google",
            "youtube": "YouTube",
            "facebook": "Facebook",
            "instagram": "Instagram",
            "linked": "LinkedIn",
            "chat": "ChatGPT",
            "whatsapp": "WhatsApp",
            "spotify": "Spotify",
            "amazon": "Amazon",
            "flipkart": "Flipkart",
            "github": "GitHub",
        }

        for keyword, website_name in website_commands.items():
            if f"open {keyword}" in command or command == keyword:
                self.speech.speak(f"Opening {website_name}.")
                self.browser.open_website(keyword)
                play_end_sound()
                return True

        # -------------------------
        # Exit
        # -------------------------

        if "exit" in command or "bye" in command or "goodbye" in command:
            self.speech.speak("Goodbye. Have a great day!")
            play_end_sound()
            return False

        # -------------------------
        # Joke
        # -------------------------

        if "joke" in command:
            joke = pyjokes.get_joke()
            self.speech.speak(joke)
            print(joke)
            play_end_sound()
            return True

        # -------------------------
        # YouTube Music / Play
        # -------------------------

        if command.startswith("play "):
            song = command.replace("play ", "", 1).strip()
            if song:
                self.speech.speak(f"Playing {song} on YouTube.")
                self.browser.play_on_youtube(song)
                play_end_sound()
                return True

        # -------------------------
        # Google Search
        # -------------------------

        if command.startswith("search ") or "search for " in command:
            query = command.replace("search for ", "").replace("search ", "").strip()
            if query:
                self.speech.speak(f"Searching Google for {query}.")
                self.browser.search_google(query)
                play_end_sound()
                return True

        # -------------------------
        # Weather (Smart City Extraction)
        # -------------------------

        if "weather" in command or "temperature" in command:
            city = None
            for prefix in ["weather in ", "weather of ", "weather for ", "temperature in ", "temperature of ", "temperature for "]:
                if prefix in command:
                    city = command.split(prefix, 1)[1].strip()
                    break

            if not city:
                # Remove trigger words to see if city remains
                words = command.replace("weather", "").replace("temperature", "").replace("what is the", "").replace("tell me the", "").replace("in", "").replace("of", "").strip()
                if words:
                    city = words

            if not city:
                city = "Delhi"

            city = city.title()
            weather_info = self.weather.get_weather(city)

            if weather_info:
                response_text = f"The weather in {city} is {weather_info}."
                self.speech.speak(response_text)
                print(response_text)
            else:
                self.speech.speak(f"Sorry, I couldn't fetch the weather for {city} right now.")

            play_end_sound()
            return True

        # -------------------------
        # Real AI Chat & Knowledge Fallback
        # -------------------------

        try:
            ai_reply = self.ai.generate_response(command)
            if ai_reply and str(ai_reply).strip():
                reply_text = self._extract_clean_summary(str(ai_reply))
                self.speech.speak(reply_text)
                print(f"JARVIS AI: {reply_text}")
            else:
                self.speech.speak("I processed your query. Let me know if you need anything else.")
        except Exception as e:
            print(f"AI response error: {e}")
            self.speech.speak("I'm online and listening. How can I help you?")

        play_end_sound()
        return True

    @staticmethod
    def _extract_clean_summary(text):
        """Return a clean 1-2 sentence summary for spoken AI output."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return "Here is what I found."
        
        # Take first 2 non-empty lines
        summary = " ".join(lines[:2])
        if len(summary) > 280:
            summary = summary[:277] + "..."
        return summary