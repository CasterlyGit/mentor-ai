# mentor-ai

A real-time multimodal coding mentor. It watches your screen, listens to your voice, and offers live guidance — like pair programming with someone who can actually see what you're stuck on.

Privacy-first: transcription runs locally via Whisper; only structured prompts go to the cloud.

---

## What it does

- **Screen capture** — periodic frames of your active workspace are pulled into the context.
- **Voice input** — push-to-talk, transcribed locally with Whisper.
- **AI guidance** — Groq for fast inference; the model gets your transcript + recent screen context and replies with targeted help.
- **FastAPI backend** — single Python service that owns the capture loop, the STT pipeline, and the LLM call.

Phase 1 MVP is complete. An Electron frontend is planned to replace the current bare-bones UI with a proper desktop overlay.

## Stack

| Layer | Choice |
|---|---|
| Backend | FastAPI · Python 3.11+ |
| STT | Whisper (local) |
| LLM | Groq API |
| Capture | Native screen + audio capture |
| Frontend | Electron (planned) |

## Run

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Add your Groq key to `.env`:

```
GROQ_API_KEY=...
```

## Layout

```
backend/                # FastAPI service: capture loop, STT, LLM
frontend/               # Electron shell (in progress)
```

## Roadmap

- Electron desktop overlay with persistent always-on-top mentor window
- Conversation memory across sessions
- Per-language / per-framework persona switching
- Optional cloud STT for low-RAM machines

## License

MIT.
