import webbrowser


class BrowserService:
    """Handles browser-based actions."""

    WEBSITES = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "chat": "https://www.chatgpt.com",
        "whatsapp": "https://www.whatsapp.com",
        "spotify": "https://www.spotify.com",
        "amazon": "https://www.amazon.com",
        "flipkart": "https://www.flipkart.com",
    }

    def open_website(self, name):
        """Open a supported website."""
        url = self.WEBSITES.get(name)

        if url:
            webbrowser.open(url)
            return True

        return False

    def search_google(self, query):
        """Search Google for a query."""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def play_on_youtube(self, song):
        """Play a song on YouTube."""
        import pywhatkit

        pywhatkit.playonyt(song)
        
        