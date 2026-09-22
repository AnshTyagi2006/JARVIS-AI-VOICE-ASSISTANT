import os
import sys
import time
import webbrowser
import threading
from server import app

def open_browser():
    """Wait for server startup then open default web browser."""
    time.sleep(1.5)
    print("Opening JARVIS AI Web Interface in browser...")
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 65)
    print("JARVIS AI VOICE ASSISTANT -- FULL-STACK WEB EDITION")
    print("   Developed by Ansh Tyagi (B.Tech AI & Data Science)")
    print("=" * 65)
    print("Access Web Interface at: http://127.0.0.1:5000")
    print("=" * 65)
    
    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask App
    app.run(host="127.0.0.1", port=5000, debug=False)
