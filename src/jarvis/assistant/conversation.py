from jarvis.audio.sounds import play_end_sound


class ConversationHandler:
    """Handles AI and web-based information requests."""

    def __init__(self, speech_manager, ai_service, web_service):
        self.speech = speech_manager
        self.ai = ai_service
        self.web = web_service

    def handle_news(self, command):
        """Handle a news request using web search."""

        try:
            result = self.web.get_answer(command)

            if result:
                answer = self._format_web_result(result)
            else:
                answer = "Sorry, I couldn't find relevant information."

            print(f"WEB: {answer}")
            self.speech.speak(answer)

        except Exception as error:
            print(f"News error: {error}")

            self.speech.speak(
                "Sorry, I couldn't retrieve the latest information."
            )

        finally:
            play_end_sound()

    def start_ai_conversation(self, command):
        """
        Handle one general question.

        OpenAI is used when available.
        Web search is used as a free fallback.
        """

        try:
            # ---------------------------------
            # Try AI first
            # ---------------------------------

            if self.ai.is_available:
                output = self.ai.generate_response(command)

                if output:
                    print(f"AI: {output}")

                    summary = self._extract_response(
                        str(output)
                    )

                    self.speech.speak(summary)
                    play_end_sound()
                    return

            # ---------------------------------
            # Free web-search fallback
            # ---------------------------------

            print("AI unavailable. Using web search...")

            result = self.web.get_answer(command)

            if result:
                answer = self._format_web_result(result)

                print(f"WEB: {answer}")
                self.speech.speak(answer)

            else:
                self.speech.speak(
                    "I couldn't find a reliable answer "
                    "to that question."
                )

        except Exception as error:
            print(f"Information request error: {error}")

            self.speech.speak(
                "Sorry, I couldn't process that request."
            )

        finally:
            play_end_sound()

    @staticmethod
    def _format_web_result(result):
        """Convert a web-search result into a short voice response."""

        title = result.get("title", "").strip()
        body = result.get("body", "").strip()

        if body:
            return body

        if title:
            return title

        return "I found a result, but couldn't extract an answer."

    @staticmethod
    def _extract_response(text):
        """Return a concise AI response suitable for speech."""

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return "I don't have a response for that."

        if len(lines) == 1:
            return lines[0]

        return f"{lines[0]} {lines[-1]}"