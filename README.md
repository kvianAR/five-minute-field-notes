# Five-Minute Field Notes 🌿

A tiny local web app that turns a nearby place and a chosen sense into a three-step outdoor observation card. Make the card, print it or remember it, and put the screen away. Built during the Hacktoberfest 2026 Week 1 **Touch Grass** window.


**[Watch the 31-second silent demo](demo/five-minute-field-notes-demo.mp4)** · [Build notes and checks](BUILD_NOTES.md)

## What the AI does

Google's open-weight `gemma3:1b` model writes the card through Ollama's local inference API. The prompts change with the setting, focus, pace, and time you choose. The app does not fetch weather, maps, or species data and does not claim to know what is present at your location. It sends no place or location information to a cloud AI service. After the model has been downloaded, card generation works without internet.

The app is an experiment, not an accessibility or navigation aid. Stay in an area you can safely access. Observe plants and animals without disturbing them.

## Run on a Mac

1. Install [Ollama](https://ollama.com/download) and open it. In Terminal, download the small model once:

   ```sh
   ollama pull gemma3:1b
   ```

2. In Terminal, go to this folder and start the web app:

   ```sh
   cd /path/to/five-minute-field-notes
   python3 app.py
   ```

3. Open [http://127.0.0.1:8765](http://127.0.0.1:8765). Choose a setting, focus, pace, and duration, then click **Make my field card**.

If Ollama is installed but not running, start it from Applications or run `ollama serve` in another Terminal window. Python 3.9+ is enough; there are no Python packages to install. The first response may take longer while the model loads.

To use another local Ollama model, run `FIELD_NOTES_MODEL=your-model-name python3 app.py`. The default model is about 815 MB. The app listens only on `127.0.0.1`.

## Two-minute demo flow

1. Select **Balcony or doorstep → Sounds → From one seated spot → 5 minutes**.
2. Generate a card and point out that the page says `Generated locally by gemma3:1b`.
3. Print/save the card and close the screen.
4. Take the card to the chosen outdoor spot. Do the three cues without taking photos or sharing a precise location.
5. Answer the reflection question when you return. Mention one real observation in the DEV post; do not invent an outdoor test.

You can also show the network independence by switching Wi-Fi off *after* downloading the model and generating another card. The UI itself is served locally.

## How it works

`index.html` is the full user interface. `app.py` serves it and handles one `POST /api/card` endpoint. Inputs are limited to fixed choices. The server calls Ollama's `/api/chat` with a JSON schema, checks the result, and returns a compact card. The UI inserts every model string as text, not HTML. There is no database, account, analytics, or external front-end asset.

## Limits and next steps

- A 1B model can still produce repetitive or awkward cues. Generate another card if one is unsuitable.
- The prompt discourages unsafe suggestions, but it cannot prove every generated suggestion is safe. You choose what to do outside.
- The app does not detect weather, terrain, traffic, or accessible entrances.
- A future version could offer language choice and an on-device speech mode for eyes-free use.

## Files

- `app.py` — local server and model call
- `index.html` — responsive UI and printable card
- `tests.py` — small checks for the model request and card validation
- `DEV_SUBMISSION.md` — draft matching the official submission template
- `SAMPLE_CARD.md` — one actual local-model result for a quick preview
- `BUILD_NOTES.md` — how this was built and verified
- `demo/` — silent MP4 walkthrough and cover image
- `demo/production/` — source screenshots and scripts used to assemble the demo video
- `releases/` — local downloadable copies and ZIP archive (ignored by Git)

## Submit to Week 1

This is a new public project for Week 1. Publish the article through the [official Week 1 submission template](https://dev.to/challenges/hacktoberfest-week1-2026-10-05), linking this repository and the demo video. The challenge requires the `devchallenge` and `hf26challenge` tags. The official deadline is **October 11, 2026 at 11:59 PM PDT**, which is **October 12 at 12:29 PM IST**. If any commits are made after that deadline, note those changes here.

## License and credits

This project's code is MIT licensed (see `LICENSE`). It uses [Ollama](https://ollama.com/) for local inference and Google's [Gemma 3](https://ollama.com/library/gemma3) open-weight model, which has its own model terms. The project does not bundle model weights.
