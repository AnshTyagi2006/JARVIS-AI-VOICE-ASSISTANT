from pathlib import Path

from playsound3 import playsound


SOUNDS_DIR = (
    Path(__file__).resolve().parents[3]
    / "assets"
    / "sounds"
)


def play_start_sound():
    """Play the sound used when JARVIS starts listening."""
    sound_path = SOUNDS_DIR / "ding_start.mp3"
    playsound(str(sound_path))


def play_end_sound():
    """Play the sound used when JARVIS finishes a response."""
    sound_path = SOUNDS_DIR / "ding_end.mp3"
    playsound(str(sound_path))