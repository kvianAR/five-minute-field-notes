# Build notes and verification

Built as a new project on October 7, 2026 for Hacktoberfest Week 1. Codex assisted with implementation, documentation, and testing. No DevRelay session was recorded or published.

## What was built

- A standard-library Python HTTP server with one `POST /api/card` endpoint.
- A responsive web form and printable field card in a single HTML file.
- Local Ollama inference with the open-weight `gemma3:1b` model.
- A 31-second silent demo made from screenshots of the running app. The video shows the actual selection, loading, and generated-card states. It does not show an outdoor field visit.
- The screenshots, slide-building script, and video encoder source are kept in `demo/production/` for reproducibility.

## Verification completed

- Ran `python3 -m unittest -v tests.py`: two checks passed.
- Opened the app in a browser and generated a real card using **balcony / sounds / seated / 5 minutes**.
- Confirmed a generated card displays three cues, a reflection question, and `Generated locally by gemma3:1b`.
- Sent an invalid setting to `/api/card` and confirmed HTTP 400.
- Played back sample frames from the 31-second H.264 MP4 and confirmed it has one video track and no audio track.

## Limits

- The 1B model can generate repetitive or unsuitable cues. Users should skip any cue that does not fit the actual place or conditions.
- No live weather, map, species, or safety data is available.
- No real outdoor test or DevRelay recording is claimed here.
