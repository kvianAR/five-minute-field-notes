#!/usr/bin/env python3
"""Tiny local web app for AI-generated outdoor observation cards."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("FIELD_NOTES_MODEL", "gemma3:1b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8765"))
SETTINGS = {"park", "street", "garden", "balcony", "campus"}
INTERESTS = {"sounds", "shapes", "textures", "colors"}
ACCESS = {"walking", "seated"}

CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "cues": {"type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 3},
        "reflection": {"type": "string"},
    },
    "required": ["title", "cues", "reflection"],
}


def make_card(settings, interest, access, minutes, opener=urlopen):
    prompt = (
        "Create a short outdoor observation card for an adult. "
        "The person will be in this setting: {setting}; interested in {interest}; "
        "mode: {access}; total time: {minutes} minutes. "
        "Return JSON with title, exactly three cues, and one reflection question. "
        "Each cue must be one short action that can be done at or very near one safe spot. "
        "Make the three cues distinct and specifically fit the setting and interest. "
        "For seated mode, never require walking or standing. "
        "Use only unaided senses; no tools, phone, camera, flashlight, or special equipment. "
        "For a sounds focus, every cue must be about listening, not looking. "
        "Do not suggest collecting plants, touching animals, crossing roads, "
        "entering restricted places, identifying edible species, or staring at the phone. "
        "Do not claim to know current weather, nearby landmarks, or what wildlife is present. "
        "Use plain English, an inviting tone, and fewer than 17 words per cue."
    ).format(setting=settings, interest=interest, access=access, minutes=minutes)
    body = json.dumps({
        "model": MODEL,
        "stream": False,
        "format": CARD_SCHEMA,
        "options": {"temperature": 0.5, "num_predict": 230},
        "messages": [
            {"role": "system", "content": "You write practical outdoor observation prompts. Output only valid JSON."},
            {"role": "user", "content": prompt},
        ],
    }).encode("utf-8")
    request = Request(OLLAMA_URL + "/api/chat", data=body, headers={"Content-Type": "application/json"})
    with opener(request, timeout=90) as response:
        result = json.load(response)
    card = json.loads(result["message"]["content"])
    if not isinstance(card, dict) or not isinstance(card.get("cues"), list) or len(card["cues"]) != 3:
        raise ValueError("The model returned an incomplete card. Try again.")
    for key in ("title", "reflection"):
        if not isinstance(card.get(key), str) or not card[key].strip() or len(card[key]) > 180:
            raise ValueError("The model returned an incomplete card. Try again.")
    if any(not isinstance(cue, str) or not cue.strip() or len(cue) > 180 for cue in card["cues"]):
        raise ValueError("The model returned an incomplete card. Try again.")
    return {"title": card["title"].strip(), "cues": [cue.strip() for cue in card["cues"]],
            "reflection": card["reflection"].strip(), "model": MODEL}


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        body = (ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/card":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 2048:
                raise ValueError("Request is too large or empty.")
            data = json.loads(self.rfile.read(length))
            setting, interest, access, minutes = (data.get(k) for k in ("setting", "interest", "access", "minutes"))
            if setting not in SETTINGS or interest not in INTERESTS or access not in ACCESS or minutes not in (5, 10, 15):
                raise ValueError("Choose a valid setting, focus, pace, and duration.")
            self.reply(200, make_card(setting, interest, access, minutes))
        except (ValueError, KeyError, TypeError) as exc:
            self.reply(400, {"error": str(exc)})
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            self.reply(503, {"error": "Local Ollama is unavailable. Start Ollama and pull " + MODEL + "."})


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Field Notes: http://{HOST}:{PORT} | model: {MODEL}", flush=True)
    server.serve_forever()
