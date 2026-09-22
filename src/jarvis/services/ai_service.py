import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class AIService:
    """Provides optional AI-powered functionality for JARVIS."""

    GENERAL_SYSTEM_PROMPT = (
        "You are JARVIS, a helpful AI voice assistant. "
        "Give clear, concise and useful answers suitable for "
        "being spoken aloud by a voice assistant."
    )

    NEWS_SYSTEM_PROMPT = (
        "You are JARVIS, a helpful AI voice assistant. "
        "Answer news-related questions clearly and concisely."
    )

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as error:
                print(f"AI client initialization error: {error}")
                self.client = None

    @property
    def is_available(self):
        """Return True when an OpenAI API key is configured."""
        return self.client is not None

    def generate_response(self, command):
        """
        Generate an AI response.

        Returns:
            str: AI response when successful.
            None: When AI is unavailable or the request fails.
        """

        if not self.is_available:
            print("AI unavailable: no API key configured.")
            return None

        try:
            response = self.client.responses.create(
                model="gpt-5-mini",
                instructions=self.GENERAL_SYSTEM_PROMPT,
                input=command,
            )

            return response.output_text

        except Exception as error:
            print(f"AI service error: {error}")
            return None

    def generate_news_response(self, command):
        """
        Generate an AI-powered news response.

        Returns:
            str: AI response when successful.
            None: When AI is unavailable or the request fails.
        """

        if not self.is_available:
            print("AI unavailable: no API key configured.")
            return None

        try:
            response = self.client.responses.create(
                model="gpt-5-mini",
                instructions=self.NEWS_SYSTEM_PROMPT,
                input=command,
            )

            return response.output_text

        except Exception as error:
            print(f"News service error: {error}")
            return None