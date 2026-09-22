# Render Deployment — JARVIS

## Render settings

Create a **Web Service** from this repository.

- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn server:app --bind 0.0.0.0:$PORT`
- **Health Check Path:** `/health`

Add `OPENAI_API_KEY` in Render's Environment Variables if you want OpenAI-powered responses.

## Why this version is deployment-ready

- `server.py` serves `/` and `/health`.
- Render's `$PORT` and `0.0.0.0` are supported.
- `PyAudio` is installed only on Windows, so Linux web deployment does not require local microphone drivers.
- Server-side sound playback is disabled for the web deployment; the browser plays the UI sound cues.
- Website actions such as **Open YouTube**, **Open GitHub**, Google search, and YouTube search are executed in the visitor's browser.

## Important

The original desktop assistant can still use the local microphone/audio stack when run locally. The deployed web version uses the browser microphone and browser speech synthesis instead.

After deployment, Render provides a public HTTPS URL such as:

`https://your-service-name.onrender.com`
