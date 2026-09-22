from jarvis.audio.speech import SpeechManager
from jarvis.audio.sounds import play_start_sound, play_end_sound

from jarvis.services.ai_service import AIService
from jarvis.services.weather_service import WeatherService
from jarvis.services.browser_service import BrowserService
from jarvis.services.web_service import WebService

from jarvis.assistant.conversation import ConversationHandler
from jarvis.assistant.commands import CommandProcessor


def create_jarvis():
    """Create and configure all JARVIS components."""

    speech_manager = SpeechManager()

    ai_service = AIService()
    weather_service = WeatherService()
    browser_service = BrowserService()
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

    return speech_manager, command_processor


def run():
    """Start the JARVIS voice assistant."""

    speech_manager, command_processor = create_jarvis()

    speech_manager.speak("Initializing JARVIS...")

    while True:
        wake_command = speech_manager.listen()

        if "jarvis" in wake_command:
            play_start_sound()

            speech_manager.speak(
                "Yes, how can I help you?"
            )

            play_start_sound()

            user_command = speech_manager.listen()

            if user_command:
                should_continue = (
                    command_processor.process_command(
                        user_command
                    )
                )

                if not should_continue:
                    break

            else:
                speech_manager.speak(
                    "Sorry, I couldn't understand the command."
                )

                play_end_sound()


if __name__ == "__main__":
    run()