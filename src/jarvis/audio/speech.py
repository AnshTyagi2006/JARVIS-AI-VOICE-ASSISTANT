import speech_recognition as sr
import pyttsx3


class SpeechManager:
    """Handles speech recognition and text-to-speech."""

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Convert text to speech using a fresh TTS engine."""

        if not text:
            return

        print(f"JARVIS: {text}")

        engine = pyttsx3.init()

        try:
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)

            engine.say(str(text))
            engine.runAndWait()

        finally:
            engine.stop()
            del engine

    def listen(self, lang="en-IN"):
        """Listen to the microphone and return recognized speech."""

        print("Listening...")

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=4,
                    phrase_time_limit=10,
                )

                command = self.recognizer.recognize_google(
                    audio,
                    language=lang,
                )

                print(f"You said: {command}")

                return command.lower()

            except (
                sr.WaitTimeoutError,
                sr.UnknownValueError,
                sr.RequestError,
            ):
                return ""

            except Exception as error:
                print(f"Speech recognition error: {error}")
                return ""