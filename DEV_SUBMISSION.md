---
title: "Five-Minute Field Notes: a local Gemma card that sends you outside"
published: false
tags: devchallenge, hf26challenge, opensource, gemma
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05).*

## What I Built

Five-Minute Field Notes makes a tiny observation mission for a place someone can already access: a park, garden, quiet sidewalk, campus, or balcony. Pick a focus (sounds, shapes, textures, or colors), a pace (slow stroll or one seated spot), and a 5, 10, or 15-minute duration. A local model writes three short cues and a question to consider afterward. The point is to close the screen and spend the time outside.

I avoided maps, live weather, and species identification. The app cannot know what is present at a particular place or which route is safe. It offers an adaptable way to pay attention where you already are.

This is a **solo submission**. There are no teammates to credit.

## Demo

**[Watch the 31-second silent demo](https://github.com/kvianAR/five-minute-field-notes/blob/main/demo/five-minute-field-notes-demo.mp4).** It shows the running app, the selected settings, Gemma generating a card, and the finished printable card. There is no voice or music.

The demo uses **Balcony or doorstep → Sounds → From one seated spot → 5 minutes**. The example card asks the user to listen for changes in nearby sounds, then put the screen away. I have not included outdoor footage or claimed an outdoor field test. The video shows the working software.

## Code

**[Public GitHub repository](https://github.com/kvianAR/five-minute-field-notes)** · [Setup instructions](https://github.com/kvianAR/five-minute-field-notes#run-on-a-mac) · [Build notes and verification](https://github.com/kvianAR/five-minute-field-notes/blob/main/BUILD_NOTES.md)

The app is intentionally small: `app.py` is the local Python server and Ollama call; `index.html` is the responsive interface and printable card. `tests.py` checks the model request and card validation. Python's standard library is enough; no cloud API key or Python package installation is needed.

To run it on a Mac, install Ollama, then run:

```sh
git clone https://github.com/kvianAR/five-minute-field-notes.git
cd five-minute-field-notes
ollama pull gemma3:1b
python3 app.py
```

Open `http://127.0.0.1:8765` in a browser. Downloading the model needs internet once; afterward, generation runs locally.

## How I Built It

The browser sends four fixed choices to a Python server listening only on `127.0.0.1`. The server calls Ollama's local `/api/chat` endpoint with Google's open-weight Gemma 3 1B model and a JSON schema. Gemma generates the title, three observation cues, and reflection question. The server validates the shape and length of the response; the browser displays every model string as text and offers a print-friendly card.

Gemma is the core of the project: without model inference, the field card is not produced. A live browser run returned a three-cue card for balcony / sounds / seated / five minutes, and the app displayed the model name. Two automated checks passed; an invalid input request returned HTTP 400.

## Why Does Open Innovation Matter?

An outdoor prompt should not require sending someone's location or preferences to a remote AI service. With an open-weight model and local inference, this card can be generated on a Mac after the initial model download, without an internet connection or a per-request fee. The prompt and server code are inspectable, and another builder can swap the model through one environment variable.

There is a tradeoff: a small 1B model can write repetitive or unsuitable cues. The app validates the response structure, but it cannot verify real-world conditions. Users should skip any cue that does not fit their setting and stay in safe, accessible areas.

## My Agent Session

I used Codex to help implement, test, and document this project. I did **not** record a DevRelay session or publish a shareable agent trace, so there is no session embed to claim. The [build notes](https://github.com/kvianAR/five-minute-field-notes/blob/main/BUILD_NOTES.md) list what was built, what was verified, and the limits of the demo.

## Prize Categories

**Best Use of Gemma.** The app runs Google's open-weight `gemma3:1b` locally through Ollama. Every field card depends on Gemma's generated cues and reflection question. I am not entering any other partner category because this project does not use those partners' technologies.
